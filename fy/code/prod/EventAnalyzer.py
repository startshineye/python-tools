#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
 事件分析模块:1、每个阵元 每次读取10秒数据，数据加入各自buffer1-buffer4的尾部(buffer长度15000；每10秒为1000个数据点)，然后头部移除1000个数据；
            2、然后通过方位角检测模块检测出对应的：azimuth、velocity、corrcoef；然后分别将其加入15x60的矩阵；azimuth_matrix、velocity_matrix、corrcoef_matrix；
            3、读取azimuth_matrix、velocity_matrix、corrcoef_matrix数据然后专置成60x15，然后调用PMCC模块检测出事件；
            4、将从matrixAV中检测非0的事件的对应方位角、视在速度、相关性统计出来，然后将数据插入到单阵事件表中。
'''


from datetime import datetime, timedelta
import mysql.connector
import time
from CommonUtils import *
from RedisUtil import RedisClient
from AzimuthCalAlgo import AzimuthCalFunc
from FamilyClusterFuncConsumer import FamilyClusterFunc
from IdWorkers import *

float_type = ctypes.c_float
itemsize = ctypes.sizeof(float_type)

array_type = (float_type * 5) * 15000

queue_name = 'data_queue'
time_format = "%Y-%m-%d %H:%M:%S"


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
    A4 = c_types_2array_to_matrix(matrixC, m, n)
    print("----------------A2--------------------")
    print(f'matrixA-r:{A2.shape[0]} matrixA-c:{A2.shape[1]} non_zero_rows:{non_zero_rows_matrix_calculate(A2)}'
          f' non_zeros_thous_rows_matrix_calculate:{non_zeros_thous_rows_matrix_calculate(A2)}')
    print(A2)

    print("----------------A3--------------------")
    print(f'matrixV-r:{A3.shape[0]} matrixV-c:{A3.shape[1]} non_zero_rows:{non_zero_rows_matrix_calculate(A3)}')
    print(A3)

    # 找到OutputAV:A1中非-1元素的坐标
    event_coordinates = []
    for i in range(m):
        for j in range(n):
            if A1[i, j] != 0:
                event_coordinates.append((i, j))

    print("----------------event_coordinates--------------------")
    print(event_coordinates)

    print("----------------result--------------------")
    # 生成event_azimuth event_velocity
    event_azimuth = {}
    event_velocity = {}
    event_relevant = {}
    for x, y in event_coordinates:
        if A1[x, y] in event_azimuth:
            event_azimuth[A1[x, y]] += ',' + str(A2[x, y])
        else:
            event_azimuth[A1[x, y]] = str(A2[x, y])
        event_velocity[A1[x, y]] = str(A3[x, y])
        event_relevant[A1[x, y]] = str(A4[x, y])

    # 显示结果
    print(f'event_azimuth:{event_azimuth}')
    print(f'event_velocity:{event_velocity}')
    print(f'event_relevant:{event_relevant}')
    return event_azimuth, event_velocity, event_relevant


class EventAnalyzer:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='rbjf_DEV123',
                                           host='103.36.193.81',
                                           port='3306',
                                           database='ruoyi')
        self.cursor = self.cnx.cursor()
        # 定义5个一维buffer,每个长度15000
        self.bufferA0 = read_single_buffer_from_redis(redis_client, redis_key_origin_single_bufferA0)
        self.bufferB1 = read_single_buffer_from_redis(redis_client, redis_key_origin_single_bufferB1)
        self.bufferB2 = read_single_buffer_from_redis(redis_client, redis_key_origin_single_bufferB2)
        self.bufferB3 = read_single_buffer_from_redis(redis_client, redis_key_origin_single_bufferB3)

    def get_db_buffer(self):
        query = "SELECT * FROM dp_origin_data WHERE operate_status = 0 AND device_id IN ('A0', 'B1', 'B2', 'B3') AND " \
                "collect_time = (SELECT min(collect_time) FROM dp_origin_data WHERE operate_status = 0 AND device_id IN " \
                "('A0', 'B1', 'B2', 'B3')) "
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_db_buffer_status(self, uids):
        if len(uids) > 0:
            update_query = "update dp_origin_data set operate_status = 1 where uid in  (%s)"
            placeholders = ', '.join(['%s'] * len(uids))
            update_query = update_query % placeholders

            # 执行更新操作
            self.cursor.execute(update_query, uids)
            # 提交更改到数据库
            commit = self.cnx.commit()
            print(f'update_db_buffer_status:{commit}')

    def average_str_nums(self, str_nums):
        num_list = str_nums.split(",")
        nums = [float(num) for num in num_list]
        # 计算平均值
        return sum(nums) / len(nums)

    def event_to_db(self, site_id, collect_time, collect_time_delay_ten_second, event_azimuth, event_velocity, event_relevant):
        # 遍历event_azimuth(事件方位角)中的键和值
        # 定义插入数据的SQL语句
        sql = "INSERT INTO dp_single_array_event (sevent_id, site_id, start_time, end_time, detect_time, azimuth, appa_speed, av_azimuth, av_appa_speed, revelent) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        data = []
        event_array = []
        for key, value in event_azimuth.items():
            print(key, ":", value)
            event_array.append(key)

        if len(event_array) == 0:
            return

        for i in range(len(event_array)):
            uid = nextId()
            event = event_array[i]
            azimuth = event_azimuth[event]
            av_azimuth = self.average_str_nums(azimuth)
            velocity = event_velocity[event]
            av_appa_speed = self.average_str_nums(velocity)
            relevant = event_relevant[event]
            data = [uid, site_id, collect_time, collect_time_delay_ten_second, collect_time, azimuth, velocity, av_azimuth, av_appa_speed, relevant]
            self.cursor.execute(sql, data)
            # 提交事务
            self.cnx.commit()

    def push_data_to_buffer(self, redis_client, results):
        uids = []
        print(results)
        # 移除buffer头部1000个元素
        '''
        self.bufferA0 = self.bufferA0[1000:] + data1.tolist()
        self.bufferB1 = self.bufferB1[1000:] + data2.tolist()
        self.bufferB2 = self.bufferB2[1000:] + data3.tolist()
        self.bufferB3 = self.bufferB3[1000:] + data4.tolist()
        '''
        siteId = None
        collect_time = None
        for row in results:
            siteId = row[3]
            collect_time = row[5]
            deviceId = row[4]
            uid = row[0]
            if uid is not None:
                uids.append(uid)
            single_buffer = row[16].split(',')
            # 移除buffer头部1000个元素
            if "A0" == deviceId:
                self.bufferA0 = self.bufferA0[1000:] + single_buffer
            elif "B1" == deviceId:
                self.bufferB1 = self.bufferB1[1000:] + single_buffer
            elif "B2" == deviceId:
                self.bufferB2 = self.bufferB2[1000:] + single_buffer
            elif "B3" == deviceId:
                self.bufferB3 = self.bufferB3[1000:] + single_buffer
            print(f'type:{type(single_buffer)} single_buffer:{single_buffer}')

        # 数据写入到redis缓存
        write_single_buffer_to_redis(redis_client, redis_key_origin_single_bufferA0, self.bufferA0)
        write_single_buffer_to_redis(redis_client, redis_key_origin_single_bufferB1, self.bufferB1)
        write_single_buffer_to_redis(redis_client, redis_key_origin_single_bufferB2, self.bufferB2)
        write_single_buffer_to_redis(redis_client, redis_key_origin_single_bufferB3, self.bufferB3)

        ndarray = single_buffer_contract(self.bufferA0, self.bufferB1, self.bufferB2, self.bufferB3, 15000, 4)
        print(f'print_non_zero_column:{print_non_zero_column(ndarray)}')
        push_data_to_matrix(redis_client, ndarray)

        # update data status
        self.update_db_buffer_status(uids)
        return siteId, collect_time

    def event_analysis(self, site_id, collect_time, collect_time_delay_ten_second, redis_client, m, n, OutputAV):
        ndarray = get_matrix_from_redis(redis_client, redis_key_origin_buffer, m, n)
        ctype_array_buffer = ndarray_to_ctype_array(ndarray, m, n)
        # 方位角计算
        func = AzimuthCalFunc()
        func.AzimuthCalCallBack(ctype_array_buffer)
        if func.Azimuth and func.Velocity and func.Corrcoef:
            azimuth_ndarray = ctype_array_to_ndarray(func.Azimuth, 15)
            velocity_ndarray = ctype_array_to_ndarray(func.Velocity, 15)
            corrcoef_ndarray = ctype_array_to_ndarray(func.Corrcoef, 15)
            gen_azimuth_velocity_corrcoef(redis_client, azimuth_ndarray, velocity_ndarray, corrcoef_ndarray, queue_name)

            # 获取数据
            # 1、从redis里面获取对应的矩阵，如果没有的话初始化15x60的零矩阵
            d = get_c_array_from_redis(redis_client, queue_name)
            print(d)
            if d:
                print(d['k_azimuth'])
                print(d['k_velocity'])
                print(d['k_corrcoef'])
                push_azimuth_velocity_corrcoef_to_matrix(redis_client, d)

            # Family操作
            # 从redis队列中获取矩阵：矩阵是15x60
            azimuth_matrix = get_matrix_from_redis(redis_client, redis_key_azimuth_matrix, 15, 60)
            print(f'redis->azimuth_matrix:{azimuth_matrix}')
            velocity_matrix = get_matrix_from_redis(redis_client, redis_key_velocity_matrix, 15, 60)
            print(f'redis->velocity_matrix:{velocity_matrix}')
            corrcoef_matrix = get_matrix_from_redis(redis_client, redis_key_corrcoef_matrix, 15, 60)
            print(f'redis->corrcoef_matrix:{corrcoef_matrix}')

            # 将矩阵转置:15x600 变成600x15  然后转换成c_float类型的二维数组:
            matrixA_pointer = convert_to_pointer(azimuth_matrix.transpose())
            matrixV_pointer = convert_to_pointer(velocity_matrix.transpose())
            matrixC_pointer = convert_to_pointer(corrcoef_matrix.transpose())
            outputAV_pointer = convert_to_pointer(OutputAV)

            print(
                f' 1---type(OutputAV):{type(outputAV_pointer)} type(matrixA):{type(matrixA_pointer)} type(matrixV):{type(matrixV_pointer)} type(matrixC):{type(matrixC_pointer)}')

            timestamp = time.time()
            matrixA_file = './matrixA_' + str(timestamp) + '.txt'
            matrixV_file = './matrixV_' + str(timestamp) + '.txt'
            matrixC_file = './matrixC_' + str(timestamp) + '.txt'
            OutputAV_file = './OutputAV_' + str(timestamp) + '.txt'


            # 2、PMCC计算
            print(
                f' 2---type(OutputAV):{type(outputAV_pointer)} type(matrixA):{type(matrixA_pointer)} type(matrixV):{type(matrixV_pointer)} type(matrixC):{type(matrixC_pointer)}')
            func = FamilyClusterFunc(outputAV_pointer, matrixA_pointer, matrixV_pointer, matrixC_pointer)
            func.ArrayFamilyForm()
            outputAV_matrix = convert_pointer_to_matrix(func.OutputAV, 15, 60)
            matrixA_matrix = convert_pointer_to_matrix(matrixA_pointer, 15, 60)
            matrixV_matrix = convert_pointer_to_matrix(matrixV_pointer, 15, 60)
            matrixC_matrix = convert_pointer_to_matrix(matrixC_pointer, 15, 60)

            print(outputAV_matrix)
            print(f'find_nonzero:{find_nonzero(outputAV_matrix)}')
            event_azimuth, event_velocity, event_relevant = find_data_from_matrix(outputAV_matrix, matrixA_matrix,
                                                                                  matrixV_matrix,
                                                                                  matrixC_matrix, 60, 15)
            self.event_to_db(site_id, collect_time, collect_time_delay_ten_second, event_azimuth, event_velocity, event_relevant)

            output_matrix(matrixA_matrix, matrixA_file)
            output_matrix(matrixV_matrix, matrixV_file)
            output_matrix(matrixC_matrix, matrixC_file)


if __name__ == "__main__":
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)
    event = EventAnalyzer()
    while True:
        try:
            results = event.get_db_buffer()
            OutputAV = np.zeros((60, 15))
            siteId, collect_time = event.push_data_to_buffer(redis_client, results)
            collect_time_delay_ten_second = collect_time + timedelta(seconds=10)
            print(f'siteId:{siteId}, collect_time:{collect_time} type_collect_time:{type(collect_time)} new_collect_time:{collect_time_delay_ten_second}')
            event.event_analysis(siteId, collect_time, collect_time_delay_ten_second, redis_client, 15000, 4, OutputAV)
        except Exception as e:
            # 捕获异常并进行处理
            print("捕获到异常:", str(e))

        # 等待10秒
        time.sleep(10)
