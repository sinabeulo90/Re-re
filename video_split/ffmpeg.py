from subprocess import Popen, PIPE, STDOUT
import time


def _hms_format(seconds):
    return  time.strftime("%H:%M:%S", time.gmtime(seconds))

class ffmpeg(object):

    def __init__(self, input=None, output=None):
        self._input = input
        self._output = output

        self._subcmd = ""
        self._cmd = ""

    def _split(self, _from, _to):
        _ss = _hms_format(_from)
        _to = _hms_format(_to)

        _cmd = " -ss %s -to %s" % (_ss, _to)
        self._subcmd += _cmd

    def _audio(self, disable=False):
        if disable:
            self._subcmd += " -an"
        else:
            self._subcmd += " -strict -2"


    def _process(self, _cmd):
        _cmd = list(filter(None, _cmd.split(' ')))
        print("!!!!!!!!!!!!!!!!!!!!!", _cmd)

        p = Popen(_cmd, stdin=PIPE, stderr=STDOUT)

        return p.communicate(input=b"y\n")


    def setFile(self, input, output):
        self._input = input
        self._output = output

    def sefInput(self, input):
        self._input = input

    def setOutput(self, output):
        self._output = output

    def run(self):
        self._audio()
        self._cmd = "ffmpeg -i %s %s %s" % (self._input, self._subcmd, self._output)

        out, err = self._process(self._cmd)
        if out:
            print(out)
            print("EOE")
        else:
            print(err)
            print("Error")



if __name__ == "__main__":
    proc = ffmpeg("teacher.mp4", "clip.mp4")
    proc._split(10, 20)
    proc.run()
