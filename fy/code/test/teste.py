import ctypes
import numpy as np

def pointer(A):
    # 定义 ctype 指针类型
    OutputAV = ctypes.POINTER(ctypes.c_float * 15)()

    # 将 A 转换成 ctype 数组类型
    A_ctype = (ctypes.c_float * (A.shape[0] * A.shape[1]))(*A.ravel())

    # 将 ctype 数组类型转换成 ctype 指针类型
    ctypes.pythonapi.PyCObject_FromVoidPtr.restype = ctypes.py_object
    ctypes.pythonapi.PyCObject_FromVoidPtr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    OutputAV = ctypes.pythonapi.PyCObject_FromVoidPtr(A_ctype, None)

    return OutputAV

# 测试数据
A = np.random.rand(600, 15).astype(np.float32)

# 将 A 转换成指针类型
ptr = pointer(A)

# 将指针类型转换成 B 矩阵
B = np.zeros((15, 600), dtype=np.float32)
for i in range(15):
    B[i] = np.ctypeslib.as_array(ptr[i], shape=(600,))

# 打印矩阵 B
print(B)
