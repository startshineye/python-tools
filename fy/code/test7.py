import ctypes
from RedisUtil import RedisClient
import pickle

# 写入redis
a = (ctypes.c_float * 15000)()
for i in range(15000):
    a[i] = i * 1.1

print(list(a))

a = list(a)
redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)

pickled = pickle.dumps(a)
redis_client.set('a', pickled)

pickled = redis_client.get('a')
a = pickle.loads(pickled)
print(a)

