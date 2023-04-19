import ctypes

# 定义c_float数组
c_arr = (ctypes.c_float*3)(1.2, 2.3, 3.4)

# 定义空字符串
rs = ''

# 遍历c_float数组
for num in c_arr:
    rs += str(num) + ','  # 添加字符串并连接逗号

# 去除最后一个逗号
rs = rs[:-1]

print(rs)
# 1.2,2.3,3.4