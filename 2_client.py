# Echo client program
import socket
import pickle
import json
import ast
import pprint
# "a cat sitting on top of a bathroom sink."

import sys
txt = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("", 9999))
s.sendall(txt.encode())

length = int(s.recv(8).decode())

msg = b""
while len(msg) < length:
    remain_length = length - len(msg)
    msg += s.recv(1024 if remain_length < 1024 else remain_length+1)

msg = msg.decode()

pprint.pprint(ast.literal_eval(msg))

s.sendall(b"00")
s.close()
