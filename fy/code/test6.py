import ctypes
import numpy as np

# 定义数据类型
float_type = ctypes.c_float

# 定义5个一维buffer,每个长度15000
buffer1 = (float_type * 15000)()
buffer2 = (float_type * 15000)()
buffer3 = (float_type * 15000)()
buffer4 = (float_type * 15000)()
buffer5 = (float_type * 15000)()

print(type(buffer1))

# 定义15000x5的二维数组
buffer1 = np.ctypeslib.as_array(buffer1)
buffer2 = np.ctypeslib.as_array(buffer2)
buffer3 = np.ctypeslib.as_array(buffer3)
buffer4 = np.ctypeslib.as_array(buffer4)
buffer5 = np.ctypeslib.as_array(buffer5)
print(type(buffer1))

# result = (float_type * 5) * 15000
# result = (np.float32 * 5) * 15000
# result = np.float32 * (5 * 15000)
result = np.zeros((15000, 5), np.float32)

'''
result[:15000, 0] = buffer1
result[15000:30000, 0] = buffer2
result[30000:45000, 0] = buffer2
result[45000:60000, 0] = buffer2
result[60000:75000, 0] = buffer2
'''

# 将5个一维buffer复制到result
# 赋值给result
result[:, 0] = buffer1
result[:, 1] = buffer2
result[:, 2] = buffer3
result[:, 3] = buffer4
result[:, 4] = buffer5

print(type(result))

def ndarray_to_ctype_array(src, m, n):
    b = (ctypes.c_float * n) * m
    c = b()

    for i in range(m):
        for j in range(n):
            c[i][j] = src[i][j]

    return c


'''
b = (ctypes.c_float * 5) * 15000
c = b()

for i in range(15000):
    for j in range(5):
        c[i][j] = result[i][j]
'''

array = ndarray_to_ctype_array(result, 15000, 5)
print(array)
