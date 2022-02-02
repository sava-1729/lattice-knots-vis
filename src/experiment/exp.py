import mayavi.mlab as mlab
import numpy as np
from random import random
from time import perf_counter

N = 10000000

# x = np.array([random() for i in range(N)])
x = np.arange(N)

# lt = np.tril(np.ones((N, N), dtype=np.uint8))

# t1 = perf_counter()
# y = lt @ x
# t2 = perf_counter()
# print("Matrix vector multiplication in numpy, time elapsed: %f s" % (t2-t1))


############### FASTEST METHOD! #################
t1 = perf_counter()
y = np.empty(N, dtype=np.uint8)
last_sum = 0
for i in range(N):
    last_sum += x[i]
    y[i] = last_sum
t2 = perf_counter()
print("Iterating over array in numpy and summing manually, time elapsed: %f s" % (t2-t1))

