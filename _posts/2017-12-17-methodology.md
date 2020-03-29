---
layout: post
title: "2. 방법론"
description: 이 주제에 대해 조사해보니 Image를 자동으로 Caption을 만들어내는 'Show and Tell'이란 연구결과와 두 문장의 유사성을 측정하는 'Manhattan LSTM' 모델을 알게 되었습니다.
tag: capstone
---

### 전제조건

사실 인터넷 상에서 무수하게 생겨나는 모든 동영상을 찾는다는 것은 Google과 같은 전문 기업이 아니면 거의 불가능하다고 생각합니다. 그리고 자신이 본 동영상을 찾는다는 것은 그 동영상을 이미 보았다는 선행조건이 필요합니다. 지도교수님께서도 그런 문제를 지적하시면서 'YouTube의 History'를 활용하는 것을 권유하셨습니다.

<br>

### 자료조사
1. [Show and Tell](https://research.googleblog.com/2016/09/show-and-tell-image-captioning-open.html)
- Google Brain team의 연구자들이 기계학습을 통해 이미지에서 자동으로 캡션을 만들어내었다는 기사입니다.
2. [Manhattan LSTM Model](https://www.quora.com/What-is-Manhattan-LSTM)
- 두 문장을 비교하여 유사성을 측정하는 여러가지 모델 중 하나입니다.

<br>

### 개발환경

| ------ | ---------------- |
| **OS** | Ubuntu 16.04 LTS |
| **언어** | Python |
| **라이브러리** | TensorFlow |
