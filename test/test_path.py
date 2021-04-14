import pymysql
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

# MySQL Connection 연결
db_conn = pymysql.connect(host='localhost', user='root', password='tkfkdgo0!!', db='Rere', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = db_conn.cursor()
sql = "SELECT V_DETAIL.V_ID, V_TITLE, V_TIME FROM V_DETAIL JOIN V_INFO ON V_INFO.V_ID = V_DETAIL.V_ID AND (V_TIME LIKE '%25');"
curs.execute(sql)
rows = curs.fetchall()
print(str(formatting_result(rows)).encode('utf-8'))
