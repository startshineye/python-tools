#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 读取bin文件数据,每10秒生成一个文件,数据拼接上一些信息: 台阵、阵元、开始时间
import time
import numpy as np
import struct
import os
import datetime


class DataAcquisition:
    def __init__(self, file_names,now_time):
        self.file_names = file_names
        self.now_time = now_time

    def read_files(self):
        for file_name in self.file_names:
            with open(file_name, 'rb') as f:
                data = f.read()
            num_samples = len(data) // 4  # 每个float32类型占4个字节
            num_chunks = num_samples // 1000
            for i in range(num_chunks):
                start = i * 1000 * 4
                end = (i + 1) * 1000 * 4
                chunk_data = data[start:end]
                chunk = struct.unpack('1000f', chunk_data)
                # 添加台阵、阵元、时间信息
                # ...
                # 保存到新文件
                ten_seconds_later = now + datetime.timedelta(seconds=((i + 1) * 10))
                time_for = ten_seconds_later.strftime("%Y%m%d%H%M%S")
                new_file_name = '.' + file_name.split('.')[1].replace('acquire_data', 'origin_data') + '_' + str(time_for) + '_' + str(i + 1) + '.bin'
                with open(new_file_name, 'wb') as f:
                    f.write(chunk_data)
                print('Saved {} samples to {}'.format(len(chunk), new_file_name))


if __name__ == '__main__':
    now = datetime.datetime.now()
    da = DataAcquisition(['./acquire_data/01_A0.bin', './acquire_data/01_B1.bin', './acquire_data/01_B2.bin',
                          './acquire_data/01_B3.bin'] , now)
    da.read_files()

