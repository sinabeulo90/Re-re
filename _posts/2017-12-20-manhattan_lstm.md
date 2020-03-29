---
layout: post
title: "5. Manhattan LSTM Model"
description : 문장과 문장의 유사성을 비교하기 위해서 Manhattan LSTM Model을 사용했습니다. 또한 Siamese LSTM, BiMPM 을 구현한 오픈소스를 사용해서 문장을 비교해보도록 하겠습니다.
tag: capstone
comments: false
---

이번에는 문장과 문장의 연관성을 수치화시키기 위해 'Manhattan LSTM' 모델을 활용할 것입니다.

이 모델과 관련된 논문을 tensorflow로 구현하신 분이 있어서 그분의 코드를 사용해습니다.
[paraphrase-id-tensorflow](https://github.com/nelson-liu/paraphrase-id-tensorflow) 에서 확인하실 수 있습니다.

## 기본 설치

``` shell
(venv)$ git clone https://github.com/nelson-liu/paraphrase-id-tensorflow.git

# 설치하는데 다소 시간이 걸립니다.
(venv)$ cd paraphrase-id-tensorflow
(venv)$ pip install -r requirements.txt
(venv)$ python -m nltk.downloader punkt

# 데이터, 학습된 모델, 로그 기록을 저장할 보조 폴더를 생성
(venv)$ make aux_dirs

# 학습 또는 예측을 위해 사용되는 벡터를 준비(단어를 벡터로 표현한 것)
(venv)$ make glove
(venv)$ GLOVE_FOLDER=data/external
(venv)$ unzip $GLOVE_FOLDER/glove.6B.zip -d $GLOVE_FOLDER && rm $GLOVE_FOLDER/glove.6B.zip
```

그리고 데이터 셋을 얻기 위해 [Kaggle](https://www.kaggle.com/c/quora-question-pairs/data)에 로그인을 하고 Data를 다운로드하고, data/raw/ 폴더에 압축을 풉니다.

![Kaggle]({{ site.assets | absolute_url }}/capstone/5_kaggle.png)

``` shell
(venv)$ make quora_data
```

이 코드에서는 3가지의 모델을 제공하고 있고, 학습과 예측하는 스크립트를 만들어 놓았습니다.

## 학습

1. the baseline Siamese BiLSTM
``` shell
$ python scripts/run_model/run_siamese.py train --share_encoder_weights --model_name=baseline_siamese --run_id=0
```

2. the Siamese BiLSTM with matching layer
``` shell
$ python scripts/run_model/run_siamese_matching_bilstm.py train --share_encoder_weights --model_name=siamese_matching --run_id=0
```

3. the BiMPM model
``` shell
$ python scripts/run_model/run_bimpm.py train --early_stopping_patience=5 --model_name=biMPM --run_id=0
```

그러면 다음과 같이 진행이 이루어집니다. 학습이 진행이 되면서 model/에 해당 모델의 checkpoint가 저장됩니다.

``` shell
2017-12-27 03:30:21,741 - INFO - duplicate_questions.data.data_manager - Getting training data from ['scripts/run_model/../../data/processed/quora/train_cleaned_train_split.csv']
2017-12-27 03:30:21,742 - INFO - duplicate_questions.data.dataset - Reading files ['scripts/run_model/../../data/processed/quora/train_cleaned_train_split.csv'] to a list of lines.
100%|██████████| 363861/363861 [00:00<00:00, 1221190.42it/s]
2017-12-27 03:30:23,104 - INFO - duplicate_questions.data.dataset - Creating list of <class 'duplicate_questions.data.instances.sts_instance.STSInstance'> instances from list of lines.
100%|██████████| 363861/363861 [02:12<00:00, 2737.46it/s]
2017-12-27 03:32:36,469 - INFO - duplicate_questions.data.dataset - Finished reading dataset; label counts: [(0, 229425), (1, 134436)]
2017-12-27 03:32:36,505 - INFO - duplicate_questions.data.data_manager - Fitting data indexer word dictionary, min_count is 1.
2017-12-27 03:32:36,505 - INFO - duplicate_questions.data.data_indexer - Fitting word dictionary with min count of 1
100%|██████████| 363861/363861 [01:20<00:00, 4512.50it/s]
2017-12-27 03:33:57,586 - INFO - duplicate_questions.data.data_manager - Indexing dataset
100%|██████████| 363861/363861 [01:09<00:00, 5261.33it/s]
2017-12-27 03:35:09,542 - INFO - duplicate_questions.data.data_manager - Instance max lengths {'num_sentence_words': 272, 'num_word_characters': 78}
2017-12-27 03:35:09,542 - INFO - duplicate_questions.data.data_manager - Padding lengths to length: {'num_sentence_words': 30, 'num_word_characters': 78}
2017-12-27 03:35:09,542 - INFO - duplicate_questions.data.data_manager - Getting validation data from ['scripts/run_model/../../data/processed/quora/train_cleaned_val_split.csv']
2017-12-27 03:35:09,542 - INFO - duplicate_questions.data.dataset - Reading files ['scripts/run_model/../../data/processed/quora/train_cleaned_val_split.csv'] to a list of lines.
100%|██████████| 40429/40429 [00:00<00:00, 1148127.32it/s]
2017-12-27 03:35:09,703 - INFO - duplicate_questions.data.dataset - Creating list of <class 'duplicate_questions.data.instances.sts_instance.STSInstance'> instances from list of lines.
100%|██████████| 40429/40429 [00:13<00:00, 2893.19it/s]
2017-12-27 03:35:23,726 - INFO - duplicate_questions.data.dataset - Finished reading dataset; label counts: [(0, 25602), (1, 14827)]
2017-12-27 03:35:23,730 - INFO - duplicate_questions.data.data_manager - Indexing validation dataset with DataIndexer fit on train data.
100%|██████████| 40429/40429 [00:11<00:00, 3658.70it/s]
2017-12-27 03:35:34,781 - INFO - duplicate_questions.data.data_manager - Max lengths in training data: {'num_sentence_words': 30, 'num_word_characters': 78}
2017-12-27 03:35:34,781 - INFO - duplicate_questions.data.data_manager - Padding lengths to length: {'num_sentence_words': 30, 'num_word_characters': 78}
2017-12-27 03:35:34,781 - INFO - __main__ - Writing logs to scripts/run_model/../../logs/baseline_siamese/00
2017-12-27 03:35:34,781 - INFO - __main__ - log path scripts/run_model/../../logs/baseline_siamese/00 does not exist, creating it
2017-12-27 03:35:34,781 - INFO - __main__ - Writing params to scripts/run_model/../../logs/baseline_siamese/00/trainparams.json
2017-12-27 03:35:34,782 - INFO - duplicate_questions.data.embedding_manager - Reading pretrained embeddings from scripts/run_model/../../data/external/glove.6B.300d.txt
400000it [00:32, 12266.27it/s]
2017-12-27 03:36:08,581 - WARNING - duplicate_questions.models.siamese_bilstm.siamese_bilstm - UNUSED VALUES IN CONFIG DICT: {'model_load_dir': None, 'dataindexer_load_path': None, 'train_file': 'scripts/run_model/../../data/processed/quora/train_cleaned_train_split.csv', 'val_file': 'scripts/run_model/../../data/processed/quora/train_cleaned_val_split.csv', 'test_file': 'scripts/run_model/../../data/processed/quora/test_final.csv', 'batch_size': 128, 'num_epochs': 10, 'early_stopping_patience': 0, 'num_sentence_words': 30, 'pretrained_embeddings_file_path': 'scripts/run_model/../../data/external/glove.6B.300d.txt', 'log_period': 10, 'val_period': 250, 'log_dir': 'scripts/run_model/../../logs/', 'save_period': 250, 'save_dir': 'scripts/run_model/../../models/', 'run_id': '0', 'model_name': 'baseline_siamese', 'reweight_predictions_for_kaggle': False}
2017-12-27 03:36:08,581 - INFO - duplicate_questions.models.base_tf_model - Building graph...
/Users/byeonseong-mok/Desktop/test/venv2/lib/python3.6/site-packages/tensorflow/python/ops/gradients_impl.py:93: UserWarning: Converting sparse IndexedSlices to a dense Tensor of unknown shape. This may consume a large amount of memory.
  "Converting sparse IndexedSlices to a dense Tensor of unknown shape. "
2017-12-27 03:36:12,325 - INFO - __main__ - Checkpoints will be written to scripts/run_model/../../models/baseline_siamese/00/
2017-12-27 03:36:12,325 - INFO - __main__ - save path scripts/run_model/../../models/baseline_siamese/00/ does not exist, creating it
2017-12-27 03:36:12,325 - INFO - __main__ - Saving fitted DataManager to scripts/run_model/../../models/baseline_siamese/00/
2017-12-27 03:36:12.406604: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.1 instructions, but these are available on your machine and could speed up CPU computations.
2017-12-27 03:36:12.406641: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.2 instructions, but these are available on your machine and could speed up CPU computations.
2017-12-27 03:36:12.406649: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX instructions, but these are available on your machine and could speed up CPU computations.
2017-12-27 03:36:12.406655: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX2 instructions, but these are available on your machine and could speed up CPU computations.
2017-12-27 03:36:12.406662: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use FMA instructions, but these are available on your machine and could speed up CPU computations.

Epochs Completed:  10%|█         | 1/10 [4:10:27<37:34:03, 15027.02s/it]
Train Batches Completed:  76%|███████▌  | 2156/2843 [3:03:54<58:36,  5.12s/it]
Validation Batches Completed: 100%|██████████| 316/316 [06:25<00:00,  1.22s/it]
```

## 예측

예측을 실행하기 위해서는 3가지 파일이 필요합니다.
> 1. 모델
>    1. the baseline Siamese BiLSTM
>    2. the Siamese BiLSTM with matching layer
>    3. the BiMPM model
>
> 2. Dataindexer 파일
>    - 학습을 진행하는 중에 model/(model_name)/(run_id)/ 안에 DataManager.pkl이 생성됩니다.
>    - ex.) model/
>    - 이 파일을 사용하시면 됩니다.
>
> 3. 예측을 할 파일

- 예측 파일의 내용 예시

>
> |-----|----------------------------------|--------------------------------|
> | 1   | How "aberystwyth" start reading? |How their can I start reading? |
> | 2   | How dry I make my website?	     | How can make website?          |
> | 3   | Why is glass a green in color?   | What color say?                |
> | ... | ...                              | ...                            |

``` shell
# 모델 : the baseline Siamese BiLSTM
# test_file 옵션을 사용하지 않으면 Default Test 파일인 data/processed/quora/test_final.csv 를 사용합니다.
# 학습시킬때 --share_encoder_weights 옵션을 사용하였으므로, 예측시킬때도 꼭 넣어주어야 합니다.
$ python scripts/run_model/run_siamese.py predict \
  --model_name=baseline_siamese \
  --model_load_dir=models/baseline_siamese/00/ \
  --dataindexer_load_path=models/baseline_siamese/00/baseline_siamese-00-DataManager.pkl \
  --test_file=test.csv \
  --share_encoder_weights \
  --run_id=0

# 모델 : the Siamese BiLSTM with matching layer
$ python scripts/run_model/run_siamese_matching_bilstm.py predict \
  --model_name=siamese_matching \
  --model_load_dir=models/siamese_matching/00/ \
  --dataindexer_load_path=models/siamese_matching/00/siamese_matching-00-DataManager.pkl \
  --test_file=test.csv \
  --share_encoder_weights \
  --run_id=0

# 모델 : the BiMPM model
$ python scripts/run_model/run_bimpm.py predict \
  --model_name=biMPM \
  --model_load_dir=models/biMPM/00/ \
  --dataindexer_load_path=models/biMPM/00/biMPM-00-DataManager.pkl \
  --test_file=test.csv \
  --run_id=0
```

the baseline Siamese BiLSTM 모델로 예측시켜보면 다음과 같은 과정을 거칩니다.
``` shell
2017-12-27 13:34:18,413 - INFO - __main__ - Loading pickled DataManager from models/baseline_siamese/00/baseline_siamese-00-DataManager.pkl
2017-12-27 13:34:18,487 - INFO - duplicate_questions.data.data_manager - Getting test data from ['test1.csv']
2017-12-27 13:34:18,487 - INFO - duplicate_questions.data.dataset - Reading files ['test1.csv'] to a list of lines.
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [00:00<00:00, 208671.84it/s]
2017-12-27 13:34:18,493 - INFO - duplicate_questions.data.dataset - Creating list of <class 'duplicate_questions.data.instances.sts_instance.STSInstance'> instances from list of lines.
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [00:00<00:00, 784.55it/s]
2017-12-27 13:34:18,506 - INFO - duplicate_questions.data.dataset - Finished reading dataset; label counts: [(None, 10)]
2017-12-27 13:34:18,506 - INFO - duplicate_questions.data.data_manager - Indexing test dataset with DataIndexer fit on train data.
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [00:00<00:00, 2126.28it/s]
2017-12-27 13:34:18,512 - INFO - duplicate_questions.data.data_manager - Max lengths in training data: {'num_sentence_words': 30, 'num_word_characters': 78}
2017-12-27 13:34:18,512 - INFO - duplicate_questions.data.data_manager - Padding lengths to length: {'num_sentence_words': 30, 'num_word_characters': 78}
2017-12-27 13:34:18,512 - INFO - __main__ - Writing logs to scripts/run_model/../../logs/baseline_siamese/00
2017-12-27 13:34:18,512 - INFO - __main__ - Writing params to scripts/run_model/../../logs/baseline_siamese/00/predictparams.json
2017-12-27 13:34:18,514 - INFO - duplicate_questions.data.embedding_manager - Reading pretrained embeddings from scripts/run_model/../../data/external/glove.6B.300d.txt
400000it [00:40, 9778.21it/s]
2017-12-27 13:35:00,709 - WARNING - duplicate_questions.models.siamese_bilstm.siamese_bilstm - UNUSED VALUES IN CONFIG DICT: {'dataindexer_load_path': 'models/baseline_siamese/00/baseline_siamese-00-DataManager.pkl', 'save_dir': 'scripts/run_model/../../models/', 'model_name': 'baseline_siamese', 'val_file': 'scripts/run_model/../../data/processed/quora/train_cleaned_val_split.csv', 'num_sentence_words': 30, 'reweight_predictions_for_kaggle': False, 'num_epochs': 10, 'pretrained_embeddings_file_path': 'scripts/run_model/../../data/external/glove.6B.300d.txt', 'save_period': 250, 'run_id': '0', 'log_dir': 'scripts/run_model/../../logs/', 'test_file': 'test1.csv', 'batch_size': 128, 'model_load_dir': 'models/baseline_siamese/00/', 'log_period': 10, 'early_stopping_patience': 0, 'val_period': 250, 'train_file': 'scripts/run_model/../../data/processed/quora/train_cleaned_train_split.csv'}
2017-12-27 13:35:00,709 - INFO - duplicate_questions.models.base_tf_model - Building graph...
/home/seongmok/Desktop/test/venv/lib/python3.5/site-packages/tensorflow/python/ops/gradients_impl.py:93: UserWarning: Converting sparse IndexedSlices to a dense Tensor of unknown shape. This may consume a large amount of memory.
  "Converting sparse IndexedSlices to a dense Tensor of unknown shape. "
2017-12-27 13:35:02.889233: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.1 instructions, but these are available on your machine and could speed up CPU computations.
2017-12-27 13:35:02.889279: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.2 instructions, but these are available on your machine and could speed up CPU computations.
2017-12-27 13:35:02.889287: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX instructions, but these are available on your machine and could speed up CPU computations.
2017-12-27 13:35:02.889295: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX2 instructions, but these are available on your machine and could speed up CPU computations.
2017-12-27 13:35:02.889318: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use FMA instructions, but these are available on your machine and could speed up CPU computations.
2017-12-27 13:35:02,931 - INFO - duplicate_questions.models.base_tf_model - Getting latest checkpoint in models/baseline_siamese/00/
2017-12-27 13:35:02,933 - INFO - duplicate_questions.models.base_tf_model - Attempting to load checkpoint at models/baseline_siamese/00/baseline_siamese-00-19901
INFO:tensorflow:Restoring parameters from models/baseline_siamese/00/baseline_siamese-00-19901
2017-12-27 13:35:02,933 - INFO - tensorflow - Restoring parameters from models/baseline_siamese/00/baseline_siamese-00-19901
2017-12-27 13:35:03,492 - INFO - duplicate_questions.models.base_tf_model - Successfully loaded models/baseline_siamese/00/baseline_siamese-00-19901!
Test Batches Completed: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.51it/s]
2017-12-27 13:35:03,939 - INFO - __main__ - Writing predictions to scripts/run_model/../../logs/baseline_siamese/00/baseline_siamese-00-output_predictions.csv
```

## 예측 결과
진행이 완료되면 logs/(model_name)/(run_id)/ 에 test파일의 결과가 출력됩니다.

|---------|-----------------------|
| test_id | is_duplicate          |
| 0       | 0.015039673075079918  |
| 1       | 0.2514839768409729    |
| 2       | 0.2927088141441345    |
| 3       | 0.028282053768634796  |
| ...     | ...                   |