import ctypes
import time
import numpy as np
from datetime import datetime
import ctypes
import pickle
import json
from RedisUtil import RedisClient
from AzimuthCalAlgo import AzimuthCalFunc
from CommonUtils import *
from FamilyClusterFuncConsumer import *

m = 15000
n = 5

redis_key_origin_buffer = 'origin_buffer'
redis_key_origin_single_buffer1 = 'origin_single_buffer1'
redis_key_origin_single_buffer2 = 'origin_single_buffer2'
redis_key_origin_single_buffer3 = 'origin_single_buffer3'
redis_key_origin_single_buffer4 = 'origin_single_buffer4'
redis_key_origin_single_buffer5 = 'origin_single_buffer5'

# 连接 Redis 数据库

# 定义一个队列的名称
queue_name = 'data_queue'
redis_key_AzimuthCalCallBack_Azimuth = 'AzimuthCalCallBack_Azimuth'
redis_key_AzimuthCalCallBack_Velocity = 'AzimuthCalCallBack_Velocity'
redis_key_AzimuthCalCallBack_Corrcoef = 'AzimuthCalCallBack_Corrcoef'

redis_key_azimuth_matrix = 'azimuth_matrix'
redis_key_velocity_matrix = 'velocity_matrix'
redis_key_corrcoef_matrix = 'corrcoef_matrix'


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


def write_single_buffer_to_redis(redis_client, key, value):
    value = list(value)
    pickled = pickle.dumps(value)
    redis_client.set(key, pickled)


def read_single_buffer_from_redis(redis_client, key):
    pickled = redis_client.get(key)
    if pickled is not None:
        return pickle.loads(pickled)
    return (float_type * 15000)()


def get_matrix_from_redis(redis_client, key):
    result = redis_client.get_matrix(key)
    if result is None:
        return np.zeros((m, n))
    return result


def push_origin_buffer_to_matrix(redis_client, origin_buffer_nparray):
    # 将新的矩阵插入到redis中
    redis_client.set_matrix(redis_key_origin_buffer, origin_buffer_nparray)


def get_matrix_from_redis(redis_client, key, m, n):
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


def push_azimuth_velocity_corrcoef_to_matrix(redis_client, d):
    # 将c_float数组转换成15x1的向量
    m = 15
    azimuth_vector = np.ctypeslib.as_array(d['k_azimuth']).reshape((m, 1))
    velocity_vector = np.ctypeslib.as_array(d['k_velocity']).reshape((m, 1))
    corrcoef_vector = np.ctypeslib.as_array(d['k_corrcoef']).reshape((m, 1))

    # 从redis获取举着 将向量插入到矩阵末尾
    azimuth_matrix = get_matrix_from_redis(redis_client, redis_key_azimuth_matrix, 15, 60)
    velocity_matrix = get_matrix_from_redis(redis_client, redis_key_velocity_matrix, 15, 60)
    corrcoef_matrix = get_matrix_from_redis(redis_client, redis_key_corrcoef_matrix, 15, 60)

    azimuth_matrix = np.concatenate((azimuth_matrix[:, 1:], azimuth_vector), axis=1)
    velocity_matrix = np.concatenate((velocity_matrix[:, 1:], velocity_vector), axis=1)
    corrcoef_matrix = np.concatenate((corrcoef_matrix[:, 1:], corrcoef_vector), axis=1)

    # 将新的矩阵插入到redis中
    redis_client.set_matrix(redis_key_azimuth_matrix, azimuth_matrix)
    redis_client.set_matrix(redis_key_velocity_matrix, velocity_matrix)
    redis_client.set_matrix(redis_key_corrcoef_matrix, corrcoef_matrix)


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
             c_float_array_buffer5: (ctypes.c_float * 15000)()):
    '''
     将一维数组封装成一个二维数组
    :param c_float_array_buffer1: c_float类型的一维数组
    :param c_float_array_buffer2: c_float类型的一维数组
    :param c_float_array_buffer3: c_float类型的一维数组
    :param c_float_array_buffer4: c_float类型的一维数组
    :param c_float_array_buffer5: c_float类型的一维数组
    :return: nparry类型的二维数组
    '''
    buffer1 = np.ctypeslib.as_array(c_float_array_buffer1)
    buffer2 = np.ctypeslib.as_array(c_float_array_buffer2)
    buffer3 = np.ctypeslib.as_array(c_float_array_buffer3)
    buffer4 = np.ctypeslib.as_array(c_float_array_buffer4)
    buffer5 = np.ctypeslib.as_array(c_float_array_buffer5)
    result = np.zeros((15000, 5), np.float32)
    if len(buffer1) == 15000 and len(buffer2) == 15000 and len(buffer3) == 15000 and len(buffer4) == 15000 and len(
            buffer5) == 15000:
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


def print_non_zero_column(matrix):
    count = 0
    for row in matrix:
        if any(row != 0):
            count += 1
    return count


# 定义数据类型和数组
float_type = ctypes.c_float
itemsize = ctypes.sizeof(float_type)

array_type = (float_type * 5) * 15000

# 打开5个bin文件
f1 = open('./data/xKEL1.bin', 'rb')
f2 = open('./data/xKEL2.bin', 'rb')
f3 = open('./data/xKEL3.bin', 'rb')
f4 = open('./data/xKEL4.bin', 'rb')
f5 = open('./data/xKEL5.bin', 'rb')

# 定义5个一维buffer,每个长度15000
buffer1 = (float_type * 15000)()
buffer2 = (float_type * 15000)()
buffer3 = (float_type * 15000)()
buffer4 = (float_type * 15000)()
buffer5 = (float_type * 15000)()

