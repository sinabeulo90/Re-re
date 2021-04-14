import socket,os

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("./socketname")
except OSError:
    pass
s.bind("./socketname")
s.listen(1)
while 1:
	conn, addr = s.accept()
	data = conn.recv(1024)
	if not data: break
	conn.send(data)
conn.close()
