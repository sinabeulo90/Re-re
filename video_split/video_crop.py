# -*- coding: utf-8 -*-
"""
Video Spliter from start time to end time.
"""
from subprocess import Popen, PIPE, STDOUT
import argparse
import time
import sys

def hms_format(seconds):
    return  time.strftime("%H:%M:%S", time.gmtime(seconds))

parser = argparse.ArgumentParser(description="Video Spliter from start time to end time.",
                                 usage="%s [-h] INPUT_FILENAME OUTPUT_FILENAME FROM TO [--a]" % (sys.argv[0]))

# Required
parser.add_argument("INPUT_FILENAME", type=str, help="Input filename")
parser.add_argument("OUTPUT_FILENAME", type=str, help="Output filename")
parser.add_argument("FROM", type=int, help="From start")
parser.add_argument("TO", type=int, help="To end")

# Options
parser.add_argument("-an", default=True, action='store_false', help="Disable audio recording")


args = parser.parse_args()
print(args)

input_filename = args.INPUT_FILENAME
output_filename = args.OUTPUT_FILENAME

start_time = hms_format(args.FROM)
end_time = hms_format(args.TO)


is_audio = args.an

if is_audio:
    ffmpeg_cmd = 'ffmpeg -i %s -ss %s -to %s -strict -2 %s'
    
else:
    ffmpeg_cmd = 'ffmpeg -i %s -ss %s -to %s -an %s'
    
    
ffmpeg_cmd = ffmpeg_cmd % (input_filename, start_time, end_time, output_filename)

print(ffmpeg_cmd)
ffmpeg_cmd = ffmpeg_cmd.split(' ')



p = Popen(ffmpeg_cmd, stdin=PIPE, stderr=STDOUT)
out, err = p.communicate(input=b"y\n")

print("EOE")