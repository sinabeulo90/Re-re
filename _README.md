쿠키작업 관련

Environment : tensorflow (~/.conda_tf)
1. 쿠키 (작업중)

2. DB에서 id 값을 통해서 비디오를 다운받고, 이미지를 분할
python video2img_server.py

3. 이미지를 분석하고 DB의 V_DETAIL 테이블에 입력
python im2txt_server.py


겁색 관련 작업

Environment : python3 (~/.conda_py3)
1. client에게서 입력을 받아서, 분석한뒤 결과를 client에 전송
python txt2predict_server.py
