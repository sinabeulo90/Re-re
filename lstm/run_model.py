import sys
import numpy as np
from gensim.models.keyedvectors import KeyedVectors

import mtruk_loader
from constants import CONSTRACTIONS

# model_file = "./GoogleNews-vectors-negative300.bin.gz"      # 3,000,000 words
# model_file = "./freebase-vectors-skipgram1000-en.bin.gz"    # 1,422,903 words
model_file = "./glove.840B.300d.bin.gz"                     # 2,196,016 words
word2vec = KeyedVectors.load_word2vec_format(model_file, binary=True)

DUMP_300VEC = np.array([0.0 for _ in range(300)])
def Normalization(sentences, max_str_size):
    vec_sentences = []
    seq_length = []

    for sentence in sentences:
        seq = 0

        vec_sentence = []
        for word in sentence.split():
            word = word.replace(".", "").replace(",", "")
            if word in CONSTRACTIONS:
                word = CONSTRACTIONS[word].replace("/", "").replace(";", "")
                for _word in word.split():
                    if _word in word2vec:
                        vec_sentence.append(word2vec.wv[_word])
                        seq += 1

            else:
                if word in word2vec:
                    vec_sentence.append(word2vec.wv[word])
                    seq += 1

        while len(vec_sentence) != max_str_size:
            vec_sentence.append(np.array(DUMP_300VEC))

        vec_sentences.append(vec_sentence)
        seq_length.append(seq)

    return np.array(vec_sentences, dtype=np.float64), seq_length

import tensorflow as tf

MAX_STR = 1000
MAX_VEC = 300
NUM_UNIT = 50
BATCH_SIZE = 30

X1 = tf.placeholder(tf.float64, [None, MAX_STR, MAX_VEC])
X2 = tf.placeholder(tf.float64, [None, MAX_STR, MAX_VEC])
Y = tf.placeholder(tf.float64, [None])

X1_Seq = tf.placeholder(tf.int64, [None])
X2_Seq = tf.placeholder(tf.int64, [None])

batch_size = tf.placeholder(tf.int32, [])

cell = tf.nn.rnn_cell.BasicLSTMCell(NUM_UNIT)

init_state = cell.zero_state(batch_size, tf.float64)

outputs1, states1 = tf.nn.dynamic_rnn(
    cell,
    X1,
    sequence_length=X1_Seq,
    initial_state=init_state,
    dtype=tf.float64
)

outputs2, states2 = tf.nn.dynamic_rnn(
    cell,
    X2,
    sequence_length=X2_Seq,
    initial_state=init_state,
    dtype=tf.float64
)


outputs1 = outputs1[:, -1, :]
outputs2 = outputs2[:, -1, :]

logits = tf.exp(-tf.norm(outputs1-outputs2, axis=1))

loss = tf.reduce_mean(tf.square(Y - logits))
train = tf.train.AdadeltaOptimizer().minimize(loss)

accuracy = 1 - tf.reduce_mean(tf.square(Y - logits)) / 30

tf.summary.scalar("loss", loss)
tf.summary.scalar("accuracy", accuracy)
merged_summary_op = tf.summary.merge_all()

data_file = "./merged_mtruk.csv"
train_set, val_set, test_set = mtruk_loader.load_data(data_file)

val_sentence_a, val_sentence_b, val_answer = val_set.next_batch(BATCH_SIZE, one_hot=False)
val_a, val_seq_a = Normalization(val_sentence_a, MAX_STR)
val_b, val_seq_b = Normalization(val_sentence_b, MAX_STR)

val_feed_dict = {
        X1: val_a,
        X2: val_b,
        X1_Seq: val_seq_a,
        X2_Seq: val_seq_b,
        Y: val_answer/5,
        batch_size: len(val_seq_a)
    }


BATCH_RANGE = train_set.batch_size // BATCH_SIZE

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    summary_writer = tf.summary.FileWriter("./log")

    x_size = 100
    for epoch in range(1000):

        avg_cost = 0
        for batch_step in range(BATCH_RANGE):
            sentence_a, sentence_b, answer = train_set.next_batch(BATCH_SIZE, one_hot=False)

            train_a, seq_a = Normalization(sentence_a, MAX_STR)
            train_b, seq_b = Normalization(sentence_b, MAX_STR)

            train_feed_dict = {
                X1: train_a,
                X2: train_b,
                X1_Seq: seq_a,
                X2_Seq: seq_b,
                Y: answer/5,
                batch_size: len(seq_a)
            }

            _loss, _ = sess.run([loss, train], feed_dict=train_feed_dict)
            avg_cost += _loss
            
            _acc, summary = sess.run([accuracy, merged_summary_op], feed_dict=val_feed_dict)
            summary_writer.add_summary(summary, epoch * BATCH_RANGE + batch_step)

            if batch_step % 20 == 0:
                print("Epoch : %04d , Batch idx : %04d/%04d , cost = %.10f" % (epoch, batch_step, BATCH_RANGE, _loss))
            else:
                cnt = (batch_step + 1) % 20
                sys.stdout.write("\r%s" % ("." * cnt))
                sys.stdout.flush()
            
            del sentence_a
            del sentence_b
            del train_a
            del train_b

        print("Epoch : %04d , Avg.cost = %.10f" % (epoch, avg_cost))

        if epoch % 200 == 0:
            saver.save(sess, "lstm_saver/lstm", global_step=epoch)
