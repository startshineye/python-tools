#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 事件检测方位角模块生产者模块:包括方位角、速度、相关性
import time
import redis
import numpy as np
import json

# 连接 Redis 数据库
r = redis.Redis(host='localhost', port=6379, password='Founder123', db=0)

# 定义一个队列的名称
queue_name = 'data_queue'
redis_key_AzimuthCalCallBack_Azimuth = 'AzimuthCalCallBack_Azimuth'
redis_key_AzimuthCalCallBack_Velocity = 'AzimuthCalCallBack_Velocity'
redis_key_AzimuthCalCallBack_Corrcoef = 'AzimuthCalCallBack_Corrcoef'


def gen_azimuth_velocity_corrcoef():
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
    r.rpush(queue_name, json_str)


if __name__ == '__main__':
    while True:
        gen_azimuth_velocity_corrcoef()
        # 暂停10秒
        time.sleep(100)


