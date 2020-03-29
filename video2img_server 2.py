import socket,os

from queue import Queue
from youtube.video2img import Video
from youtube.video2img import ThreadPool

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


def imgStarter(id):
    cs = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    cs.connect("./_im2txt")
    cs.send(id.encode('utf-8'))
    cs.close()

print("VIDEO2IMAGE SERVER READY")
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("./_video2img")
except OSError:
    pass
s.bind("./_video2img")
s.listen(1)

# Pool count = 3
video_pool = ThreadPool(3)

# processed Video ID
image_pool = ThreadPool(1)


while 1:
    conn, addr = s.accept()
    data = conn.recv(1024)

    id = data.decode()
    video_pool.add_task(videoNclip, id, image_pool)

conn.close()
