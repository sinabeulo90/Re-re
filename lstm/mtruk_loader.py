import csv
import random
import json
import numpy as np

def load_data(path):
    SEED = 5
    random.seed(SEED)

    list_statement1 = []
    list_statement2 = []
    list_answer = []

    with open(path) as f:
        reader = csv.DictReader(f)
        reader = list(reader)
        random.shuffle(reader)

        for row in reader:
            list_statement1.append(row['sentence_a'])
            list_statement2.append(row['sentence_b'])
            list_answer.append(row['answer'])


    length_80p = int(len(reader) * 0.8)
    length_10p = int(len(reader) * 0.1)

    train = DataSet(list_statement1[:length_80p], list_statement2[:length_80p], list_answer[:length_80p])
    val   = DataSet(list_statement1[length_80p:length_80p+length_10p], list_statement2[length_80p:length_80p+length_10p], list_answer[length_80p:length_80p+length_10p])
    test  = DataSet(list_statement1[length_80p+length_10p:], list_statement2[length_80p:length_80p+length_10p], list_answer[length_80p+length_10p:])

    return train, val, test


class DataSet:
    
    def __init__(self, list_statement1, list_statement2, list_answer):
        self.batch_pos = 0
        self.statement1 = list_statement1
        self.statement2 = list_statement2
        self.answer    = list_answer

        self.batch_size = len(list_answer)
    
    def next_batch(self, batch_size=1, class_size=6, one_hot=True, lower=True):
        statement1 = self.statement1[self.batch_pos:self.batch_pos+batch_size]
        statement2 = self.statement2[self.batch_pos:self.batch_pos+batch_size]

        answer    = self.answer[self.batch_pos:self.batch_pos+batch_size]
        answer    = [ int(_) for _ in answer]

        self.batch_pos += batch_size

        if one_hot:
            # [0, 0, 0, 0, 0]
            #   : class_size = 5
            answer = np.array(answer)
            vector = np.zeros((batch_size, class_size))
            vector[np.arange(batch_size), answer] = 1
            
            answer = vector

        if lower:
            statement1 = [ _.lower() for _ in statement1 ]
            statement2 = [ _.lower() for _ in statement2 ]


        if self.batch_pos > self.batch_size:
            self.batch_pos = 0

        return statement1, statement2, np.array(answer, dtype=np.float64)








if __name__ == "__main__":
    load_data("dataset/merged_mtruk.csv")