import nup as np
import ctypes
from ctypes import *
'''
t = ((c_float * 60) * 15)()

for v in t:
    for v1 in v:
        print(v1, end=",")
'''


float_ = (c_float * 15)()
print(float_.value)

a = np.arange(4)
print(a)

p = np.insert(a, 4, 100)
print(p)
x = np.delete(p, 0)
print(x)
