from subprocess import Popen, PIPE, STDOUT
import os
import time


def _hms_format(seconds):
    return  time.strftime("%H:%M:%S", time.gmtime(seconds))

class FFmpeg(object):

    def __init__(self, input=None, output=None):
        self._input = input
        self._output = output

        self._subcmd = ""
        self._cmd = ""

    def _split(self, _from, _to):
        _ss = _hms_format(_from)
        _to = _hms_format(_to)

        _cmd = " -ss %s -to %s" % (_ss, _to)
        self._subcmd = _cmd

    def _audio(self, disable=False):
        if disable:
            self._subcmd += " -an"
        else:
            self._subcmd += " -strict -2"


    def _process(self, _cmd):
        _cmd = list(filter(None, _cmd.split(' ')))

        p = Popen(_cmd, stdin=PIPE, stderr=STDOUT)

        return p.communicate(input=b"y\n")


    def setSplit(self, _from, to, audioFlag=False):
        self._split(_from, to)
        self._audio(audioFlag)



    def setFile(self, input, output):
        self._input = input
        self._output = output

    def getCapture(self, _from=None, _to=None, _fps=1):
        self._subcmd = "-vf fps=%d -f image2" % (_fps)
        self._cmd = "ffmpeg -i %s %s %s" % (self._input, self._subcmd, self._output)

        print(self._cmd)
        out, err = self._process(self._cmd)



if __name__ == "__main__":
    proc = FFmpeg("teacher.mp4")
    proc.getCapture(10, 25, "image.png")