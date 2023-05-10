#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 公共方法
import ctypes
import numpy as np
from ctypes import *


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
