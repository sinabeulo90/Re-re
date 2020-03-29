import socket
import sys

from txt2predict import run_siamese
import pymysql
import pickle

SiameseBiLSTM_init, SiameseMatchingBiLSTM_init = run_siamese.init()

# MySQL Connection 연결
db_conn = pymysql.connect(host='localhost', user='root', password='tkfkdgo0!!', db='Rere', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = db_conn.cursor()

def formatting_result(rows):
    formated_data = []

    base_id = rows[0][0]
    base_title = rows[0][1]
    seconds = []

    for row in rows:
        id = row[0]
        title = row[1]
        second = row[2]

        if base_id != id:
            formated_data.append({"id": base_id, "seconds": seconds, "title": base_title})
            seconds = []

            base_id = id
            base_title = title
        seconds.append(second)
    formated_data.append({"id": base_id, "seconds": seconds, "title": base_title})

    return formated_data



def formatting_pretty_result(rows):
    formated_data = []

    base_id = rows[0][0]
    base_title = str(rows[0][1])
    seconds = []

    for row in rows:
        id = row[0]
        title = row[1]
        second = str(row[2])

        URL = "http://youtube.com/watch?v=" + id

        if base_id != id:
            formated_data.append({"URL": URL, "seconds": seconds, "title": base_title})
            seconds = []

            base_id = id
            base_title = title
        seconds.append(URL + "&t=" + second)
    formated_data.append({"URL": base_id, "seconds": seconds, "title": base_title})

    return formated_data


HOST = ""
PORT = 9999
config = (HOST, PORT)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(config)
serverSocket.listen(1)

print("DESCRIPTION PREDICT SERVER READY")

print ('tcp server :: server wait...')
percent = 0.7
while True:
    connection, clientAddress = serverSocket.accept()
    print ("tcp server :: connect :", clientAddress)

    message = ""
    while True:
        data = connection.recv(1024).decode()
        message += data

        if not data or len(data) < 1024:
            break

    predict_result = []
    predict_result += run_siamese.predict(message, SiameseBiLSTM_init, percent)
    predict_result += run_siamese.predict(message, SiameseMatchingBiLSTM_init, percent)

    if len(predict_result) == 0:
        connection.send("No Result")
    elif len(predict_result) == 1:
        sql = "SELECT V_DETAIL.V_ID, V_TIME FROM V_DETAIL JOIN V_INFO ON V_INFO.V_ID = V_DETAIL.V_ID AND V_DESCRIPTION LIKE '%s'" % predict_result[0];
    else:
        sub_sql = "V_DESCRIPTION LIKE %s" % db_conn.escape(predict_result[0])
        for result in predict_result[1:]:
            sub_sql += "OR V_DESCRIPTION LIKE %s" % db_conn.escape(result)
        sql = "SELECT V_DETAIL.V_ID, V_TITLE, V_TIME FROM V_DETAIL JOIN V_INFO ON V_INFO.V_ID = V_DETAIL.V_ID AND (%s)" % sub_sql

    curs.execute(sql)
    rows = curs.fetchall()
    
    formatted_data = str(formatting_pretty_result(rows)).encode()
    with open("dump", "wb") as f:
        f.write(formatted_data)

    length = str(len(formatted_data)).zfill(8).encode()

    connection.sendall(length)
    connection.sendall(formatted_data)

    # b"00" 을 전달받을 때 클라이언트는 전송 완료
    end = connection.recv(2)
    print(end)
    connection.close()
