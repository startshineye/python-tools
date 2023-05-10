import numpy as np


# 读取文件并转换为矩阵
def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        matrix = np.zeros((len(lines), 15))
        for i, line in enumerate(lines):
            row = line.strip().split(',')
            for j, val in enumerate(row):
                matrix[i][j] = float(val)
        return matrix


# 读取三个文件并转换为矩阵
matrixA = read_file('./f/matrixA.txt')
matrixV = read_file('./f/matrixV.txt')
matrixC = read_file('./f/matrixC.txt')

print(f'type:{type(matrixA)}')
print(f'matrixA:{matrixA}')