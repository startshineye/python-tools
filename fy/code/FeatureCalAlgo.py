#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 特征计算模块
import ctypes


class FeatureCalFunc:
    def __init__(self):
        self.so = ctypes.CDLL("./SOsigprocess.so")

    def time_character_dispersion(self, dataIn, dataLen):
        """
        时域特征：离散度

        :param dataIn:float[] 输入数据
        :param dataLen:uint 数据长度
        :return:dispersion: double 离散度[输出]
        """
        return self.so.cal_Dispersion(dataIn, dataLen)

    def time_character_skewness(self, dataIn, dataLen):
        """
        时域特征：偏斜度

        :param dataIn:float[] 输入数据
        :param dataLen:uint 数据长度
        :return:skewness: double 偏斜度[输出]
        """
        self.so.cal_Skewness(dataIn, dataLen)

    def time_character_peakedness(self, dataIn, dataLen):
        """
        时域特征：峭度

        :param dataIn:float[] 输入数据
        :param dataLen:uint 数据长度
        :return:peakedness: double 峭度[输出]
        """
        self.so.cal_Peakedness(dataIn, dataLen)

    def time_character_zero_crossingrate(self, dataIn, dataLen):
        """
        时域特征：过零率

        :param dataIn:float[] 输入数据
        :param dataLen:uint 数据长度
        :return:zero_crossingrate: double 峭度[输出]
        """
        self.so.cal_Zero_crossingrate(dataIn, dataLen)

    def frequency_character_spectral_roll_off(self, pointer_da, pointer_take, dataLen, sampleRate):
        """

        :param pointer_da:输入数据
        :param pointer_take:处理数据
        :param dataLen:数据长度
        :param sampleRate:采样率
        :return: 结构体: 频谱通量[输出]
        """
        self.so.cal_spectral_roll_off(pointer_da, pointer_take, dataLen, sampleRate)

    def frequency_character_spectral_flux(self, pointer_dataIn, dataLen, step, win):
        return self.so.cal_spectral_flux(pointer_dataIn, dataLen, step, win)

    def frequency_character_spectral_centroid(self, pointer_dataIn, dataLen, win, step):
        return self.so.cal_Spectral_centroid(pointer_dataIn, dataLen, win, step)

    def time_frequency_character_bispecd(self, pointer_dataIn, nfft, wind, nsamp, overlap, nrecs, ly):
        return self.so.cal_bispecd(pointer_dataIn, nfft, wind, nsamp, overlap, nrecs, ly)
