'''
1、python定义一个方法将600x15的矩阵A转换成c语言中 ctype中15维度 每一个维度为600个数的指针:float (*OutputAV)[15]
'''
import ctypes
import numpy as np


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
    # 将OutputAV转换为numpy数组
    B = np.frombuffer(ctypes.cast(OutputAV, ctypes.POINTER(ctypes.c_float * 15 * 600)).contents, dtype=np.float32)
    # 重新reshape为600x15的矩阵
    B = B.reshape((600, 15))
    print(B)


if __name__ == '__main__':
    A = np.random.rand(600, 15)

    # print(A)
    OutputAV = convert_to_pointer(A)

    # 将C语言中的指针转换为NumPy数组
    #matrix = np.ctypeslib.as_array(OutputAV)
    # print(matrix)

    # 将OutputAV转换为numpy数组
    # B = np.frombuffer(ctypes.cast(OutputAV, ctypes.POINTER(ctypes.c_float * 15 * 600)).contents, dtype=np.float32)
    # 重新reshape为600x15的矩阵
    # B = B.reshape((600, 15))
    B = convert_pointer_to_matrix(OutputAV)
    print(B)

    # 输出OutputAV_A的值
    # for i in range(15):
    #    print(pointer[i][:5])

    # 打印输出OutputAV指针的数据
