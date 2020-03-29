import socket,os
import pymysql

# MySQL Connection 연결
db_conn = pymysql.connect(host='localhost', user='root', password='tkfkdgo0!!', db='Rere', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = db_conn.cursor()

print("SEARCH SERVER READY")
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("./_search")
except OSError:
    pass
s.bind("./_search")
s.listen(1)

while 1:
    conn, addr = s.accept()

    sentence = ""
    while 1:
        data = conn.recv(1024)
        sentence += data.decode('utf-8')

        if len(data) < 1024:
            break
    
    sql = "SELECT DISTINCT V_DESCRIPTION FROM V_DETAIL;"
    curs.execute(sql)
    rows = curs.fetchall()

    for row in rows:
        v_sentence = row[0]
        print(v_sentence)


conn.close()
