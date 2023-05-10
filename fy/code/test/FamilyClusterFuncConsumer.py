#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 事件检测消费者模块: 根据对应的矩阵数据，调用FamilyClusterFunc检测出事件，保存到mysql中
import ctypes
from ctypes import *
import numpy as np
import time
from MysqlDBUtils import MysqlDB
from RedisUtil import RedisClient
from CommonUtils import *

redis_key_azimuth_matrix = 'azimuth_matrix'
redis_key_velocity_matrix = 'velocity_matrix'
redis_key_corrcoef_matrix = 'corrcoef_matrix'


def get_matrix_from_redis(redis_client, key):
    result = redis_client.get_matrix(key)
    if result is None:
        # r-15 c-600
        return np.zeros((15, 600))
    return result


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
                   (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),
                   (20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
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
        self.so.ArrayFamilyForm(self.OutputAV, self.matrixA, self.matrixV, self.matrixC, self.nLineNumTime,
                                self.nColumnNumFreq,
                                self.nTimeStep, self.Fs,
                                self.structParameter2)

    def get_OutputAV(self):
        return self.OutputAV


def c_types_2array_to_matrix(c_types_array, m, n):
    '''
     将c_types类型的二维数组转换成矩阵
    :param c_types_array: c_types类型的二维数组
    :param m: 矩阵行
    :param n: 矩阵列表
    :return:
    '''
    arr_np = np.frombuffer(c_types_array, dtype=np.float32).reshape((m, n))
    # print(arr_np)
    return arr_np


def find_data_from_matrix(OutputAV, matrixA, matrixV, matrixC, m, n):
    '''

    :param OutputAV:
    :param matrixA:
    :param matrixV:
    :param matrixC:
    :param m: 行数
    :param n: 列数
    :return:
    '''
    A1 = c_types_2array_to_matrix(OutputAV, m, n)
    print("----------------A1--------------------")
    print(f'OutputAV-r:{A1.shape[0]} OutputAV-c:{A1.shape[1]} non_zero_rows:{non_zero_rows_matrix_calculate(A1)}')
    print(A1)
    A2 = c_types_2array_to_matrix(matrixA, m, n)
    A3 = c_types_2array_to_matrix(matrixV, m, n)
    print("----------------A2--------------------")
    print(f'matrixA-r:{A2.shape[0]} matrixA-c:{A2.shape[1]} non_zero_rows:{non_zero_rows_matrix_calculate(A2)}'
          f' non_zeros_thous_rows_matrix_calculate:{non_zeros_thous_rows_matrix_calculate(A2)}')
    print(A2)

    print("----------------A3--------------------")
    print(f'matrixV-r:{A3.shape[0]} matrixV-c:{A3.shape[1]} non_zero_rows:{non_zero_rows_matrix_calculate(A3)}')
    print(A3)

    # 找到A1中非-1元素的坐标
    coord1 = []
    for i in range(m):
        for j in range(n):
            if A1[i, j] != 0:
                coord1.append((i, j))

    print("----------------coord1--------------------")
    print(coord1)

    print("----------------result--------------------")
    # 生成json1和json2
    json1 = {}
    json2 = {}
    for x, y in coord1:
        if A1[x, y] in json1:
            json1[A1[x, y]] += ',' + str(A2[x, y])
        else:
            json1[A1[x, y]] = str(A2[x, y])
        json2[A1[x, y]] = str(A3[x, y])

    # 显示结果
    print(json1)
    print(json2)


if __name__ == '__main__':
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)
    m = 600
    n = 15
    OutputAV = ((ctypes.c_float * n) * m)()
    while True:
        # 从redis队列中获取矩阵：矩阵是15x600
        azimuth_matrix = get_matrix_from_redis(redis_client, redis_key_azimuth_matrix)
        print(f'redis->azimuth_matrix:{azimuth_matrix}')
        velocity_matrix = get_matrix_from_redis(redis_client, redis_key_velocity_matrix)
        print(f'redis->velocity_matrix:{velocity_matrix}')
        corrcoef_matrix = get_matrix_from_redis(redis_client, redis_key_corrcoef_matrix)
        print(f'redis->corrcoef_matrix:{corrcoef_matrix}')

        # 将矩阵转置 然后转换成c_float类型的二维数组
        matrixA = (ctypes.c_float * (m * n))(*np.ravel(azimuth_matrix.transpose()).astype(np.float32))
        matrixV = (ctypes.c_float * (m * n))(*np.ravel(velocity_matrix.transpose()).astype(np.float32))
        matrixC = (ctypes.c_float * (m * n))(*np.ravel(corrcoef_matrix.transpose()).astype(np.float32))

        print(
            f' 1---type(OutputAV):{type(OutputAV)} type(matrixA):{type(matrixA)} type(matrixV):{type(matrixV)} type(matrixC):{type(matrixC)}')

        # 使用reshape函数将一维数组转换成二维数组
        non_zero_cols_matrixA = non_zero_cols_matrix_calculate(np.ctypeslib.as_array(matrixA).reshape((m, n)))
        non_zero_cols_matrixV = non_zero_cols_matrix_calculate(np.ctypeslib.as_array(matrixV).reshape((m, n)))
        non_zero_cols_matrixC = non_zero_cols_matrix_calculate(np.ctypeslib.as_array(matrixC).reshape((m, n)))

        matrixA = ndarray_to_ctype_array(np.ctypeslib.as_array(matrixA).reshape((m, n)), m, n)
        matrixV = ndarray_to_ctype_array(np.ctypeslib.as_array(matrixV).reshape((m, n)), m, n)
        matrixC = ndarray_to_ctype_array(np.ctypeslib.as_array(matrixC).reshape((m, n)), m, n)

        print(f'2---type(OutputAV):{type(OutputAV)} type(matrixA):{type(matrixA)} type(matrixV):{type(matrixV)} type(matrixC):{type(matrixC)}')

        timestamp = time.time()
        matrixA_file = './matrixA_' + str(timestamp) + '.txt'
        matrixV_file = './matrixV_' + str(timestamp) + '.txt'
        matrixC_file = './matrixC_' + str(timestamp) + '.txt'

        output_matrix(matrixA, matrixA_file)
        output_matrix(matrixV, matrixV_file)
        output_matrix(matrixC, matrixC_file)

        print(f'non_zero_cols_matrixA:{non_zero_cols_matrixA} '
              f'non_zero_cols_matrixV:{non_zero_cols_matrixV} '
              f'non_zero_cols_matrixC:{non_zero_cols_matrixC}')

        # 2、PMCC计算
        print(f'type(OutputAV):{type(OutputAV)} type(matrixA):{type(matrixA)} type(matrixV):{type(matrixV)} type(matrixC):{type(matrixC)}')
        # func = FamilyClusterFunc(OutputAV, matrixA, matrixV, matrixC)
        # func.ArrayFamilyForm()


        print(
            f'type(OutputAV):{type(OutputAV)} type(matrixA):{type(matrixA)} type(matrixV):{type(matrixV)} type(matrixC):{type(matrixC)}')

        find_data_from_matrix(OutputAV, matrixA, matrixV, matrixC, m, n)

        # 数据打印
        # print_ctypes_array(OutputAV, "../output.txt")
        # c_OutputAV_arr = (ctypes.c_float * (len(OutputAV) * len(OutputAV[0])))(*np.ravel(OutputAV).astype(np.float32))
        # 将c_float类型的二维数组转换成NumPy数组
        # np_OutputAV_arr = np.ctypeslib.as_array(c_OutputAV_arr).reshape((len(OutputAV), len(OutputAV[0])))

        # db.update("UPDATE dp_single_array_event set matrixA=%s,matrixV=%s,matrixC=%s,matrixAV=%s", (matrixA, matrixV,
        #                                                                                            matrixC,
        #                                                                                            np_OutputAV_arr))
        # 暂停10秒
        time.sleep(10)
