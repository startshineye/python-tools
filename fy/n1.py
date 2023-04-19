import hashlib
import time

def next_power_of_2(n):
    # 如果 n 已经是 2 的次方，则直接返回 n
    if n and not (n & (n - 1)):
        return n

    # 从 2^0 开始，不断倍增
    p = 1
    while p < n:
        p <<= 1
    return p


if __name__ == '__main__':
    of__ = next_power_of_2(10240)
    print(of__)
    for i in range(100):
        hexdigest = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()
        print(hexdigest)