begin = False


def init_buffer(f1, f2, f3, f4, f5):
    print(f'初始化前:buffer1:{buffer1[0]} ')
    # 读取150s数据,150x100=15000,对应15000x4=60000个字节
    data1 = np.frombuffer(f1.read(60000), np.float32)
    data2 = np.frombuffer(f2.read(60000), np.float32)
    data3 = np.frombuffer(f3.read(60000), np.float32)
    data4 = np.frombuffer(f4.read(60000), np.float32)
    data5 = np.frombuffer(f5.read(60000), np.float32)

    data1 = data1[:15000]
    data2 = data2[:15000]
    data3 = data3[:15000]
    data4 = data4[:15000]
    data5 = data5[:15000]

    for i in range(15000):
        buffer1[i] = data1[i]
        buffer2[i] = data2[i]
        buffer3[i] = data3[i]
        buffer4[i] = data4[i]
        buffer5[i] = data5[i]

    print(f'初始化前:buffer1:{buffer1[0]} ')


if __name__ == '__main__':
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)

    # OutputAV = ((ctypes.c_float * 15) * 600)()
    OutputAV = np.zeros((60, 15))
    # 读取并推送数据,每10秒推1000个
    start = time.time()
    done = False
    while True:
        if time.time() - start > 3:  # 10秒推送一次
            print(f'begin 开始计数:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            if begin == False:
                init_buffer(f1, f2, f3, f4, f5)
                begin = True
            else:
                data1 = np.frombuffer(f1.read(4000), np.float32)
                data2 = np.frombuffer(f2.read(4000), np.float32)
                data3 = np.frombuffer(f3.read(4000), np.float32)
                data4 = np.frombuffer(f4.read(4000), np.float32)
                data5 = np.frombuffer(f5.read(4000), np.float32)

                # 移除buffer头部1000个元素
                buffer1 = buffer1[1000:] + data1.tolist()
                buffer2 = buffer2[1000:] + data2.tolist()
                buffer3 = buffer3[1000:] + data3.tolist()
                buffer4 = buffer4[1000:] + data4.tolist()
                buffer5 = buffer5[1000:] + data5.tolist()

            print("-------------------------------------------------------------------")
            buffer = contract(buffer1, buffer2, buffer3, buffer4, buffer5)
            print(f'type(buffer):{type(buffer)} non_zero_column(buffer):{print_non_zero_column(buffer)}')
            # push_data_to_matrix(redis_client, ndarray)
            print("-------------------------redis------------------------------------------")
            # ndarray = get_matrix_from_redis(redis_client, redis_key_origin_buffer)
            ctype_array_buffer = ndarray_to_ctype_array(buffer, m, n)

            # 方位角计算
            func = AzimuthCalFunc()
            func.AzimuthCalCallBack(ctype_array_buffer)

            if func.Azimuth and func.Velocity and func.Corrcoef:
                azimuth_ndarray = ctype_array_to_ndarray(func.Azimuth, 15)
                velocity_ndarray = ctype_array_to_ndarray(func.Velocity, 15)
                corrcoef_ndarray = ctype_array_to_ndarray(func.Corrcoef, 15)
                gen_azimuth_velocity_corrcoef(redis_client, azimuth_ndarray, velocity_ndarray, corrcoef_ndarray)

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
                # matrixA = (ctypes.c_float * (600 * 15))(*np.ravel(azimuth_matrix.transpose()).astype(np.float32))
                # matrixV = (ctypes.c_float * (600 * 15))(*np.ravel(velocity_matrix.transpose()).astype(np.float32))
                # matrixC = (ctypes.c_float * (600 * 15))(*np.ravel(corrcoef_matrix.transpose()).astype(np.float32))

                matrixA_pointer = convert_to_pointer(azimuth_matrix.transpose())
                matrixV_pointer = convert_to_pointer(velocity_matrix.transpose())
                matrixC_pointer = convert_to_pointer(corrcoef_matrix.transpose())
                outputAV_pointer = convert_to_pointer(OutputAV)

                print(
                    f' 1---type(OutputAV):{type(outputAV_pointer)} type(matrixA):{type(matrixA_pointer)} type(matrixV):{type(matrixV_pointer)} type(matrixC):{type(matrixC_pointer)}')

                # 使用reshape函数将一维数组转换成二维数组
                # matrixA = ndarray_to_ctype_array(np.ctypeslib.as_array(matrixA).reshape((600, 15)), 600, 15)
                # matrixV = ndarray_to_ctype_array(np.ctypeslib.as_array(matrixV).reshape((600, 15)), 600, 15)
                # matrixC = ndarray_to_ctype_array(np.ctypeslib.as_array(matrixC).reshape((600, 15)), 600, 15)

                timestamp = time.time()
                matrixA_file = './matrixA_' + str(timestamp) + '.txt'
                matrixV_file = './matrixV_' + str(timestamp) + '.txt'
                matrixC_file = './matrixC_' + str(timestamp) + '.txt'
                OutputAV_file = './OutputAV_' + str(timestamp) + '.txt'

                # output_matrix(matrixA, matrixA_file)
                # output_matrix(matrixV, matrixV_file)
                # output_matrix(matrixC, matrixC_file)

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
                find_data_from_matrix(outputAV_matrix, matrixA_matrix, matrixV_matrix, matrixC_matrix, 60, 15)
                output_matrix(matrixA_matrix, matrixA_file)
                output_matrix(matrixV_matrix, matrixV_file)
                output_matrix(matrixC_matrix, matrixC_file)

            start = time.time()  # 重新计时
