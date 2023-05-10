#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 数据读取模块:读取生成的数据文件,然后数据写入数据库:mysql；读取完毕之后,删除文件
import os
import shutil
import struct
from datetime import datetime
import mysql.connector
import IdWorkers


# pip3 install mysql-connector-python

class DataReader:
    def __init__(self):
        self.filepath = "./origin_data"
        self.cnx = mysql.connector.connect(user='root', password='rbjf_DEV123',
                                           host='103.36.193.81',
                                           port='3306',
                                           database='ruoyi')
        self.cursor = self.cnx.cursor()

    def read_files(self):
        for filename in os.listdir(self.filepath):
            if filename.endswith(".bin"):
                filepath = os.path.join(self.filepath, filename)
                array, element, time_str, seq_num = self.parse_filename(filename)
                timestamp = self.parse_time(time_str)
                data = self.read_binary_file(filepath)
                print(type(data))

                seq_num = 1000
                data_status = 1
                join = ','.join(str(num) for num in data)
                # insert data into MySQL table
                query = ("INSERT INTO dp_origin_data (uid, site_id, device_id, collect_time, sample_rate, "
                         "data_status, infra_data) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s)")
                self.cursor.execute(query, (IdWorkers.nextId(), array, element, timestamp, seq_num, data_status, join))
                self.cnx.commit()
            # 删除文件
            try:
                os.remove(self.filepath + "/" + filename)
            except Exception as ex:
                print(f'ex:{ex} filename:{filename} filepath:{self.filepath}')
                try:
                    dst_dir = './origin_data_bak'
                    shutil.move(self.filepath + "/" + filename, dst_dir + "/" + filename)
                except Exception as ex2:
                    print(f'ex2:{ex2} filename:{filename} filepath:{self.filepath}')
                pass

        # 关闭数据库连接
        self.cursor.close()
        self.cnx.close()

    def parse_filename(self, filename):
        parts = filename.split(".")[0].split("_")
        array = parts[0]
        element = parts[1]
        time_str = parts[2]
        seq_num = parts[3]
        return array, element, time_str, seq_num

    def parse_time(self, time_str):
        return datetime.strptime(time_str, "%Y%m%d%H%M%S")

    def read_binary_file(self, filepath):
        data = []
        with open(filepath, "rb") as f:
            while True:
                bytes_read = f.read(4)
                if not bytes_read:
                    break
                val = struct.unpack("f", bytes_read)[0]
                data.append(val)
        return data


if __name__ == "__main__":
    reader = DataReader()
    reader.read_files()
