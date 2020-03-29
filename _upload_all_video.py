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

sql = "SELECT V_ID FROM V_INFO;"

curs.execute(sql)
rows = curs.fetchall()

all_ids = []
for row in rows:
    all_ids.append(row[0])


from queue import Queue
from youtube.video2img import Video
from youtube.video2img import ThreadPool
from img2txt.Model import ImageFullCaption

CHECKPOINT_PATH="./img2txt/tf_data/model2.ckpt-3000000"
VOCAB_FILE="./img2txt/tf_data/word_counts_3.txt"

caption = ImageFullCaption(CHECKPOINT_PATH, VOCAB_FILE)
caption.init()

# Function to be executed in a thread
def videoNclip(*args):
    id = args[0]
    img_pool = args[1]

    vd = Video()
    if not os.path.isfile(os.path.join("videos", id)):
        url = "http://youtube.com/watch?v=" + id
        vd.setUrl(url)
        print("  비디오 다운로드 >>", vd.stream.default_filename)
        vd.download("videos")

    if not os.path.isdir(os.path.join("images", id)):
        vd.video_path = os.path.join("videos", id)
        vd.image_foldername = id

        print("  비디오 분할 >>", vd.stream.default_filename)
        vd.clip("images")
        img_pool.add_task(imgStarter, id)

    #########################
    img_pool.add_task(imgStarter, id)
    

def imgStarter(*args):
    video_id = args[0]

    base_path = os.path.join("images", video_id)
    listdir = os.listdir(base_path)

    curs_i = 0
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
            print("commited")

    db_conn.commit()



# Pool count = 3
video_pool = ThreadPool(3)

# processed Video ID
image_pool = ThreadPool(1)


for id in all_ids:
    print(id)
    video_pool.add_task(videoNclip, id, image_pool)

video_pool.wait_completion()
image_pool.wait_completion()

