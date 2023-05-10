#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 方位角计算
# https://blog.csdn.net/qq_42455809/article/details/126226424
# https://zhuanlan.zhihu.com/p/145165873

# https://blog.csdn.net/Light_Travlling/article/details/103843506
import ctypes
from ctypes import *
import time
from MysqlDBUtils import MysqlDB
import IdWorkers
from CommonUtils import *
import numpy as np


# 自定义基类结构体
class SysParameters(Structure):
    _fields_ = [
        ("windowLen", c_float * 15),
        ("freqBins", c_float * 15),
        ("csThd", c_float * 15),
        ("corrThd", c_float * 15),
        ("sigma_A", c_float * 15),
        ("sigma_V", c_float * 15),

        ("sigma_F", c_float),
        ("sigma_T", c_float),
        ("timeThd", c_float),
        ("nFamilyMax", c_int),
        ("nFamilyMin", c_int),
        ("ThresholdDistance", c_float),

        ("VelocityMax", c_float),
        ("VelocityMin", c_float),
        ("freqHighLim", c_float * 15),
        ("freqLowLim", c_float * 15),
        ("overlapRate", c_float),
    ]


# 初始化结构体
sp = SysParameters((150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150),
                   (0.01, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0000),
                   (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                   (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
                   (20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20),
                   (0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2),
                   0.3,
                   20,
                   20,
                   1000,
                   2,
                   1.5,
                   1000,
                   200,
                   (50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50),
                   (0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01),
                   0.9)


class AzimuthCalFunc:

    def __init__(self):
        self.so = ctypes.CDLL("./SOAzimuthCalFunc.so")
        self.Azimuth = (c_float * 15)()
        self.Velocity = (c_float * 15)()
        self.Corrcoef = (c_float * 15)()
        self.nCHState = ctypes.pointer((c_int * 5)(1, 1, 1, 1, 1))
        self.nsigLen = c_int(15000)
        self.g_Fs = c_float(100)
        self.nDimMic = c_int(5)
        self.Resolution = c_float(0.01)
        pos_matrix = np.array([[998.8, 1284.5], [0, 0], [1460, -358.2], [1254, -130.1], [1254, -130.1]])
        self.Pos = ctypes.pointer(ndarray_to_ctype_array(pos_matrix, 5, 2))
        self.sp = sp

    def get_buffer(self):
        c_float_array = ((ctypes.c_float * 5) * 15000)()
        with open("../data/testWvfrm.txt", 'r') as f:
            readlines = f.readlines()
            for i in range(len(readlines)):
                line = readlines[i]
                ar = line.strip().split("   ")
                if len(ar) < 5:
                    tmp = line.strip().split("  ")
                else:
                    tmp = ar
                for j in range(len(tmp)):
                    c_float_array[i][j] = float(tmp[j])
        return c_float_array

    def AzimuthCalCallBack(self, buffer=None):

        if buffer is None:
            self.so.AzimuthCalCallBack(self.Azimuth, self.Velocity, self.Corrcoef, self.nCHState, self.sp,
                                       self.get_buffer(),
                                       self.nsigLen, self.g_Fs, self.nDimMic, self.Resolution, self.Pos)
        else:
            self.so.AzimuthCalCallBack(self.Azimuth, self.Velocity, self.Corrcoef, self.nCHState, self.sp,
                                       buffer,
                                       self.nsigLen, self.g_Fs, self.nDimMic, self.Resolution, self.Pos)


def get_data(db):
    # 1、定期从原始数据表获取数据
    results = db.select('SELECT infra_data FROM dp_origin_data where site_id=1 and (operate_status=0 or '
                        'operate_status is NULL) group by device_id')
    print(len(results))
    if len(results) == 0:
        return None
    # 定义二维数组
    c_float_array = ((ctypes.c_float * 5) * 15000)()
    # 遍历每行结果,添加到二维数组
    for row in results:
        # 将每一行数据按逗号切割
        arr = row[0].strip('[ ] \n').split(',')
        for i in range(5):
            # 添加数据到c_float数组
            for j in range(len(arr)):
                c_float_array[i][j] = ctypes.c_float(float(arr[i]))

    return c_float_array


def c_arr2str(c_arr):
    rs = ''
    for num in c_arr:
        rs += str(num) + ','
    return rs[:-1]


if __name__ == '__main__':
    # 1、定期从原始数据表获取数据
    db = MysqlDB('103.36.193.81', 3306, 'root', 'rbjf_DEV123', 'ruoyi')
    func = AzimuthCalFunc()
    while True:
        data = get_data(db)
        if data:
            func.AzimuthCalCallBack(data)
            for a in func.Azimuth:
                print(f'Azimuth: {a}')

            for a in func.Velocity:
                print(f'Velocity: {a}')

            for a in func.Corrcoef:
                print(f'corrcoef: {a}')

            azimuth_str = c_arr2str(func.Azimuth)
            velocity_str = c_arr2str(func.Velocity)
            corrcoef_str = c_arr2str(func.Corrcoef)

            # 更新操作
            # db.insert('INSERT INTO table (name) VALUES (%s)', ('John',))
            db.insert('INSERT INTO dp_single_array_event(sevent_id,site_id,azimuth,appa_speed,revelent) VALUES(%s,%s,'
                      '%s,%s,%s)', (IdWorkers.nextId(), '1', azimuth_str, velocity_str, corrcoef_str))
            db.update('UPDATE dp_origin_data SET operate_status=%s WHERE site_id=1', 1)

            # 暂停10秒
        time.sleep(10)
