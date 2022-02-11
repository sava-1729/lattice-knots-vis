from knots_new import *
from numpy import cos, sin, pi, mgrid, abs, minimum
from parameterizations import *

def visualize_distortion(knot, plot_knot=False, cmap="cool"):
    if plot_knot:
        mlab.figure(bgcolor=(0,0,0))
        knot.plot()
    N = knot.num_vertices

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


    d = knot.distortion_ratios["euclidean"]
    f = (d / np.amax(d)) * max_f_radius # normalized

    mlab.figure(bgcolor=(0,0,0))
    # mlab.mesh(x, y, z)#, colormap='viridis') # plotting torus
    # mlab.quiver3d(x, y, z, u, v, w, scale_mode='none') # plotting normal vectors on torus
    mlab.mesh(x + f*u, y + f*v, z + f*w, colormap=cmap, scalars=d, scale_mode="none") # plotting f on torus!
    mlab.colorbar()

DIRECTIONS = get_smooth_torus_knot(3, 4, 1, num_points=500)
K = StickKnot(DIRECTIONS, validate=False, compute_distortion=True, mode="euclidean")
visualize_distortion(K, plot_knot=False, cmap="plasma")
mlab.show()
