#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 次声预处理模块
import ctypes
from ctypes import *


class InfraPreprocFunc:
    def __init__(self, file_path):
        self.so = ctypes.CDLL("./SOInfraPreproc.so")
        self.file_path = file_path

    def InfraPreproc(self, wvfrm_raw, wvfrm_proc):
        self.so.InfraPreproc(wvfrm_raw, wvfrm_proc)

    def get_origin_data(self):
        c_float_array = (c_double * 75000)()
        with open(self.file_path, 'r') as f:
            readlines = f.readlines()
            for i in range(len(readlines)):
                line = readlines[i]
                ar = line.strip().split("   ")
                if len(ar) < 5:
                    tmp = line.strip().split("  ")
                else:
                    tmp = ar
                len_n = len(tmp)
                for j in range(len(tmp)):
                    # print(f'i:{i} j:{j}')
                    c_float_array[i * len_n + j] = float(tmp[j])
        return ctypes.pointer(c_float_array)


if __name__ == '__main__':
    # 输出函数
    wvfrm_proc =((c_double * 75000)())
    wvfrm_proc_pointer = ctypes.pointer(wvfrm_proc)

    func = InfraPreprocFunc("./testWvfrm_origin.txt")
    origin_data = func.get_origin_data()
    print(wvfrm_proc)
    print(origin_data)

    func.InfraPreproc(origin_data, wvfrm_proc_pointer)
    print(wvfrm_proc_pointer)
    for i in range(len(wvfrm_proc)):
        print(wvfrm_proc_pointer[i])


