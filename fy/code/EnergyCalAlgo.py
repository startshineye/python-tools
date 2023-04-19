#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 当量估计EnergyCalFunc

import ctypes
from ctypes import *


# 自定义基类结构体
class SysParameters(Structure):
    _fields_ = [
        ("windowLen", c_float * 15),
        ("freqBins", c_float * 15),
        ("csThd", c_float * 15),
        ("corrThd", c_float * 15),
        ("sigma_A", c_float * 15),
        ("sigma_V", c_float * 15),

        ("sigma_F", c_float),
        ("sigma_T", c_float),
        ("timeThd", c_float),
        ("nFamilyMax", c_int),
        ("nFamilyMin", c_int),
        ("ThresholdDistance", c_float),

        ("VelocityMax", c_float),
        ("VelocityMin", c_float),
        ("freqHighLim", c_float * 15),
        ("freqLowLim", c_float * 15),
        ("overlapRate", c_float),
    ]


# 初始化结构体
sp = SysParameters((150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150),
                   (0.01, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.0000),
                   (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                   (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),
                   (20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20),
                   (0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2),
                   0.3,
                   20,
                   20,
                   1000,
                   2,
                   1.5,
                   1000,
                   200,
                   (50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50),
                   (0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01),
                   0.9)


class EnergyCalFunc:
    def __init__(self):
        self.so = ctypes.CDLL("./SOEnergyCalFunc.so")
        self.nCHState = ctypes.pointer((c_int * 5)(0, 0, 0, 0, 0))
        self.pCH1D = ctypes.pointer((c_float * 15000)())
        self.nsigLen = c_int(15000)
        self.Fs = c_float(100)
        self.nDimMic = c_int(5)
        self.ArrFlag = c_int(5)
        self.Resolution = c_float(100)
        self.DistS2A = c_float(500)
        self.windSpeed = c_float(20)
        self.weather = c_int(1)
        self.earthquake = c_int(1)
        self.LowLimFreq = c_float(0.01)
        self.HighLimFreq = c_float(20)
        self.sp = sp

    def energyESTCallBack(self):
        return self.so.EnergyESTCallBack(self.nCHState, self.pCH1D, self.nsigLen, self.Fs,
                                         self.nDimMic, self.ArrFlag, self.Resolution, self.DistS2A, self.windSpeed,
                                         self.weather, self.earthquake,
                                         self.sp, self.LowLimFreq, self.HighLimFreq)


if __name__ == '__main__':
    func = EnergyCalFunc()
    back = func.energyESTCallBack()
    print(back)
