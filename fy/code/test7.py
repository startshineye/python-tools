import numpy as np
import ctypes

# 创建一个 (ctypes.c_float * 5) 对象
my_c_array = (ctypes.c_float * 5)()

# 填充一些数据
for i in range(5):
    my_c_array[i] = i


print(f'my_c_array:{type(my_c_array)}')
# 将 ctypes 对象转换为 bytes 对象
my_bytes = ctypes.cast(my_c_array, ctypes.POINTER(ctypes.c_float * 5)).contents

# 将 bytes 对象转换为 numpy 数组
my_np_array = np.frombuffer(my_bytes, dtype=np.float32)
print(f'my_np_array:{type(my_np_array)}')

print(my_np_array)

