#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 公共方法
import ctypes
import pickle
import numpy as np
from ctypes import *
import json

redis_key_origin_buffer = 'origin_buffer'
redis_key_AzimuthCalCallBack_Azimuth = 'AzimuthCalCallBack_Azimuth'
redis_key_AzimuthCalCallBack_Velocity = 'AzimuthCalCallBack_Velocity'
redis_key_AzimuthCalCallBack_Corrcoef = 'AzimuthCalCallBack_Corrcoef'
redis_key_azimuth_matrix = 'azimuth_matrix'
redis_key_velocity_matrix = 'velocity_matrix'
redis_key_corrcoef_matrix = 'corrcoef_matrix'

redis_key_origin_single_bufferA0 = 'origin_single_bufferA0'
redis_key_origin_single_bufferB1 = 'origin_single_bufferB1'
redis_key_origin_single_bufferB2 = 'origin_single_bufferB2'
redis_key_origin_single_bufferB3 = 'origin_single_bufferB3'


def convert_to_pointer(A):
    # 获取矩阵A的行列数
    rows, cols = A.shape

    # 将A的数据类型转换为ctype中的c_float类型
    A = A.astype(ctypes.c_float)

    # 创建一个大小为15维度x600个数的c_float类型的二维数组
    OutputAV_A = (ctypes.c_float * cols) * rows
    OutputAV = OutputAV_A()

    # 将A中的数据存储到OutputAV中
    for i in range(rows):
        row_data = A[i, :]
        ctypes.memmove(ctypes.addressof(OutputAV[i]), row_data.ctypes.data, row_data.nbytes)

    # 返回OutputAV的指针
    return ctypes.pointer(OutputAV)


def convert_pointer_to_matrix(OutputAV, m, n):
    '''

    :param OutputAV:指针数组 m行 n列
    :param m: 行
    :param n: 列
    :return:
    '''
    # 将OutputAV转换为numpy数组
    B = np.frombuffer(ctypes.cast(OutputAV, ctypes.POINTER(ctypes.c_float * m * n)).contents, dtype=np.float32)
    # 重新reshape为600x15的矩阵
    B = B.reshape((n, m))
    print(B)
    return B


def matrix_to_c_array(matrix):
    print(f'matrix_to_c_array-begin: type(matrix):{type(matrix)}')
    # 定义C语言一维数组类型
    array_type = c_float * matrix.size

    # 初始化C语言一维数组
    c_array = array_type()

    # 遍历矩阵每行,将非0非-1值求和,添加到c_array对应位置
    idx = 0
    for row in matrix:
        col_sum = 0

        for col in range(matrix.shape[1]):
            if row[col] != 0 and row[col] != -1:
                col_sum += row[col]

        c_array[idx] += col_sum
        idx += 1

    return c_array


def c_array_to_pointer(c_array):
    # 获取C语言一维数组指针
    c_pointer = pointer(c_array)
    return c_pointer


def print_data(matrix):
    result = []  # 定义空list
    # 遍历矩阵每个元素
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            # 如果元素不为0或-100.0,添加到list中
            if matrix[i, j] != 0 and matrix[i, j] != -100.0:
                result.append(matrix[i, j])
    # 遍历list输出
    for num in result:
        print(num)
    return result


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


def output_matrix(matrix, filename):
    '''
     矩阵数据输出到文件中
    :param matrix:
    :param filename:
    :return:
    '''
    with open(filename, 'w') as f:
        for row in matrix:
            for col in row:
                f.write(str(col) + ' ')
            f.write('\n')


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


# 定义查询方法
def find_nonzero(array):
    # 获取数组形状
    rows, cols = array.shape
    # 结果列表
    res = []

    # 遍历数组
    for i in range(rows):
        for j in range(cols):
            # 如果当前元素非0,添加到结果中
            if array[i, j] != 0:
                res.append((i, j))

    return res


def non_zero_rows_matrix_calculate(np_array):
    if np_array is None:
        return 0
    rows = np_array.shape[0]
    non_zero_rows = 0
    for i in range(rows):
        if np.all(np_array[i] != 0.0) and np.all(np_array[i] != 0):
            non_zero_rows += 1
        else:
            continue

    return non_zero_rows


