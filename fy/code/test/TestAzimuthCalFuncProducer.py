#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 事件检测方位角模块生产者模块:包括方位角、速度、相关性
import time
import numpy as np
from datetime import datetime
import json
from AzimuthCalAlgo import AzimuthCalFunc
from RedisUtil import RedisClient
import ctypes
from CommonUtils import *

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
    '''
     将类型为:ctype的一维数组:src转换成一维数组矩阵
    :param src: 类型为:ctype的一维数组
    :param m: src数据长度
    :return: np_array
    '''
    print(f'my_c_array:{type(src)}')
    # 将 ctypes 对象转换为 bytes 对象
    my_bytes = ctypes.cast(src, ctypes.POINTER(ctypes.c_float * m)).contents
    # 将 bytes 对象转换为 numpy 数组
    my_np_array = np.frombuffer(my_bytes, dtype=np.float32)
    return my_np_array


def get_matrix_from_redis(redis_client, key):
    result = redis_client.get_matrix(key)
    if result is None:
        return np.zeros((m, n))
    return result


def gen_azimuth_velocity_corrcoef(redis_client, azimuth_ndarray, velocity_ndarray, corrcoef_ndarray):
    # 创建一个字典对象
    hash_element = {redis_key_AzimuthCalCallBack_Azimuth: azimuth_ndarray.tolist(),
                    redis_key_AzimuthCalCallBack_Velocity: velocity_ndarray.tolist(),
                    redis_key_AzimuthCalCallBack_Corrcoef: corrcoef_ndarray.tolist()}

    # 将字典对象转换为 JSON 字符串
    json_str = json.dumps(hash_element)

    # 将 JSON 字符串添加到队列中
    redis_client.rpush(queue_name, json_str)
    print(f'AzimuthCalFuncProducer rpush json_str:{json_str}')


if __name__ == '__main__':
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)
    func = AzimuthCalFunc()
    while True:

        for i in range(600):
            print(f'begin 开始计数:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            ndarray = get_matrix_from_redis(redis_client, redis_key_origin_buffer)
            ctype_array_buffer = ndarray_to_ctype_array(ndarray, m, n)
            func.AzimuthCalCallBack(ctype_array_buffer)
            for a in func.Azimuth:
                print(f'Azimuth: {a}')

            for a in func.Velocity:
                print(f'Velocity: {a}')

            for a in func.Corrcoef:
                print(f'corrcoef: {a}')

            if func.Azimuth and func.Velocity and func.Corrcoef:
                azimuth_ndarray = ctype_array_to_ndarray(func.Azimuth, 15)
                velocity_ndarray = ctype_array_to_ndarray(func.Velocity, 15)
                corrcoef_ndarray = ctype_array_to_ndarray(func.Corrcoef, 15)
                gen_azimuth_velocity_corrcoef(redis_client, azimuth_ndarray, velocity_ndarray, corrcoef_ndarray)
        # 暂停10秒
        time.sleep(10)