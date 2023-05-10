import numpy as np
from ctypes import *


def matrix_to_c_array(matrix):
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


matrixA = np.random.rand(600, 15)  # 生成600x15矩阵

# 将numpy数组转换为C语言一维数组
c_array = matrix_to_c_array(matrixA)

# 再将C语言一维数组转换为指针
OutputAV = c_array_to_pointer(c_array)
print(OutputAV)