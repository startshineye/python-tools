from RedisUtil import RedisClient
import numpy as np

redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)
# 创建一个 Numpy 矩阵
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(type(matrix))
key = '11111'
redis_client.set_matrix(key, matrix)
get = redis_client.get_matrix(key)
print(get)
print(type(get))
m = 15
n = 60

azimuth_matrix = np.zeros((m, n))

print(type(azimuth_matrix))

