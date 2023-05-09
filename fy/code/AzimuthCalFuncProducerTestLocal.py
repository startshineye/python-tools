#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 事件检测方位角模块生产者模块:包括方位角、速度、相关性
import time
import numpy as np
import json
from RedisUtil import RedisClient
import ctypes

redis_key_origin_buffer = 'origin_buffer'

# 连接 Redis 数据库

# 定义一个队列的名称
queue_name = 'data_queue'
redis_key_AzimuthCalCallBack_Azimuth = 'AzimuthCalCallBack_Azimuth'
redis_key_AzimuthCalCallBack_Velocity = 'AzimuthCalCallBack_Velocity'
redis_key_AzimuthCalCallBack_Corrcoef = 'AzimuthCalCallBack_Corrcoef'

m = 15000
n = 5


def ctype_array_to_ndarray(src, m):

    print(f'my_c_array:{type(src)}')
    # 将 ctypes 对象转换为 bytes 对象
    my_bytes = ctypes.cast(src, ctypes.POINTER(ctypes.c_float * m)).contents
    # 将 bytes 对象转换为 numpy 数组
    my_np_array = np.frombuffer(my_bytes, dtype=np.float32)
    return my_np_array


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


def get_matrix_from_redis(redis_client, key):
    result = redis_client.get_matrix(key)
    if result is None:
        return np.zeros((m, n))
    return result


def gen_azimuth_velocity_corrcoef(redis_client):
    # 生成一个 15x1 的数组
    azimuth_array = np.array([-1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0,
                              -1000.0, -1000.0, -1000.0, -1000.0, -1000.0])

    velocity_array = np.array(
        [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0])

    corrcoef_array = np.array(
        [2.5822121138711653e-34, 4.571175720473986e-41, 7.048934849511555e-38, 0.0, 1.3693397977576138e-34,
         4.571175720473986e-41, 5.707908909577075e-28, 4.571175720473986e-41, 0.0, 0.0, 1.3693397977576138e-34,
         4.571175720473986e-41, 7.048934849511555e-38, 0.0, 7.7582004838157695e-28])

    # 创建一个字典对象
    hash_element = {redis_key_AzimuthCalCallBack_Azimuth: azimuth_array.tolist(),
                    redis_key_AzimuthCalCallBack_Velocity: velocity_array.tolist(),
                    redis_key_AzimuthCalCallBack_Corrcoef: corrcoef_array.tolist()}

    # 将字典对象转换为 JSON 字符串
    json_str = json.dumps(hash_element)

    # 将 JSON 字符串添加到队列中
    redis_client.rpush(queue_name, json_str)


if __name__ == '__main__':
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)
    gen_azimuth_velocity_corrcoef(redis_client)
    # 暂停10秒
