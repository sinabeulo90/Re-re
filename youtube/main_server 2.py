import socket,os

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("./_main")
except OSError:
    pass
s.bind("./_main")
s.listen(1)

while 1:
    conn, addr = s.accept()
    data = conn.recv(1024)

    if data == "COOKIE":
        # 1. 히스토리 정보 수집단계
        # 2. 비디오 -> 이미지 처리 (OK)
        # 3. 이미지 -> 번역 처리 
        print("COOKIE")
    
    elif data == "SEARCH":
        print("SEARCH")
	
    if not data: break
    conn.send(data)

conn.close()
