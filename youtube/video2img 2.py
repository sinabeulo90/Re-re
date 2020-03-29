import os
import re

from pytube import YouTube
from youtube.FFmpeg import FFmpeg

re_patt = r'.*\/watch\?v=(.*)[&]?.*'
re_patt2 = r'(&t=.*)'

class Video():

    yt = None

    def setUrl(self, url):
        if self.yt is not None:
            del self.yt

        self.yt = YouTube(url)

        self.stream = self.yt.streams.filter(progressive=True).first()
        
        self.image_foldername = re.match(re_patt, url).group(1)
        rm_str = re.search(re_patt2, self.image_foldername)
        if rm_str:
            self.image_foldername = self.image_foldername.replace(rm_str.group(1), "")

        self.filename = self.image_foldername
        self.fps = self.stream.fps


    def download(self, path):
        if path is None:
            self.stream.download()

        else:
            if os.path.isdir(path) is False:
                os.mkdir(path)

            self.stream.download(path)
            self.video_path = os.path.join(path, self.filename)

            os.rename(os.path.join(path, self.stream.default_filename), self.video_path)

    def clip(self, path):
        images_folder = os.path.join(path, self.image_foldername)
        if os.path.isdir(images_folder) is False:
            os.makedirs(images_folder)

        proc = FFmpeg(self.video_path, os.path.join(images_folder, "%04d.png"))
        proc.getCapture(_fps=1)


from queue import Queue
from threading import Thread

class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()

class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()



if __name__ == "__main__":
    # url = "http://youtube.com/watch?v=9bZkp7q19f0"
    # vd = Video()
    # vd.setUrl(url)
    # vd.download("videos")
    # vd.clip("images")

    from random import randrange
    from time import sleep

    # Function to be executed in a thread
    def videoNclip(id):
        url = "http://youtube.com/watch?v=" + id
        print(url)

        vd = Video()
        vd.setUrl(url)
        vd.download("videos")
        vd.clip("images")

    # Generate random delays
    delays = [randrange(3, 7) for i in range(50)]

    # Instantiate a thread pool with 5 worker threads
    pool = ThreadPool(5)

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    pool.map(videoNclip, delays)
    pool.wait_completion()
