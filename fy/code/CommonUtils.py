#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 公共方法

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