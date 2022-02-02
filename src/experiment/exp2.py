from turtle import rt
import numpy as np
from time import perf_counter

x = np.array((np.e*100, np.e*200, np.e*300))
y = np.array((np.pi*0.1, np.pi*0.2, np.pi*0.3))

EPSILON = 2**-53
ABS_TOL = 1e-10

t1 = perf_counter()
parallel = np.allclose(np.cross(x, y), np.zeros(3), rtol=0)
print(parallel)
t2 = perf_counter()

print("Cross product in numpy, time elapsed: %f s" % (t2-t1))

t1 = perf_counter()
parallel = np.allclose(x/np.sqrt(np.sum(x**2)), y/np.sqrt(np.sum(y**2)), rtol=0)
print(parallel)
t2 = perf_counter()

print("Normalizing in numpy, time elapsed: %f s" % (t2-t1))
