OLD_CHECKPOINT_FILE = "siamese_matching-00-11372"
NEW_CHECKPOINT_FILE = "siamese_matching2-00-11372"

import tensorflow as tf
vars_to_rename = {
    # "lstm/basic_lstm_cell/weights": "lstm/basic_lstm_cell/kernel",
    # "lstm/basic_lstm_cell/biases": "lstm/basic_lstm_cell/bias",
    # "lstm/basic_lstm_cell/weights": "lstm/basic_lstm_cell/weights",
    # "lstm/basic_lstm_cell/biases": "lstm/basic_lstm_cell/biases",
    "encode_sentences/encoded_sentence_one/bw/lstm_cell/kernel": "encode_sentences/encoded_sentence_one/bw/lstm_cell/weights",
    "encode_sentences/encoded_sentence_one/bw/lstm_cell/bias": "encode_sentences/encoded_sentence_one/bw/lstm_cell/biases",
    
    "encode_sentences/encoded_sentence_one/fw/lstm_cell/kernel": "encode_sentences/encoded_sentence_one/fw/lstm_cell/weights",
    "encode_sentences/encoded_sentence_one/fw/lstm_cell/bias": "encode_sentences/encoded_sentence_one/fw/lstm_cell/biases",
    
    "encode_sentences/encoded_sentence_one/bw/lstm_cell/bias/Adam": "encode_sentences/encoded_sentence_one/bw/lstm_cell/biases/Adam",
    "encode_sentences/encoded_sentence_one/bw/lstm_cell/bias/Adam": "encode_sentences/encoded_sentence_one/bw/lstm_cell/biases/Adam",
    
    "encode_sentences/encoded_sentence_one/fw/lstm_cell/kernel/Adam": "encode_sentences/encoded_sentence_one/bw/lstm_cell/weights/Adam",
    "encode_sentences/encoded_sentence_one/fw/lstm_cell/bias/Adam": "encode_sentences/encoded_sentence_one/bw/lstm_cell/biases/Adam",
}
new_checkpoint_vars = {}
reader = tf.train.NewCheckpointReader(OLD_CHECKPOINT_FILE)
for old_name in reader.get_variable_to_shape_map():
  print(old_name)
  
  if "lstm_cell/kernel" in old_name:
        new_name = old_name.replace("lstm_cell/kernel", "lstm_cell/weights")
  elif "lstm_cell/bias" in old_name:
        new_name = old_name.replace("lstm_cell/bias", "lstm_cell/biases")
  else:
    new_name = old_name

  new_checkpoint_vars[new_name] = tf.Variable(reader.get_tensor(old_name))

init = tf.global_variables_initializer()
saver = tf.train.Saver(new_checkpoint_vars)

with tf.Session() as sess:
  sess.run(init)
  saver.save(sess, NEW_CHECKPOINT_FILE)
