from knots_new import *
from numpy import cos, sin, pi, mgrid, abs, minimum
from parameterizations import *
from tvtk.api import write_data

def get_torus(R, r, phi, theta):
    x = R*cos(phi) + r*cos(theta)*cos(phi)
    y = R*sin(phi) + r*cos(theta)*sin(phi)
    z = r*sin(theta)
    u = cos(theta)*cos(phi)
    v = cos(theta)*sin(phi)
    w = sin(theta)
    return (x, y, z, u, v, w)

def visualize_distortion(knot, plot_knot=False, cmap="cool", highlight_peaks=True, scene_mlab=None):
    if scene_mlab is None:
        scene_mlab = mlab
    if plot_knot:
        scene_mlab.figure(bgcolor=(0,0,0))
        knot.plot()
    N = knot.num_vertices

    a, b = mgrid[0:N, 0:N]

    phi = a * (2*pi / N)
    theta = b * (2*pi / N)

    R, r, max_f_radius = 10, 2, 5
    assert R >= r + max_f_radius + 1

    x, y, z, u, v, w = get_torus(R, r, phi, theta)

    d = knot.distortion_ratios["euclidean"]
    f = (d / np.amax(d)) * max_f_radius # normalized

    # scene_mlab.figure(bgcolor=(0,0,0))
    # mlab.mesh(x, y, z, color=(0.5,0.5,0.5))#, colormap='viridis') # plotting torus
    # mlab.quiver3d(x, y, z, u, v, w, scale_mode='none') # plotting normal vectors on torus
    plot = scene_mlab.mesh(x + f*u, y + f*v, z + f*w, colormap=cmap, scalars=d, scale_mode="none") # plotting f on torus!
    scene_mlab.colorbar()
    peaks = None
    if highlight_peaks:
        inner_ratios = d[1:-1, 1:-1]
        peaks_flag = np.full_like(d, fill_value=False, dtype=bool)
        peaks_flag[1:-1, 1:-1] = (inner_ratios > d[:-2, :-2]) & (inner_ratios > d[2:, :-2]) & \
                                (inner_ratios > d[:-2, 2:]) & (inner_ratios > d[2:, 2:])
        peak_phi, peak_theta = phi[peaks_flag], theta[peaks_flag]
        px, py, pz, pu, pv, pw = get_torus(R, r, peak_phi, peak_theta)
        px = px + f[peaks_flag]*pu
        py = py + f[peaks_flag]*pv
        pz = pz + f[peaks_flag]*pw
        peaks = scene_mlab.quiver3d(px, py, pz, pu, pv, pw, color=(1,1,1), mode="arrow", scale_factor=1)
    return (plot, peaks)

if __name__ == "__main__":
    DIRECTIONS = get_minimal_lattice_trefoil(1, num_points=100) #get_smooth_figure8(5, num_points=500)
    K = StickKnot(DIRECTIONS, validate=False, compute_distortion=True, mode="euclidean")
    print(K.vertex_distortion_pairs)
    K.plot()

    # plot = visualize_distortion(K, plot_knot=True, cmap="plasma")
    mlab.show()
