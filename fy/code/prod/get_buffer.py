import numpy as np
from RedisUtil import RedisClient

redis_key_origin_buffer = 'origin_buffer'


def get_matrix_from_redis(redis_client, key, m, n):
    result = redis_client.get_matrix(key)
    if result is None:
        return np.zeros((m, n))
    return result


if __name__ == '__main__':
    redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)
    ndarray = get_matrix_from_redis(redis_client, redis_key_origin_buffer, 15000, 4)
    print(f'ndarray:{ndarray}')
