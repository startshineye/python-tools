#! /usr/bin/env python
# -*- coding=utf-8 -*-
# https://www.jianshu.com/p/89cb36f3fd7b

# filename: main.py
from ctypes import *

a = [[0 for i in range(2)] for j in range(5)]
print(a)

c = (c_float * 15)(150,150,150,150,150,150,150,150,150,150,150,150,150,150,150)
for i in range(len(c)):
    print(c[i])


class SysParameters(Structure):
    _fields_ = [
        ("windowLen", (c_float * 15)(150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150)),
        ("freqBins", (c_float * 15)(0.01, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0000)),
        ("csThd", (c_float * 15)(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)),
        ("corrThd", (c_float * 15)(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)),
        ("sigma_A", (c_float * 15)(20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20)),
        ("sigma_V", (c_float * 15)(0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2)),
        ("sigma_T", c_float(20)),
        ("timeThd", c_float(20)),
        ("nFamilyMax", c_int(1000)),
        ("nFamilyMin", c_int(2)),
        ("ThresholdDistance", c_float(1.5)),
        ("VelocityMax", c_float(1000)),
        ("VelocityMin", c_float(200)),
        ("sigma_V", (c_float * 15)(50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50)),
        ("sigma_V", (c_float * 15)(0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01)),
        ("overlapRate", c_float(0.9)),
    ]