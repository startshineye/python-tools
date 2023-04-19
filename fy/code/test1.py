from RedisUtil import RedisClient
import numpy as np

# 连接Redis
redis_client = RedisClient(host='localhost', password='Founder123', port=6379, db=0)

# 构造一个3x2矩阵
matrix = np.array([[1, 2], [3, 4], [5, 6]])


print(f'matrix:{matrix}')

# 序列化矩阵并存储到Redis
redis_client.set('matrix', matrix.tobytes())

print(f'matrix.tobytes():{matrix.tobytes()}')

# 读取并反序列化
s = redis_client.get('matrix')
print(f'matrix s:{s}')
matrix = np.fromstring(s, dtype=np.int32)

print(f'matrix redis:{matrix}')
matrix = matrix.reshape((3, 4))

print(f'matrix after:{matrix}')




