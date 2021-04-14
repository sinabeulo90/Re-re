import pymysql

# MySQL Connection 연결
db_conn = pymysql.connect(host='localhost', user='root', password='tkfkdgo0!!', db='Rere', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = db_conn.cursor()

sql = "SELECT V_DETAIL.V_ID, V_TITLE, V_TIME FROM V_DETAIL JOIN V_INFO ON V_INFO.V_ID = V_DETAIL.V_ID LIMIT 10";

curs.execute(sql)
rows = curs.fetchall()

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

import ast
import pprint
pprint.pprint(ast.literal_eval(str(formatting_pretty_result(rows))))