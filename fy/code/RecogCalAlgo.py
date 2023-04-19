#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 识别模块

import ctypes
from ctypes import *


# 自定义基类结构体
class Svm_Model(Structure):
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


class RecogCalFunc:
    def __init__(self):
        self.so = ctypes.CDLL("./SOrecog.so")

    def model_load(self, model_file_name):
        return self.so.model_load(model_file_name)

    def read_csv_problem(self, input_file_name):
        return self.so.read_csv_problem(input_file_name)

    def model_pred(self):
        return self.so.model_pred()
