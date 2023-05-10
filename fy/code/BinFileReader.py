import ctypes
import time
import numpy as np
from datetime import datetime
import ctypes
import pickle
from RedisUtil import RedisClient

m = 15000
n = 5

redis_key_origin_buffer = 'origin_buffer'
redis_key_origin_single_buffer1 = 'origin_single_buffer1'
redis_key_origin_single_buffer2 = 'origin_single_buffer2'
redis_key_origin_single_buffer3 = 'origin_single_buffer3'
redis_key_origin_single_buffer4 = 'origin_single_buffer4'
redis_key_origin_single_buffer5 = 'origin_single_buffer5'


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


def push_data_to_matrix(redis_client, origin_buffer_nparray):
    # 将新的矩阵插入到redis中
    redis_client.set_matrix(redis_key_origin_buffer, origin_buffer_nparray)


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
    if len(buffer1) == 15000 and len(buffer2) == 15000 and len(buffer3) == 15000 and len(buffer4) == 15000 and len(buffer5) == 15000:
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
f1 = open('../data/01_A0.bin', 'rb')
f2 = open('../data/01_B1.bin', 'rb')
f3 = open('../data/01_B2.bin', 'rb')
f4 = open('../data/01_B3.bin', 'rb')
f5 = open('../data/xKEL5.bin', 'rb')

# 定义5个一维buffer,每个长度15000
buffer1 = (float_type * 15000)()
buffer2 = (float_type * 15000)()
buffer3 = (float_type * 15000)()
buffer4 = (float_type * 15000)()
buffer5 = (float_type * 15000)()

if __name__ == '__main__':
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)

    # 读取并推送数据,每10秒推1000个
    start = time.time()
    while True:
        if time.time() - start > 3:  # 10秒推送一次
            print(f'begin 开始计数:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            # 读取1000个元素
            data1 = np.frombuffer(f1.read(4000), np.float32)
            data2 = np.frombuffer(f2.read(4000), np.float32)
            data3 = np.frombuffer(f3.read(4000), np.float32)
            data4 = np.frombuffer(f4.read(4000), np.float32)
            data5 = np.frombuffer(f5.read(4000), np.float32)


            # redis中读取buffer数据
            buffer1 = read_single_buffer_from_redis(redis_client, redis_key_origin_single_buffer1)
            buffer2 = read_single_buffer_from_redis(redis_client, redis_key_origin_single_buffer2)
            buffer3 = read_single_buffer_from_redis(redis_client, redis_key_origin_single_buffer3)
            buffer4 = read_single_buffer_from_redis(redis_client, redis_key_origin_single_buffer4)
            buffer5 = read_single_buffer_from_redis(redis_client, redis_key_origin_single_buffer5)


            # 移除buffer头部1000个元素
            buffer1 = buffer1[1000:] + data1.tolist()
            buffer2 = buffer2[1000:] + data2.tolist()
            buffer3 = buffer3[1000:] + data3.tolist()
            buffer4 = buffer4[1000:] + data4.tolist()
            buffer5 = buffer5[1000:] + data5.tolist()

            # 将buffer数据写入到redis
            write_single_buffer_to_redis(redis_client, redis_key_origin_single_buffer1, buffer1)
            write_single_buffer_to_redis(redis_client, redis_key_origin_single_buffer2, buffer2)
            write_single_buffer_to_redis(redis_client, redis_key_origin_single_buffer3, buffer3)
            write_single_buffer_to_redis(redis_client, redis_key_origin_single_buffer4, buffer4)
            write_single_buffer_to_redis(redis_client, redis_key_origin_single_buffer5, buffer5)

            print("-------------------------------------------------------------------")

            ndarray = contract(buffer1, buffer2, buffer3, buffer4, buffer5)
            print(f'print_non_zero_column:{print_non_zero_column(ndarray)}')
            push_data_to_matrix(redis_client, ndarray)

            print("-------------------------redis------------------------------------------")
            redis = get_matrix_from_redis(redis_client, redis_key_origin_buffer)

            # array = ndarray_to_ctype_array(ndarray, 15000, 5)

            start = time.time()  # 重新计时
# buffer1-5为最终结果,5个15000x5数组
