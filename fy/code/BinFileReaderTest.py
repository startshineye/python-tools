#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 测试一个5x5的矩阵数据

import ctypes
import time
import numpy as np
from datetime import datetime
import ctypes
from RedisUtil import RedisClient

m = 5
n = 5

redis_key_test_origin_buffer = 'test_origin_buffer'


def push_data_to_matrix(redis_client, origin_buffer_nparray):
    # 将新的矩阵插入到redis中
    redis_client.set_matrix(redis_key_test_origin_buffer, origin_buffer_nparray)


def get_matrix_from_redis(redis_client, key):
    result = redis_client.get_matrix(key)
    if result is None:
        return np.zeros((m, n))
    return result


def ndarray_to_ctype_array(src, m, n):
    '''
    将np的2维数组转换成ctype类型的2维数组
    :param src: np的2维数
    :param m: 数组行数
    :param n: 数组列数
    :return: ctype类型的2维数组
    '''
    b = (ctypes.c_float * n) * m
    c = b()

    for i in range(m):
        for j in range(n):
            c[i][j] = src[i][j]

    return c


def contract(c_float_array_buffer1: (ctypes.c_float * 15000)(), c_float_array_buffer2: (ctypes.c_float * 15000)(),
             c_float_array_buffer3: (ctypes.c_float * 15000)(), c_float_array_buffer4: (ctypes.c_float * 15000)(),
             c_float_array_buffer5: (ctypes.c_float * 15000)(), m):
    '''
     将一维数组封装成一个二维数组
    :param c_float_array_buffer1: c_float类型的一维数组
    :param c_float_array_buffer2: c_float类型的一维数组
    :param c_float_array_buffer3: c_float类型的一维数组
    :param c_float_array_buffer4: c_float类型的一维数组
    :param c_float_array_buffer5: c_float类型的一维数组
    :param m: 二维数组数据长度
    :return: nparry类型的二维数组
    '''
    buffer1 = np.ctypeslib.as_array(c_float_array_buffer1)
    buffer2 = np.ctypeslib.as_array(c_float_array_buffer2)
    buffer3 = np.ctypeslib.as_array(c_float_array_buffer3)
    buffer4 = np.ctypeslib.as_array(c_float_array_buffer4)
    buffer5 = np.ctypeslib.as_array(c_float_array_buffer5)
    result = np.zeros((m, 5), np.float32)
    result[:, 0] = buffer1
    result[:, 1] = buffer2
    result[:, 2] = buffer3
    result[:, 3] = buffer4
    result[:, 4] = buffer5
    return result


def print_matrix(array, m, n):
    # 转化为numpy数组并重塑为2x3
    nparray = np.frombuffer(array, float_type)
    nparray = np.reshape(nparray, (m, n))

    # 转化为python列表
    list = nparray.tolist()

    # 打印列表
    print(list)


# 定义数据类型和数组
float_type = ctypes.c_float
itemsize = ctypes.sizeof(float_type)

# 打开5个bin文件
f1 = open('../data/xKEL1.bin', 'rb')
f2 = open('../data/xKEL2.bin', 'rb')
f3 = open('../data/xKEL3.bin', 'rb')
f4 = open('../data/xKEL4.bin', 'rb')
f5 = open('../data/xKEL5.bin', 'rb')

# 定义5个一维buffer,每个长度5
buffer1 = (float_type * 5)()
buffer2 = (float_type * 5)()
buffer3 = (float_type * 5)()
buffer4 = (float_type * 5)()
buffer5 = (float_type * 5)()

if __name__ == '__main__':
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)
    # 读取并推送数据,每10秒推1000个
    start = time.time()
    while True:
        if time.time() - start > 8:  # 10秒推送一次
            print(f'开始计数:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            # 读取1个元素.每个元素4个字节
            data1 = np.frombuffer(f1.read(4), np.float32)
            data2 = np.frombuffer(f2.read(4), np.float32)
            data3 = np.frombuffer(f3.read(4), np.float32)
            data4 = np.frombuffer(f4.read(4), np.float32)
            data5 = np.frombuffer(f5.read(4), np.float32)

            # data1 = np.frombuffer(f1.read(1000 * np.float32.itemsize), np.float32)
            # data2 = np.frombuffer(f2.read(1000 * np.float32.itemsize), np.float32)
            # ...

            # 移除buffer头部1000个元素
            buffer1 = buffer1[1:] + data1.tolist()
            buffer2 = buffer2[1:] + data2.tolist()
            buffer3 = buffer3[1:] + data3.tolist()
            buffer4 = buffer4[1:] + data4.tolist()
            buffer5 = buffer5[1:] + data5.tolist()

            print("-----------------------------buffer1--------------------------------------")
            # print(buffer1)

            ndarray = contract(buffer1, buffer2, buffer3, buffer4, buffer5, 5)
            print("-----------------------------ndarray--------------------------------------")
            #print(ndarray)
            # print(type(ndarray))
            push_data_to_matrix(redis_client, ndarray)
            # array = ndarray_to_ctype_array(ndarray, 5, 5)

            print("-----------------------------redis--------------------------------------")
            redis = get_matrix_from_redis(redis_client, redis_key_test_origin_buffer)
            print(redis)

            start = time.time()  # 重新计时

# buffer1-5为最终结果,5个15000x5数组
