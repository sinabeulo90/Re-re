---
layout: post
title: "3. 기본준비"
description: 이 프로젝트를 진행하기 위해선 기본적으로 Python 모듈인 pip, virtualenv, tensorflow을 설치해야 하고 Github의 TensorFlow Models를 다운받아야 합니다.
tag: capstone
---

1. [pip 설치](#1-pip-설치)
2. [virtualenv 설치](#2-virtualenv-설치)
3. [tensorflow 설치](#3-tensorflow-설치)

### 1. pip 설치

- pip는 Python 패키지를 설치하고 관리해주는 시스템입니다.

	``` shell
	$ sudo apt-get update
	$ sudo apt-get upgrade

	$ wget https://bootstrap.pypa.io/get-pip.py
	$ python3 get-pip.py
	$ rm get-pip.py

	$ pip3 install --upgrade pip3
	```

<br>

### 2. virtualenv 설치

- Python의 가상환경을 만들어서 시스템의 Python 환경과 독립적인 환경을 제공해주는 툴입니다.
- 각 프로젝트마다 고유의 환경을 만들어 줄수 있고, 패키지 설치 중 오류나 그 이외에 오류에도 시스템의 환경에 영향을 막아줌으로써, 쓸데없는 골칫거리를 방지해줍니다.

	``` shell
	# 설치
	$ sudo pip install virtualenv

	# Python3 의 가상환경 생성 	# Python2 일 경우
	$ virtualenv -p python3 venv 	# virtualenv -p python  venv

	# 가상환경 적용
	$ source venv/bin/activate

	# venv의 가상환경이 적용됐음을 의미합니다.
	(venv)$
	```

<br>

### 3. tensorflow 설치

- tensorflow는 CPU 버전과 GPU 버전을 제공하는데, 현재는 GPU는 제한된 그래픽 카드에서만 지원하고 있다. 여기서는 CPU 버전만 설치합니다.
- GPU의 경우 이전버전과 다르게 설치가 많이 간소화되었는데, 그래도 몇몇 파일을 다운받아야 합니다. 자세한 사항들은 [NVIDIA requirements to run TensorFlow with GPU support](https://www.tensorflow.org/install/install_linux)를 참고하길 바랍니다.

	``` shell
	(venv)$ pip install -U tensorflow

	# 확인을 위해 Python을 실행
	(venv)$ python
	```

	``` python
	import tensorflow as tf

	hello = tf.constant('Hello, TensorFlow!')
	sess = tf.Session()
	print(sess.run(hello))

	# 결과가 나오면 잘 설치된 것입니다.
	# b'Hello, TensorFlow!'
	```

