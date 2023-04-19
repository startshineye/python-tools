import redis
import numpy as np
from RedisUtil import RedisClient
import json

# 连接 Redis 数据库
r  = redis.Redis(host='localhost', port=6379, password='Founder123', db=0)


# 定义一个队列的名称
queue_name = 'myqueue'

# 生成一个 15x1 的数组
myarray = np.random.rand(15, 1)

# 将数组转换为 Python List 对象
mylist = myarray.tolist()

# 创建一个字典对象
hash_element = {'k1': mylist}

# 将字典对象转换为 JSON 字符串
json_str = json.dumps(hash_element)

# 将 JSON 字符串添加到队列中
r.rpush(queue_name, json_str)

# 从队列中获取元素
queue_length = r.llen(queue_name)
for i in range(queue_length):
    # 从队列左侧取出元素
    json_str = r.lpop(queue_name)

    # 将 JSON 字符串转换为字典对象
    hash_element = json.loads(json_str)

    # 获取数组的值
    array_value = hash_element['k1']

    # 将数组恢复为 numpy 数组对象
    array_obj = np.array(array_value)

    # 打印出数组的内容
    print(array_obj)