def non_thous_rows_matrix_calculate(np_array):
    if np_array is None:
        return 0
    rows = np_array.shape[0]
    non_zero_thous = 0
    for i in range(rows):
        if np.all(np_array[i] == -1000.0):
            continue
        non_zero_thous += 1
    return non_zero_thous


def non_zeros_thous_rows_matrix_calculate(np_array):
    if np_array is None:
        return 0

    count = np.count_nonzero((np_array != -1000.0) & (np_array != 0.0))
    print(count)
    return count


def non_zero_cols_matrix_calculate(np_array):
    cols = np_array.shape[1]
    if np_array is None:
        return 0
    non_zero_cols = 0
    for j in range(cols):
        if np.all(np_array[:, j] == 0):
            continue
        non_zero_cols += 1
    return non_zero_cols


def single_buffer_contract(c_float_array_buffer1: (ctypes.c_float * 15000)(),
                           c_float_array_buffer2: (ctypes.c_float * 15000)(),
                           c_float_array_buffer3: (ctypes.c_float * 15000)(),
                           c_float_array_buffer4: (ctypes.c_float * 15000)(), m, n):
    '''
      将4个单一的buffer转变成mxn的矩阵
    :param c_float_array_buffer1: c_float类型的一维数组
    :param c_float_array_buffer2: c_float类型的一维数组
    :param c_float_array_buffer3: c_float类型的一维数组
    :param c_float_array_buffer4: c_float类型的一维数组
    :param m: 返回合成的矩阵行数
    :param n: 返回合成的矩阵列数
    :return: nparry类型的二维数组
    '''
    buffer1 = np.ctypeslib.as_array(c_float_array_buffer1)
    buffer2 = np.ctypeslib.as_array(c_float_array_buffer2)
    buffer3 = np.ctypeslib.as_array(c_float_array_buffer3)
    buffer4 = np.ctypeslib.as_array(c_float_array_buffer4)
    result = np.zeros((m, n), np.float32)
    if len(buffer1) == 15000 and len(buffer2) == 15000 and len(buffer3) == 15000 and len(buffer4) == 15000:
        result[:, 0] = buffer1
        result[:, 1] = buffer2
        result[:, 2] = buffer3
        result[:, 3] = buffer4
    return result


def print_non_zero_column(matrix):
    count = 0
    for row in matrix:
        if any(row != 0):
            count += 1
    return count


def push_data_to_matrix(redis_client, origin_buffer_nparray):
    # 将新的矩阵插入到redis中
    redis_client.set_matrix(redis_key_origin_buffer, origin_buffer_nparray)


def get_matrix_from_redis(redis_client, key, m, n):
    result = redis_client.get_matrix(key)
    if result is None:
        return np.zeros((m, n))
    return result


def gen_azimuth_velocity_corrcoef(redis_client, azimuth_ndarray, velocity_ndarray, corrcoef_ndarray, queue_name):
    # 创建一个字典对象
    hash_element = {redis_key_AzimuthCalCallBack_Azimuth: azimuth_ndarray.tolist(),
                    redis_key_AzimuthCalCallBack_Velocity: velocity_ndarray.tolist(),
                    redis_key_AzimuthCalCallBack_Corrcoef: corrcoef_ndarray.tolist()}

    # 将字典对象转换为 JSON 字符串
    json_str = json.dumps(hash_element)

    # 将 JSON 字符串添加到队列中
    redis_client.rpush(queue_name, json_str)
    print(f'AzimuthCalFuncProducer rpush json_str:{json_str}')


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


def read_single_buffer_from_redis(redis_client, key):
    pickled = redis_client.get(key)
    if pickled is not None:
        return pickle.loads(pickled)
    return (ctypes.c_float * 15000)()


def write_single_buffer_to_redis(redis_client, key, value):
    value = list(value)
    pickled = pickle.dumps(value)
    redis_client.set(key, pickled)