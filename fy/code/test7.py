import numpy as np

matrix = np.array([[1,2,3], [4,5,6], [7,8,9]])

with open('./matrix.txt', 'w') as f:
    # 遍历矩阵的行
    for row in matrix:
        # 遍历行的每一列,输出到文件
        for col in row:
            f.write(str(col) + ' ')
        # 换行
        f.write('\n')