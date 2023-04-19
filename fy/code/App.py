import ctypes
import numpy as np
import time
from AzimuthCalAlgo import AzimuthCalFunc
from FamilyClusterAlgo import FamilyClusterFunc


def print_ctypes_array(arr, file_name):
    c_arr = (ctypes.c_float * (len(arr) * len(arr[0])))(*np.ravel(arr).astype(np.float32))
    # 将c_float类型的二维数组转换成NumPy数组
    np_arr = np.ctypeslib.as_array(c_arr).reshape((len(arr), len(arr[0])))
    # 以矩阵形式输出c_float二维数组
    np.savetxt(file_name, np_arr, fmt="%.2f", delimiter=" ")
    # 遍历输出c_float二维数组
    # for i in range(len(np_arr)):
    #    for j in range(len(np_arr[i])):
    #        print(np_arr[i][j])


if __name__ == '__main__':

    # 1、方位角计算
    func = AzimuthCalFunc()
    func.AzimuthCalCallBack()
    azimuth = func.Azimuth
    velocity = func.Velocity
    corrcoef = func.Corrcoef
    # 定义一个1x15的c_float数组

    m = 15
    n = 60
    # m = 5
    # n = 5
    # azimuth = (ctypes.c_float * m)()

    OutputAV = ((ctypes.c_float * n) * m)()

    # 将c_float数组转换成15x1的向量
    azimuth_vector = np.ctypeslib.as_array(azimuth).reshape((m, 1))
    velocity_vector = np.ctypeslib.as_array(velocity).reshape((m, 1))
    corrcoef_vector = np.ctypeslib.as_array(corrcoef).reshape((m, 1))

    # 创建一个15x60的零矩阵
    azimuth_matrix = np.zeros((m, n))
    velocity_matrix = np.zeros((m, n))
    corrcoef_matrix = np.zeros((m, n))


    while True:
        # 更新向量中的元素
        # for i in range(5):
        #    arr[i] = ctypes.c_float(np.random.rand())

        # 将向量插入到矩阵末尾
        azimuth_matrix = np.concatenate((azimuth_matrix[:, 1:], azimuth_vector), axis=1)
        velocity_matrix = np.concatenate((velocity_matrix[:, 1:], velocity_vector), axis=1)
        corrcoef_matrix = np.concatenate((corrcoef_matrix[:, 1:],  corrcoef_vector), axis=1)

        # 输出当前矩阵
        print(azimuth_matrix)

        # 将矩阵转换成c_float类型的二维数组
        matrixA = (ctypes.c_float * (m * n))(*np.ravel(azimuth_matrix).astype(np.float32))
        matrixV = (ctypes.c_float * (m * n))(*np.ravel(velocity_matrix).astype(np.float32))
        matrixC = (ctypes.c_float * (m * n))(*np.ravel(corrcoef_matrix).astype(np.float32))
        # 使用reshape函数将一维数组转换成二维数组
        matrixA = np.ctypeslib.as_array(matrixA).reshape((m, n))
        matrixV = np.ctypeslib.as_array(matrixV).reshape((m, n))
        matrixC = np.ctypeslib.as_array(matrixC).reshape((m, n))

        # 2、PMCC计算
        FamilyClusterFunc(OutputAV, matrixA, matrixV, matrixC)

        # 数据打印
        print_ctypes_array(OutputAV, "../output.txt")
        # 暂停10秒
        time.sleep(100)


