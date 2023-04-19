#! /usr/bin/env python
# -*- coding=utf-8 -*-
# mysql数据库工具类

import pymysql


class MysqlDB:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def insert(self, sql, params):
        self.connect()
        self.cursor.execute(sql, params)
        self.conn.commit()
        self.close()

    def select(self, sql, params=None):
        self.connect()
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        self.close()
        return result

    def update(self, sql, params):
        self.connect()
        self.cursor.execute(sql, params)
        self.conn.commit()
        self.close()

    def delete(self, sql, params):
        self.connect()
        self.cursor.execute(sql, params)
        self.conn.commit()
        self.close()
