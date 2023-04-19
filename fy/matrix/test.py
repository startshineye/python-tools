'''
你可以使用NumPy库来创建和操作矩阵，同时使用time库来实现定时器功能。下面是一个示例代码，
实现了每10秒将5x1的数据插入到一个5x5的矩阵中，并移除最前元素。

在上面的代码中，我们首先创建一个5x5的零矩阵matrix。然后，进入一个无限循环，每次循环中，我们首先创建一个5x1的随机向量vector，然后使用np.concatenate函数将该向量插入到矩阵末尾，同时移除最前元素。最后，输出当前矩阵，暂停10秒后，进入下一次循环。
请注意，上述示例代码仅为演示如何使用NumPy库和time库实现定时器功能，实际使用时需要根据具体需求进行修改。另外，由于这是一个无限循环，因此需要手动停止程序。
'''

import numpy as np
import time

# 创建一个5x5的零矩阵
matrix = np.zeros((5, 5))

while True:
    # 创建一个5x1的随机向量
    vector = np.random.rand(5, 1)

    # 将向量插入到矩阵末尾
    matrix = np.concatenate((matrix[:, 1:], vector), axis=1)

    # 输出当前矩阵
    print(matrix)

    # 暂停10秒
    time.sleep(10)
