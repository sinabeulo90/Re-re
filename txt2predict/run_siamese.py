import argparse
import sys
import logging
import math
import numpy as np
import os
import pandas as pd
import pickle
import json
import datetime, time, random
import copy
import pymysql
import csv
import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__)))
from txt2predict.duplicate_questions.data.data_manager import DataManager
from txt2predict.duplicate_questions.data.embedding_manager import EmbeddingManager
from txt2predict.duplicate_questions.data.instances.sts_instance import STSInstance
from txt2predict.duplicate_questions.models.siamese_bilstm.siamese_bilstm import SiameseBiLSTM
from txt2predict.duplicate_questions.models.siamese_bilstm.siamese_matching_bilstm import SiameseMatchingBiLSTM

logger = logging.getLogger(__name__)

def create_testfile(sentence1):


    # MySQL Connection 연결
    db_conn = pymysql.connect(host='localhost', user='root', password='tkfkdgo0!!', db='Rere', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = db_conn.cursor()

    sql = "SELECT DISTINCT V_DESCRIPTION FROM V_DETAIL;"
    curs.execute(sql)
    rows = curs.fetchall()

    random.seed(datetime.datetime.now())
    csv_filename = os.path.join("txt2predict/predict_csv", "test_final-%d.csv" % (random.randint(0, int(time.time()))))

    with open(csv_filename, "w") as f:
        writer = csv.writer(f)
        for idx, row in enumerate(rows):

            data = [str(idx), sentence1, row[0]]
            writer.writerow(data)

    db_conn.close()

    return csv_filename, rows


config = {
    "batch_size": 128,
    "dataindexer_load_path": "",
    "early_stopping_patience": 0,
    "fine_tune_embeddings": False,
    "log_dir": "logs/",
    "log_period": 10,
    "mode": "predict",
    "model_load_dir": "",
    "model_name": "predict_model",
    "num_epochs": 10,
    "num_sentence_words": 30,
    "output_keep_prob": 1.0,
    "pretrained_embeddings_file_path": "txt2predict/data/glove.6B.300d.txt",
    "reweight_predictions_for_kaggle": False,
    "rnn_hidden_size": 256,
    "rnn_output_mode": "last",
    "run_id": "99",
    "share_encoder_weights": True,
    "test_file": "",
    "val_period": 250,
    "word_embedding_dim": 300,
    "word_embedding_matrix": [],
    "word_vocab_size": 107590
}

def get_SiameseBiLSTM_config(config):
    SiameseBiLSTM_config = copy.deepcopy(config)
    SiameseBiLSTM_config["dataindexer_load_path"] = "txt2predict/data/models/baseline_siamese/00/baseline_siamese-00-DataManager.pkl"
    SiameseBiLSTM_config["model_load_dir"] = "txt2predict/data/models/baseline_siamese/00"

    mode = SiameseBiLSTM_config["mode"]
    model_name = SiameseBiLSTM_config["model_name"]
    run_id = SiameseBiLSTM_config["run_id"]

    # Load the fitted DataManager
    with open(SiameseBiLSTM_config["dataindexer_load_path"], "rb") as f:
        data_manager = pickle.load(f)

    # Get the embeddings.
    embedding_manager = EmbeddingManager(data_manager.data_indexer)
    embedding_matrix = embedding_manager.get_embedding_matrix(
        SiameseBiLSTM_config["word_embedding_dim"],
        SiameseBiLSTM_config["pretrained_embeddings_file_path"])
    SiameseBiLSTM_config["word_embedding_matrix"] = embedding_matrix

    # Get the data.
    batch_size = SiameseBiLSTM_config["batch_size"]

    return data_manager, batch_size, SiameseBiLSTM_config, SiameseBiLSTM


def get_SiameseMatchingBiLSTM_config(config):
    SiameseMatchingBiLSTM_config = copy.deepcopy(config)
    SiameseMatchingBiLSTM_config["dataindexer_load_path"] = "txt2predict/data/models/siamese_matching/00/siamese_matching-00-DataManager.pkl"
    SiameseMatchingBiLSTM_config["model_load_dir"] = "txt2predict/data/models/siamese_matching/00"

    mode = SiameseMatchingBiLSTM_config["mode"]
    model_name = SiameseMatchingBiLSTM_config["model_name"]
    run_id = SiameseMatchingBiLSTM_config["run_id"]

    # Load the fitted DataManager
    with open(SiameseMatchingBiLSTM_config["dataindexer_load_path"], "rb") as f:
        data_manager = pickle.load(f)

    # Get the embeddings.
    embedding_manager = EmbeddingManager(data_manager.data_indexer)
    embedding_matrix = embedding_manager.get_embedding_matrix(
        SiameseMatchingBiLSTM_config["word_embedding_dim"],
        SiameseMatchingBiLSTM_config["pretrained_embeddings_file_path"])
    SiameseMatchingBiLSTM_config["word_embedding_matrix"] = embedding_matrix

    # Get the data.
    batch_size = SiameseMatchingBiLSTM_config["batch_size"]

    return data_manager, batch_size, SiameseMatchingBiLSTM_config, SiameseMatchingBiLSTM




def predict(string, args, percent):
    data_manager = args[0]
    batch_size = args[1]
    config = args[2]
    tf_model = args[3]

    # Initialize the model.
    tf.reset_default_graph()
    model = tf_model(config)
    model.build_graph()

    csv_filename, rows = create_testfile(string)
    config["test_file"] = csv_filename
    # use it to index the test data
    test_data_gen, test_data_size = data_manager.get_test_data_from_file(
        [config["test_file"]])

    config["word_vocab_size"] = data_manager.data_indexer.get_vocab_size()


    # Predict with the model
    model_load_dir = config["model_load_dir"]
    num_test_steps = int(math.ceil(test_data_size / batch_size))
    # Numpy array of shape (num_test_examples, 2)

    raw_predictions = model.predict(get_test_instance_generator=test_data_gen,
                                        model_load_dir=model_load_dir,
                                        batch_size=batch_size,
                                        num_test_steps=num_test_steps)
    # Remove the first column, so we're left with just the probabilities
    # that a question is a duplicate.
    is_duplicate_probabilities = np.delete(raw_predictions, 0, 1)
    is_duplicate_probabilities = is_duplicate_probabilities.flatten().tolist()
    predict_dict = dict(zip(rows, is_duplicate_probabilities))
    os.remove(csv_filename)

    description_list = []
    for description, value in predict_dict.items():
        if value > percent:
            description_list.append(description)

    return description_list



def init():
    return get_SiameseBiLSTM_config(config), get_SiameseMatchingBiLSTM_config(config)

# if __name__ == "__main__":
#     SiameseBiLSTM_init, SiameseMatchingBiLSTM_init = init()
#     print(predict("hello", SiameseBiLSTM_init))
#     print(predict("hello", SiameseMatchingBiLSTM_init))
