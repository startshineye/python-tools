#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 事件检测生产者模块:包括PMCC
from RedisUtil import RedisClient
import numpy as np
from ctypes import *
import ctypes
import time
import json

m = 15
n = 60

queue_name = 'data_queue'
redis_key_azimuth_matrix = 'azimuth_matrix'
redis_key_velocity_matrix = 'velocity_matrix'
redis_key_corrcoef_matrix = 'corrcoef_matrix'

redis_key_AzimuthCalCallBack_Azimuth = 'AzimuthCalCallBack_Azimuth'
redis_key_AzimuthCalCallBack_Velocity = 'AzimuthCalCallBack_Velocity'
redis_key_AzimuthCalCallBack_Corrcoef = 'AzimuthCalCallBack_Corrcoef'


def get_matrix_from_redis(redis_client, key):
    result = redis_client.get_matrix(key)
    if result is None:
        return np.zeros((m, n))
    return result


def get_c_array_from_redis(redis_client, key):
    result = redis_client.lpop(key)
    if result:
        print(f'FamilyClusterFuncProducer lpop json_str:{result}')
        print(type(result))
        result_json = json.loads(result)
        azimuth_value = result_json[redis_key_AzimuthCalCallBack_Azimuth]
        azimuth_obj = np.array(azimuth_value)

        c_azimuth_obj = (ctypes.c_float * len(azimuth_obj))(*azimuth_obj)

        velocity_value = result_json[redis_key_AzimuthCalCallBack_Velocity]
        velocity_obj = np.array(velocity_value)
        c_velocity_obj = (ctypes.c_float * len(velocity_obj))(*velocity_obj)

        corrcoef_value = result_json[redis_key_AzimuthCalCallBack_Corrcoef]
        corrcoef_obj = np.array(corrcoef_value)
        c_corrcoef_obj = (ctypes.c_float * len(corrcoef_obj))(*corrcoef_obj)

        d = {
            'k_azimuth': c_azimuth_obj,
            'k_velocity': c_velocity_obj,
            'k_corrcoef': c_corrcoef_obj
        }
        return d
    else:
        return result


def push_data_to_matrix(redis_client, d):
    # 将c_float数组转换成15x1的向量
    azimuth_vector = np.ctypeslib.as_array(d['k_azimuth']).reshape((m, 1))
    velocity_vector = np.ctypeslib.as_array(d['k_velocity']).reshape((m, 1))
    corrcoef_vector = np.ctypeslib.as_array(d['k_corrcoef']).reshape((m, 1))

    # 从redis获取举着 将向量插入到矩阵末尾
    azimuth_matrix = get_matrix_from_redis(redis_client, redis_key_azimuth_matrix)
    velocity_matrix = get_matrix_from_redis(redis_client, redis_key_velocity_matrix)
    corrcoef_matrix = get_matrix_from_redis(redis_client, redis_key_corrcoef_matrix)

    azimuth_matrix = np.concatenate((azimuth_matrix[:, 1:], azimuth_vector), axis=1)
    velocity_matrix = np.concatenate((velocity_matrix[:, 1:], velocity_vector), axis=1)
    corrcoef_matrix = np.concatenate((corrcoef_matrix[:, 1:], corrcoef_vector), axis=1)

    # 将新的矩阵插入到redis中
    redis_client.set_matrix(redis_key_azimuth_matrix, azimuth_matrix)
    redis_client.set_matrix(redis_key_velocity_matrix, velocity_matrix)
    redis_client.set_matrix(redis_key_corrcoef_matrix, corrcoef_matrix)


if __name__ == '__main__':
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)
    while True:
        # 1、从redis里面获取对应的矩阵，如果没有的话初始化15x60的零矩阵
        d = get_c_array_from_redis(redis_client, queue_name)
        print(d)
        if d:
            print(d['k_azimuth'])
            print(d['k_velocity'])
            print(d['k_corrcoef'])
            push_data_to_matrix(redis_client, d)

        ndarray = get_matrix_from_redis(redis_client, redis_key_azimuth_matrix)
        print(f'get_matrix_from_redis :{ndarray}')

        #azimuth = (c_float * 15)()
        #azimuth_vector = np.ctypeslib.as_array(azimuth).reshape((m, 1))
        # 暂停10秒
        time.sleep(10)
