
import time
import redis

# 连接Redis
r = redis.Redis(host='localhost', port=6379, db=0, password='Founder123')

# 矩阵的行数和列数
row, col = 3, 5

# 矩阵队列的键
key = 'matrix'

# 初始化空矩阵队列
r.set(key, "")

# 循环开始
while True:
    # 构造一列输入
    input = ['1', '2', '3']

    join = ",".join(input)
    print(join)
    print(type(join))

    print(r.get(key))

    # 拼接一列输入到矩阵左边
    r.set(key, ",".join(input) + str(r.get(key)))

    # 获取矩阵并切割为二维列表
    matrix = [list(map(str, row.split(','))) for row in str(r.get(key)).split('\n')]

    # 删除矩阵最右一列
    matrix = [row[:-1] for row in matrix]
    r.set(key, "\n".join([",".join(map(str, row)) for row in matrix]))

    # 等待10秒
    time.sleep(10)