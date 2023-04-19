#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 噪音水平
import ctypes
import re


class NoiseLevelFunc:
    def __init__(self):
        self.so = ctypes.CDLL("./SOnoiseLevel.so")

    def noiseLevel(self, data):
        return self.so.noiseLevel(data)


def get_data():
    with open("./testWvfrm.txt", 'r') as f:
        data = f.readlines()
    # 将每行数据拆分为列表，并获取第一个元素组成新的列表
    pattern = re.compile(r' {2,3}')  # 使用正则表达式进行拆分
    return [re.split(pattern, line)[1] for line in data]


if __name__ == '__main__':
    func = NoiseLevelFunc()
    func.noiseLevel(get_data())
