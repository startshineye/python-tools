import json
import numpy as np
from RedisUtil import RedisClient

redis_key_azimuth_matrix = 'azimuth_matrix'
redis_key_velocity_matrix = 'velocity_matrix'
redis_key_corrcoef_matrix = 'corrcoef_matrix'


def get_matrix_from_redis(redis_client, key, m, n):
    result = redis_client.get_matrix(key)
    if result is None:
        return np.zeros((m, n))
    return result


def print_data(name, matrix, condValue):
    result = []  # 定义空list
    # 遍历矩阵每个元素
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            # 如果元素不为0或-100.0,添加到list中
            if matrix[i, j] != 0 and matrix[i, j] != condValue:
                result.append(matrix[i, j])
    # 遍历list输出
    for num in result:
        print(f'{name} non {condValue} : {num}')
    return result


if __name__ == '__main__':
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)
    # 从redis队列中获取矩阵：矩阵是15x600
    azimuth_matrix = get_matrix_from_redis(redis_client, redis_key_azimuth_matrix, 15, 600)
    print_data('azimuth_matrix', azimuth_matrix, -1000.0)

    velocity_matrix = get_matrix_from_redis(redis_client, redis_key_velocity_matrix, 15, 600)
    print_data('velocity_matrix', velocity_matrix, -1.0)

    corrcoef_matrix = get_matrix_from_redis(redis_client, redis_key_corrcoef_matrix, 15, 600)
    print_data('corrcoef_matrix', corrcoef_matrix, 0.0)




