import ctypes

c_array = ((ctypes.c_float * 3) * 2)()   # 创建2x3的数组
c_array[0][1] = 2.2     # 元素赋值
c_array[1][2] = 3.3

print(c_array)

# 记录非0和-1元素的坐标
coordinates = []
for i in range(2):
    for j in range(3):
        if c_array[i][j] != 0 and c_array[i][j] != -1:
            coordinates.append((i, j))

print(coordinates)
# [(0, 1), (1, 2)]