#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 方位角计算
# https://blog.csdn.net/qq_42455809/article/details/126226424
# https://zhuanlan.zhihu.com/p/145165873

# https://blog.csdn.net/Light_Travlling/article/details/103843506
import ctypes
from ctypes import *
import numpy as np
import time
from MysqlDBUtils import MysqlDB
from RedisUtil import RedisClient


# so = ctypes.CDLL("./SOAzimuthCalFunc.so")

def print_ctypes_array(arr, file_name):
    c_arr = (ctypes.c_float * (len(arr) * len(arr[0])))(*np.ravel(arr).astype(np.float32))
    # 将c_float类型的二维数组转换成NumPy数组
    np_arr = np.ctypeslib.as_array(c_arr).reshape((len(arr), len(arr[0])))
    # 以矩阵形式输出c_float二维数组
    np.savetxt(file_name, np_arr, fmt="%.2f", delimiter=" ")


# 调用此函数
Azimuth = (c_float * 15)()
Velocity = (c_float * 15)()
corrcoef = (c_float * 15)()
nCHState = (c_int * 5)()
nsigLen = c_int(15000)
g_Fs = c_float(100)
nDimMic = c_int(5)
Resolution = c_float(100)
Pos = ((ctypes.c_float * 2) * 5)()


# 自定义基类结构体
class SysParameters(Structure):
    _fields_ = [
        ("windowLen", c_float * 15),
        ("freqBins", c_float * 15),
        ("csThd", c_float * 15),
        ("corrThd", c_float * 15),
        ("sigma_A", c_float * 15),
        ("sigma_V", c_float * 15),
        ("sigma_T", c_float),
        ("timeThd", c_float),
        ("nFamilyMax", c_int),
        ("nFamilyMin", c_int),
        ("ThresholdDistance", c_float),
        ("VelocityMax", c_float),
        ("VelocityMin", c_float),
        ("sigma_V", c_float * 15),
        ("sigma_V", c_float * 15),
        ("overlapRate", c_float),
    ]


# 初始化结构体
sp = SysParameters((150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150),
                   (0.01, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0000),
                   (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                   (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),
                   (20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20),
                   (0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2),
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


class FamilyClusterFunc:
    def __init__(self, OutputAV, matrixA, matrixV, matrixC):
        self.so = ctypes.CDLL("./SOFamilyClusterFunc.so")
        self.OutputAV = OutputAV
        self.matrixA = matrixA
        self.matrixV = matrixV
        self.matrixC = matrixC
        self.nLineNumTime = c_int(60)
        self.nColumnNumFreq = c_int(15)
        self.nTimeStep = c_float(10)
        self.Fs = c_float(100)
        self.structParameter2 = sp

    def ArrayFamilyForm(self):
        self.so.ArrayFamilyForm(self.OutputAV, self.matrixA, self.matrixV,
                                self.matrixC, self.nLineNumTime, self.nColumnNumFreq,
                                self.nTimeStep, self.Fs, self.structParameter2)

    def get_OutputAV(self):
        return self.OutputAV


if __name__ == '__main__':
    while True:
        m = 15
        n = 60

        # 从redis队列中获取矩阵

        # 将矩阵转换成c_float类型的二维数组
        matrixA = (ctypes.c_float * (m * n))(*np.ravel(azimuth_matrix).astype(np.float32))
        matrixV = (ctypes.c_float * (m * n))(*np.ravel(velocity_matrix).astype(np.float32))
        matrixC = (ctypes.c_float * (m * n))(*np.ravel(corrcoef_matrix).astype(np.float32))

        # 使用reshape函数将一维数组转换成二维数组
        matrixA = np.ctypeslib.as_array(matrixA).reshape((m, n))
        matrixV = np.ctypeslib.as_array(matrixV).reshape((m, n))
        matrixC = np.ctypeslib.as_array(matrixC).reshape((m, n))

        # 2、PMCC计算
        FamilyClusterFunc(OutputAV, matrixA, matrixV, matrixC)

        # 数据打印
        print_ctypes_array(OutputAV, "../output.txt")

        c_OutputAV_arr = (ctypes.c_float * (len(OutputAV) * len(OutputAV[0])))(*np.ravel(OutputAV).astype(np.float32))
        # 将c_float类型的二维数组转换成NumPy数组
        np_OutputAV_arr = np.ctypeslib.as_array(c_OutputAV_arr).reshape((len(OutputAV), len(OutputAV[0])))

        db.update("UPDATE dp_single_array_event set matrixA=%s,matrixV=%s,matrixC=%s,matrixAV=%s", (matrixA, matrixV,
                                                                                                    matrixC,
                                                                                                    np_OutputAV_arr))
        # 暂停10秒
        time.sleep(100)
