import random
import json
import numpy as np

# 定义矩阵A1
A1 = np.array([[-1, -1, -1, -1, -1],
               [1, 1, 1, 1, 1],
               [2, 2, -1, 2, 2],
               [3, 3, 3, 3, 3],
               [4, 4, 4, 4, 4]])

# A2和A3是随机数矩阵
A2 = np.random.rand(5, 5)
A3 = np.random.rand(5, 5)
print("----------------A2--------------------")
print(A2)

print("----------------A3--------------------")
print(A3)

# 找到A1中非-1元素的坐标
coord1 = []
for i in range(5):
    for j in range(5):
        if A1[i, j] != -1:
            coord1.append((i, j))

print("----------------coord1--------------------")
print(coord1)


print("----------------result--------------------")
# 生成json1和json2
json1 = {}
json2 = {}
for x, y in coord1:
    if A1[x, y] in json1:
        json1[A1[x, y]] += ',' + str(A2[x, y])
    else:
        json1[A1[x, y]] = str(A2[x, y])
    json2[A1[x, y]] = str(A3[x, y])

# 显示结果
print(json1)
print(json2)