# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

import pymysql
import re
import json
import socket

re_patt = r'.*\/watch\?v=(.*)'

global conn, curs, curs_i, s
# MySQL Connection 연결
conn = pymysql.connect(host='localhost', user='root', password='tkfkdgo0!!', db='Rere', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = conn.cursor()
curs_i = 0

class CleanUpHistoryEntriesPipeline(object):
    def proccess_items(self, item, spider):
        item['vid'] = item['vid'].replace('/watch?v=', '')
        # item['author_id'] = item['author_id'].replace('/user/', '')
        # item['author_id'] = item['author_id'].replace('/channel/', '')
        return item

class ConvertVideoTimePipeline(object):
    def process_item(self, item, spider):
        item['time'] = self.convert_time(item['time'])
        return item

    def convert_time(self, tstring):
        seconds, minutes, hours = None, None, None
        total_seconds = 0
        t_components = tstring.strip().split(':')
        for i, comp in enumerate(reversed(t_components)):
            if i == 0:
                seconds = int(comp)
                total_seconds = seconds
            if i == 1:
                minutes = int(comp)
                total_seconds += minutes * 60
            if i == 2:
                hours = int(comp)
                total_seconds += hours * 3600
        return total_seconds

class DbOutputPipeline(object):
    def __init__(self, *args, **kwargs):
        super(DbOutputPipeline, *args, **kwargs)
        # from youtube_history import db_api
        # self.db = db_api.AppDatabase();

    def process_item(self, item, spider):
        keys = ["vid", "author_id", "title", "description", "time"]
        args = []
        for k in keys:
            args.append(item[k])

        global conn, curs, curs_i
        v_id = re.match(re_patt, item["vid"]).group(1)
        v_title = conn.escape(item["title"])

        sql = "INSERT IGNORE V_INFO (V_ID, V_TITLE) VALUES (%s, %s);" % (conn.escape(v_id), v_title)
        
        curs.execute(sql)
        curs_i += 1

        if curs_i % 100 == 0:
            conn.commit()

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect("../_video2img")
        s.send(v_id.encode())
        s.close()

        return item