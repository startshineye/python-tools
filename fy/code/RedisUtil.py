#! /usr/bin/env python
# -*- coding=utf-8 -*-
# redis-tools

import redis
import numpy as np
import json


class RedisClient:
    def __init__(self, host, port, password, db):
        self.host = host
        self.port = port
        self.db = db
        self._conn = redis.Redis(host=host, port=port, password=password, db=db)

    def set(self, key, value):
        self._conn.set(key, value)

    def get(self, key):
        return self._conn.get(key)

    def delete(self, key):
        self._conn.delete(key)

    def hmset(self, key, mapping):
        self._conn.hmset(key, mapping)

    def hmget(self, key, fields):
        return self._conn.hmget(key, fields)

    def hdel(self, key, fields):
        self._conn.hdel(key, *fields)

    def rpush(self, key, fields):
        json_str = json.dumps(fields)
        self._conn.rpush(key, json_str)

    def lpop(self, key):
        json_str = self._conn.lpop(key)
        if json_str is None:
            return None
        return json.loads(json_str)

    def set_matrix(self, key, matrix):
        serialized_matrix = matrix.dumps()
        self._conn.set(key, serialized_matrix)

    def get_matrix(self, key):
        serialized_matrix = self._conn.get(key)
        print(serialized_matrix)
        if serialized_matrix is None:
            return None
        return np.loads(serialized_matrix)
