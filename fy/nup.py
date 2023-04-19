import numpy as np
import ctypes

# 初始化一个15x60数组
# y = np.zeros((15, 60), dtype=float)
y = np.zeros((15, 15), dtype=float)
print(f'type(y){type(y)}')

# 定义一个15x1
amuz = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
array = np.array(amuz)
reshape = array.reshape(1, 15)
print(reshape)

# 转换后数组
t = reshape.T
print(t)

add = np.insert(y, [0], t, axis=1)
print(add)
print(type(add))

minus = np.delete(add, [1], axis=1)
print(minus)

print(type(minus))
print(type(array))

array_ctype = np.ctypeslib.as_ctypes(minus)
print(type(array_ctype))
# minus_ctype = np.ctypeslib.as_ctypes(minus)
# print(type(minus_ctype))







