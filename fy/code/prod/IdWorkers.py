#! /usr/bin/env python
# -*- coding=utf-8 -*-
# id生成器
import hashlib
import time


def nextId():
    return hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()


class IdWorker:
    pass


if __name__ == '__main__':
    for i in range(10):
        print(nextId())
