import ctypes
import numpy as np

import numpy as np
import ctypes
n = 5
m = 10
arr = ((ctypes.c_float * n) * m)()

# 假设 arr 是 ((ctypes.c_float * n) * m)() 形状的 ctypes 数组

arr_np = np.frombuffer(arr, dtype=np.float32).reshape((m, n))
print(arr_np)
