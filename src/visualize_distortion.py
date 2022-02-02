from knots import *
from numpy import cos, sin, pi, mgrid, abs, minimum

P = 20
def get_torus_param(P):
    DIRECTIONS = []
    x_len = 2
    sign = 1
    for i in range(1, 2*P - 1):
        y_len = (P - 1) if i % 2 == 1 else P
        DIRECTIONS.append(sign * W * (2*P - i))
        DIRECTIONS.append(sign * D * x_len)
        DIRECTIONS.append(sign * Q * y_len)
        if i % 2 == 1:
            x_len += 1
        sign = -sign
    DIRECTIONS.append(sign * W * 1)
    DIRECTIONS.append(sign * D * P)
    DIRECTIONS.append(sign * Q * (2*P - 1))
    sign = -sign
    DIRECTIONS.append(sign * W * P)
    DIRECTIONS.append(sign * D * 1)
    # DIRECTIONS.append(DIRECTIONS[0]-DIRECTIONS[-1])
    return np.array(DIRECTIONS)
DIRECTIONS = get_torus_param(P)

# DIRECTIONS = np.array([D* 245, Q* 158, S* 71, A* 158, E* 245, W* 158, D* 71, Q* 158, S* 245, A* 158, E* 71])
K = construct_knot(DIRECTIONS, "taxicab")
N = K.num_vertices

a, b = mgrid[0:N, 0:N]
phi = a * (2*pi / N)
theta = b * (2*pi / N)

R, r, max_f_radius = 10, 2, 5
assert R >= r + max_f_radius + 1

x = R*cos(phi) + r*cos(theta)*cos(phi)
y = R*sin(phi) + r*cos(theta)*sin(phi)
z = r*sin(theta)

u = cos(theta)*cos(phi)
v = cos(theta)*sin(phi)
w = sin(theta)

d = K.distortion_ratios["euclidean"]
f = (d / np.amax(d)) * max_f_radius # normalized

mlab.mesh(x + f*u, y + f*v, z + f*w, colormap='cool', scalars=d, scale_mode='none') # plotting f on a torus!
mlab.colorbar()
# mlab.mesh(x, y, z)#, colormap='viridis') # plotting torus
# mlab.quiver3d(x, y, z, u, v, w, scale_mode='none') # plotting normal vectors on torus
mlab.show()