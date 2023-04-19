
import numpy as np
import ctypes

# 创建一个二维NumPy数组
a = np.array([[1, 2], [3, 4]], dtype=np.float64)

print(a)
print(type(a))

# 转换为ctypes类型
a_ctype = np.ctypeslib.as_ctypes(a)

# 获取数组的大小和形状
rows, cols = a.shape

# 定义C/C++函数的参数类型
# my_func = ctypes.cdll.LoadLibrary("my_lib.so").my_function
# my_func.argtypes = [ctypes.POINTER(ctypes.c_double * cols)] * rows, ctypes.c_int

# 调用C/C++动态链接库的函数
# result = my_func(a_ctype, rows)
