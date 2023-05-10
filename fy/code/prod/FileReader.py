#! /usr/bin/env python
# -*- coding=utf-8 -*-
import os
import numpy as np


class FileReader:
    def __init__(self, dir_path, window_size=10, sample_freq=100):
        self.dir_path = dir_path  # 数据目录路径
        self.window_size = window_size  # 滑动窗口大小,秒
        self.sample_freq = sample_freq  # 每秒采样频率

        # 初始化Buffer,每个Buffer对应一个阵元,大小为window_size*sample_freq
        self.buffer1 = np.empty((window_size * sample_freq, 1))
        self.buffer2 = np.empty((window_size * sample_freq, 1))
        self.buffer3 = np.empty((window_size * sample_freq, 1))
        self.buffer4 = np.empty((window_size * sample_freq, 1))
        self.buffer5 = np.empty((window_size * sample_freq, 1))

    def read_files(self, date):
        # 获取给定日期文件夹下所有bin文件
        file_path = os.path.join(self.dir_path, date)
        file_list = os.listdir(file_path)
        file_list = [f for f in file_list if f.endswith('.bin')]

        # 解析文件名,读取数据并添加到Buffer
        for f in file_list:
            sensor_id = int(f.split('_')[0][1:])  # 获取阵元ID

            # 打开文件并读取数据
            with open(os.path.join(file_path, f), 'rb') as fr:
                data = np.fromfile(fr, dtype=np.int16)

                # 添加到对应Buffer并更新,移除最早window_size秒的数据
            if sensor_id == 1:
                self.buffer1 = np.hstack((self.buffer1, data.reshape(-1, 1)))
                if len(self.buffer1) > self.window_size * self.sample_freq:
                    self.buffer1 = self.buffer1[:, self.sample_freq * self.window_size:]
            ...

        # 合并Buffer生成15000x5的矩阵并返回
        return np.hstack((self.buffer1, self.buffer2, ..., self.buffer5))

