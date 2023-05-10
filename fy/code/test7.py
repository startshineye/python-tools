import numpy as np

A = np.array([[1,2,3], [0,0,0], [4,5,6], [0,0,0]])

rows = A.shape[0]

non_zero_rows = 0
for i in range(rows):
    if np.all(A[i] == 0):
        continue
    non_zero_rows += 1

print(non_zero_rows)