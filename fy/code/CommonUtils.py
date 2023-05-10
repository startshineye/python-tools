#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 公共方法
import ctypes
import numpy as np

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

def non_zero_rows_matrix_calculate(np_array):
    if np_array is None:
        return 0
    rows = np_array.shape[0]
    non_zero_rows = 0
    for i in range(rows):
        if np.all(np_array[i] == 0):
            continue
        non_zero_rows += 1
    return non_zero_rows

def non_zero_rows_matrix_calculate(np_array):
    if np_array is None:
        return 0
    rows = np_array.shape[0]
    non_zero_rows = 0
    for i in range(rows):
        if np.all(np_array[i] == 0):
            continue
        non_zero_rows += 1
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


def non_zero_cols_matrix_calculate(np_array):
    cols = np_array.shape[1]
    if np_array is None:
        return 0
    non_zero_cols = 0
    for j in range(cols):
        if np.all(np_array[:,j] == 0):
            continue
        non_zero_cols += 1
    return non_zero_cols