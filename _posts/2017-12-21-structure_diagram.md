---
layout: post
title: "6. 시스템 구조도"
description : 지금까지 구현한 코드를 모두 종합하여 기능을 구현해봅시다. 재료는 이미지와 임의의 문장입니다. 이미지를 입력하면 im2txt에서 Caption을 만들어내고 이를 임의의 문장와 비교해보기 위해 시스템의 구조를 간단히 만들어보겠습니다.
tag: capstone
---

지금까지 im2txt를 통해 이미지에서 Caption을 뽑아내어 문장을 얻어 내었고, Manhattan LSTM으로 서로 다른 문장의 연관성을 수치화해보았습니다.
이 모든 과정에서 Python3를 사용했으므로, 시스템의 구현도 마찬가지로 같은 언어를 사용하려고 합니다.
저희의 시스템은 크게 4가지의 기능으로 나뉩니다.

주요 기능
---

![diagram]({{ site.assets | absolute_url }}/capstone/6_diagram.png)

> (A) YouTube에서 사용자의 History 기록을 수집
>
> (B) 동영상 다운로드 및 이미지 분할
>
> (C) 분할이 완료된 이미로부터 Caption
>
> (D) Caption과 임의의 문장의 연관성을 수치화합니다.

프로세스 문제
---

최소 4개의 서버 프로세스가 필요했고. 우선은 컴퓨터 한대에서 모든 과정을 진행하였습니다.

> (A) -> (B) -> (C) -> (D)

각 프로세스마다 서버와 클라이언트 역할을 동시에 진행합니다.
한 대의 컴퓨터에서 모든 작업이 일어나기 때문에 연산량이 특히나 많은 (C), (D)의 작업은 더뎌지는 것은 당연했습니다.

데이터베이스
---

데이터베이스 테이블은 동영상의 기본 정보를 지니는 V_INFO 테이블과 좀더 세부적인 정보를 내포하는 V_DETAIL 테이블을 사용하였습니다.

- V_INFO

| Field   | Type      | Null | Key | Default | Extra |
|---------|-----------|------|-----|---------|-------|
| V_ID    | char(255) | NO   | PRI | NULL    |       |
| V_TITLE | text      | YES  |     | NULL    |       |

- V_DETAIL

| Field         | Type      | Null | Key | Default | Extra |
|---------------|-----------|------|-----|---------|-------|
| V_ID          | char(255) | NO   | PRI | NULL    |       |
| V_TIME        | int(8)    | NO   | PRI | NULL    |       |
| V_DESCRIPTION | text      | YES  |     | NULL    |       |
