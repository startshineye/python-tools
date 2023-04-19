import nup as np
import ctypes
OutputAV = ((ctypes.c_float * 60) * 15)()
for o in OutputAV:
    print(o)

n = np.array([])
print(n)
print(n.__add__([1, 3, 2]))
# 定义 3*3 的 numpy 数组
matrix = np.array([[1, 3, 2],
                   [8, 0, 6],
                   [9, 7, 0]])
print(matrix)

# 提取第1、3列（行的提取同理）
matrix1 = matrix[:, [0, 2]]
print(matrix1)

# 提取第1、2行（列的提取同理）
matrix2 = matrix[[0, 1], :]
print(matrix2)

