from RedisUtil import RedisClient
import numpy as np

queue_name = 'data_queue'
redis_key_azimuth_matrix = 'azimuth_matrix'
redis_key_velocity_matrix = 'velocity_matrix'
redis_key_corrcoef_matrix = 'corrcoef_matrix'

redis_key_AzimuthCalCallBack_Azimuth = 'AzimuthCalCallBack_Azimuth'
redis_key_AzimuthCalCallBack_Velocity = 'AzimuthCalCallBack_Velocity'
redis_key_AzimuthCalCallBack_Corrcoef = 'AzimuthCalCallBack_Corrcoef'


redis_client = RedisClient(host='localhost', port=6379, password='Founder123', db=0)

# 生成一个 15x1 的数组
myarray = np.random.rand(15, 1)

# 创建一个 Hash 对象
hash_element = {redis_key_AzimuthCalCallBack_Azimuth: myarray.tolist(),
                redis_key_AzimuthCalCallBack_Velocity: myarray.tolist(),
                redis_key_AzimuthCalCallBack_Corrcoef: myarray.tolist()
                }

redis_client.rpush(queue_name, hash_element)