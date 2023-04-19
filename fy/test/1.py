import ctypes

# 定义c_float数组
c_arr = (ctypes.c_float*3)(1.2, 2.3, 3.4)

# 定义空字符串数组
str_arr = []

# 遍历c_float数组
for num in c_arr:
    # 使用str()函数转换为字符串
    str_arr.append(str(num))

print(str_arr)
# ['1.2', '2.3', '3.4']

print(','.join(str_arr))