import ctypes
import time
import numpy as np
from datetime import datetime

# 定义数据类型
float_type = ctypes.c_float

# 打开5个bin文件
f1 = open('../data/xKEL1.bin', 'rb')
f2 = open('../data/xKEL2.bin', 'rb')
f3 = open('../data/xKEL3.bin', 'rb')
f4 = open('../data/xKEL4.bin', 'rb')
f5 = open('../data/xKEL5.bin', 'rb')

# 定义5个一维buffer,每个长度15000
buffer1 = (float_type * 15000)()
buffer2 = (float_type * 15000)()
buffer3 = (float_type * 15000)()
buffer4 = (float_type * 15000)()
buffer5 = (float_type * 15000)()

# 定义数据类型
float_type = np.float32

# 读取并推送数据,每10秒推1000个
start = time.time()
while True:
    if time.time() - start > 2:
        print(f'开始计数:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        # 读取1000个元素
        data1 = np.frombuffer(f1.read(4000), np.float32)
        data2 = np.frombuffer(f2.read(4000), np.float32)
        data3 = np.frombuffer(f3.read(4000), np.float32)
        data4 = np.frombuffer(f4.read(4000), np.float32)
        data5 = np.frombuffer(f5.read(4000), np.float32)

        #data1 = np.frombuffer(f1.read(1000 * np.float32.itemsize), np.float32)
        #data2 = np.frombuffer(f2.read(1000 * np.float32.itemsize), np.float32)
        # ...

        # 移除buffer头部1000个元素
        buffer1 = buffer1[1000:] + data1.tolist()
        buffer2 = buffer2[1000:] + data2.tolist()
        buffer3 = buffer3[1000:] + data3.tolist()
        buffer4 = buffer4[1000:] + data4.tolist()
        buffer5 = buffer5[1000:] + data5.tolist()
        # ...
        print("-------------------------------------------------------------------")
        print(len(buffer1))

        # 定义15000x5的二维数组
        result = (ctypes.c_float * 5) * 15000

        # 将5个一维buffer复制到result
        result[:15000] = buffer1
        result[15000:30000] = buffer2
        result[30000:45000] = buffer3
        result[45000:60000] = buffer4
        result[60000:75000] = buffer5

        start = time.time()
