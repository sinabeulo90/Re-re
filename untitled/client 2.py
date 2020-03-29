# Echo client program
import socket
import pickle
import json
import pprint

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("203.237.183.58", 7162))
s.sendall(b"message")

msg = s.recv(1024)
print(type(msg))
msg = msg.decode()
pprint.pprint(json.loads(msg))
print(type(msg))
# size = s.recv()
# size = int(size.decode())

# print("size", size)

# data = b""
# while len(data) < size:
# 	print(len(data), size)

# 	read_size = size - len(data)
# 	data += s.recv(4096 if read_size > 4096 else read_size)

# print(len(data), size)

# s.sendall(b"00")

# s.close()

# print('Received ', pickle.loads(data))
