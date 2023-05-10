import redis
from RedisUtil import RedisClient
redis_client = redis.Redis(host='localhost', port=6379, password='Founder123', db=0)

keys = redis_client.keys()

if keys:
    redis_client.delete(*keys)