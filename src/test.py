from knots_new import *
from parameterizations import *
from time import perf_counter

DIRECTIONS = get_smooth_torus_trefoil(2, num_points=500)
mlab.figure(bgcolor=(0,0,0))
t1 = perf_counter()
T = StickKnot(DIRECTIONS, validate=True, compute_distortion=True, mode="euclidean")
print(T.vertex_distortion)
T.plot()
print(perf_counter()-t1)
mlab.show()
