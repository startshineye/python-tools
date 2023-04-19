#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 次声定位模块
import ctypes
from ctypes import *


# 阵列A0点坐标-结构体
class emxArray_real_T(Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.POINTER(ctypes.c_double))),
        ("size", ctypes.POINTER(ctypes.c_int)),
        ("allocatedSize", c_int),
        ("numDimensions", c_int),
        ("canFreeData", ctypes.c_bool)
    ]


# 置信椭圆---结构体
class struct0_T(Structure):
    _fields_ = [
        ("semimajor", c_double),
        ("semiminor", c_double),
        ("ecc", c_double),
        ("psi", c_double),
        ("Lat99", c_double * 100),
        ("Lon99", c_double * 100),
    ]


# 求取比某个数大的2的次方的最小数
def next_power_of_2(n):
    # 如果 n 已经是 2 的次方，则直接返回 n
    if n and not (n & (n - 1)):
        return n

    # 从 2^0 开始，不断倍增
    p = 1
    while p < n:
        p <<= 1
    return p


def get_emxArray_real_T(data, m, n):
    # 初始化一个3x2的二维数组
    # 将二维数组的每一行转换成指向double类型的指针
    data_ptrs = [ctypes.cast((ctypes.c_double * len(row))(*row), ctypes.POINTER(ctypes.c_double)) for row in data]
    # 初始化一个一维数组
    size = (ctypes.c_double * 2)(m, n)
    # 创建一个结构体实例并设置其成员变量的值
    return emxArray_real_T(data=ctypes.cast((ctypes.POINTER(ctypes.c_double) * len(data_ptrs))(*data_ptrs),
                                            ctypes.POINTER(ctypes.POINTER(ctypes.c_double))),
                           size=ctypes.cast(size, ctypes.POINTER(ctypes.c_int)),
                           allocatedSize=next_power_of_2(m * n),
                           numDimensions=2,
                           canFreeData=True
                           )


class InfraLocFunc:
    def __init__(self):
        self.so = ctypes.CDLL("./SOInfraLoc.so")

    def setData(self, arrLatLon, theta_tilde, noiseVard, p_SWPLE_hat, elps, runTime):
        self.arrLatLon = arrLatLon
        self.theta_tilde = theta_tilde
        self.noiseVard = noiseVard
        self.p_SWPLE_hat = p_SWPLE_hat
        self.elps = elps
        self.runTime = runTime

    def InfraLoc(self):
        self.so.InfraLoc(self.arrLatLon, self.theta_tilde, self.noiseVard, self.p_SWPLE_hat, self.elps, self.runTime)


if __name__ == '__main__':
    arrLatLon_data = [[38.4296, -118.3036], [48.2641, -117.1257], [33.6064, -116.4550]]
    arrLatLon = get_emxArray_real_T(arrLatLon_data, 3, 2)
    arrLatLon_pointer = ctypes.pointer(arrLatLon)

    theta_tilde_data = [[56.6], [157.5], [17.6]]
    theta_tilde = get_emxArray_real_T(theta_tilde_data, 3, 1)
    theta_tilde_pointer = ctypes.pointer(theta_tilde)

    noiseVard_data = [[0], [0], [0]]
    noiseVard = get_emxArray_real_T(theta_tilde_data, 3, 1)
    noiseVard_pointer = ctypes.pointer(noiseVard)

    # 输出结果
    p_SWPLE_hat = (c_double * 2)(0, 0)

    elps = struct0_T()
    print(elps)

    elps_pointer = ctypes.pointer(elps)
    print(elps_pointer)

    runTime_pointer = ctypes.pointer(c_double(0))
    print(runTime_pointer)

    # 函数调用
    func = InfraLocFunc()
    func.setData(arrLatLon, theta_tilde, noiseVard, p_SWPLE_hat, elps_pointer, runTime_pointer)
    # func.InfraLoc()

    print(func.p_SWPLE_hat)
    print(func.elps)
    print(func.runTime)

    '''
    void InfraLoc(const emxArray_real_T *arrLatLon, emxArray_real_T *theta_tilde,
              const emxArray_real_T *noiseVard, double p_SWIVE_hat[2],
              struct0_T *elps, double *runTime)
    '''
