import socket,os
import pymysql

# MySQL Connection 연결
db_conn = pymysql.connect(host='localhost', user='root', password='tkfkdgo0!!', db='Rere', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = db_conn.cursor()
curs_i = 0

from img2txt.Model import ImageFullCaption

CHECKPOINT_PATH="./img2txt/tf_data/model2.ckpt-3000000"
VOCAB_FILE="./img2txt/tf_data/word_counts_3.txt"

caption = ImageFullCaption(CHECKPOINT_PATH, VOCAB_FILE)
caption.init()

print("IMAGE2TXT SERVER READY")
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("./_im2txt")
except OSError:
    pass
s.bind("./_im2txt")
s.listen(1)

while 1:
    conn, addr = s.accept()
    data = conn.recv(1024)

    video_id = data.decode('utf-8')

    sql = "SELECT COUNT(*) FROM V_DETAIL WHERE V_ID LIKE '%s';" % (video_id)
    curs.execute(sql)
    row = curs.fetchone()

    if row[0] != 0:
        continue

    base_path = os.path.join("images", video_id)
    listdir = os.listdir(base_path)

    inserted_description = ""
    for filename in listdir:
        path = os.path.join(base_path, filename)
        captions_result = caption.run(path)

        v_id = video_id
        v_time = int(filename.split(".")[0])
        v_description = db_conn.escape(captions_result[0])
        
        if inserted_description != v_description:
            sql = "INSERT INTO V_DETAIL(V_ID, V_TIME, V_DESCRIPTION) VALUES ('%s', %d, %s);" % (v_id, v_time, v_description)
            inserted_description = v_description
        
            curs.execute(sql)
        
            curs_i += 1

        if curs_i % 100 == 0:
            db_conn.commit()

    db_conn.commit()


conn.close()
