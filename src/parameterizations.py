from utils import *
from numpy import pi, sin, cos

def get_knot_vertices(directions, num_points):
    origin = np.array([0,0,0])
    vertices = []
    last_pose = origin
    length = sum(int(max(np.absolute(d))) for d in directions)
    for d in directions:
        n = int(max(np.absolute(d)))
        div = int((n/length) * num_points)
        d_unit = d / div
        for i in range(div):
            vertices.append(last_pose + d_unit)
            last_pose = last_pose + d_unit
    return vertices

def get_Direction_array(X, Y, Z, num_points):
    directions = np.empty(num_points, dtype=Direction)

    x_, y_, z_ = X[0], Y[0], Z[0]
    i = 0
    for x, y, z in zip(X[1:], Y[1:], Z[1:]):
        directions[i] = Direction(x=x-x_, y=y-y_, z=z-z_)
        i += 1
        x_, y_, z_ = x, y, z
    directions[num_points-1] = Direction(x=X[0]-X[-1], y=Y[0]-Y[-1], z=Z[0]-Z[-1])
    # vertices = [np.array(p) for p in zip(list(X), list(Y), list(Z))]
    return directions

def get_minimal_lattice_trefoil(L, num_points=100):
    DIRECTIONS = np.array([D*3, Q*2, W, A*2, E*3, S*2, D, Q*2, W*3, A*2, E, S*2])*L
    return get_knot_vertices(DIRECTIONS, num_points)

def get_lattice_trefoil_vd_10_33(L, num_points=100):
    DIRECTIONS = np.array([X(8), Y(5), Z(4), X(-5), Y(-5), X(), Y(-4), Z(-8), Y(8), Z(5), Y(-1), X(), Z(), X(), Y(-1), Z(), X(), Y(-1), Z(5), X(-7), Y(-1), Z(-8)])
    return DIRECTIONS
    # return get_knot_vertices(DIRECTIONS, num_points)

def get_smooth_figure8(L, num_points=100):
    T = np.linspace(0, 2*pi, endpoint=False, num=num_points)

    X = L * (2 + np.cos(2*T)) * np.cos(3*T)
    Y = L * (2 + np.cos(2*T)) * np.sin(3*T)
    Z = L * (np.sin(4*T))

    return get_Direction_array(X, Y, Z, num_points)

def get_figure8_extra_crossing(L, num_points=200):
    T = np.linspace(0, 2*pi, endpoint=False, num=num_points)

    X = L * (2 + np.cos(2*T)) * np.cos(3*T)
    Y = L * (2 + np.cos(2*T)) * np.sin(3*T)
    Z = L * (np.sin(4*T))

    ys = Y[180]
    yf = Y[19]
    a = (ys+yf)/2
    b = (ys-yf)/2
    t = np.linspace(0, 2*pi, endpoint=False, num=40)
    for i in range(180,220):
        X[i%200] = X[i%200] + 2*sin(0.5*t[i-180])
        Y[i%200] = a + b*cos(1.5*t[i-180])
        Z[i%200] = Z[i%200] + sin(t[i-180])

    return get_Direction_array(X, Y, Z, num_points)

def get_smooth_shastri_trefoil(L, num_points):
    T = np.linspace(-2.2, 2.2, endpoint=False, num=num_points)

    X = L * ((T**3) - (3*T))
    Y = L * ((T**4) - (4*(T**2)))
    Z = L * ((T**5) - (10*T))

    return get_Direction_array(X, Y, Z, num_points)

def get_trefoil_extra_crossing(L, num_points=200):
    assert num_points == 200
    T = np.linspace(0, 2*pi, endpoint=False, num=num_points)

    X = L * (np.sin(T) + 2*np.sin(2*T))
    Y = L * (np.cos(T) - 2*np.cos(2*T))
    Z = L * (-np.sin(3*T))

    ys = Y[160]
    yf = Y[199]
    a = (ys+yf)/2
    b = (ys-yf)/2
    t = np.linspace(0, 2*pi, endpoint=False, num=40)
    for i in range(160,200):
        X[i] = X[i] + sin(t[i-160])
        Y[i] = a + b*cos(1.5*t[i-160])
        Z[i] = Z[i] + 10*sin(0.5*t[i-160])

    return get_Direction_array(X, Y, Z, num_points)

def get_smooth_trefoil(L, num_points=100):
    T = np.linspace(0, 2*pi, endpoint=False, num=num_points)

    X = L * (np.sin(T) + 2*np.sin(2*T))
    Y = L * (np.cos(T) - 2*np.cos(2*T))
    Z = L * (-np.sin(3*T))

    return get_Direction_array(X, Y, Z, num_points)

def get_tref_unknot(L, num_points=100):
    T = np.linspace(0, 2*pi, endpoint=False, num=num_points)

    X = L * (np.sin(T) + 2*np.sin(2*T))
    Y = L * (np.cos(T) - 2*np.cos(2*T))
    Z = L * (-np.sin(2*T))

    return get_Direction_array(X, Y, Z, num_points)

def get_smooth_torus_trefoil(L, num_points=100):
    T = np.linspace(0, 2*pi, endpoint=False, num=num_points)

    X = L * (2 + np.cos(3*T)) * np.cos(2*T)
    Y = L * (2 + np.cos(3*T)) * np.sin(2*T)
    Z = L * np.sin(3*T)

    return get_Direction_array(X, Y, Z, num_points)

def get_smooth_torus_knot(p, q, L, num_points=100):
    T = np.linspace(0, 2*pi, endpoint=False, num=num_points)

    X = L * (3 + np.cos(p*T)) * np.cos(q*T)
    Y = L * (3 + np.cos(p*T)) * np.sin(q*T)
    Z = L * np.sin(p*T)

    return get_Direction_array(X, Y, Z, num_points)

def get_simple_unknot(L, num_points=100):
    T = np.linspace(0, 2*pi, endpoint=False, num=num_points)

    X = L * np.cos(T)
    Y = L * np.sin(T)
    Z = 0 * T

    return get_Direction_array(X, Y, Z, num_points)

def get_K_p(P, num_points=100):
    DIRECTIONS = []
    x_len = 2
    sign = 1
    for i in range(1, 2*P - 1):
        y_len = (P - 1) if i % 2 == 1 else P
        DIRECTIONS.append(Z(sign * (2*P - i)))
        DIRECTIONS.append(X(sign * x_len))
        DIRECTIONS.append(Y(sign * y_len))
        if i % 2 == 1:
            x_len += 1
        sign = -sign
    DIRECTIONS.append(Z(sign * 1))
    DIRECTIONS.append(X(sign * P))
    DIRECTIONS.append(Y(sign * (2*P - 1)))
    sign = -sign
    DIRECTIONS.append(Z(sign * P))
    DIRECTIONS.append(X(sign * 1))
    DIRECTIONS.append(Y(sign * P))
    # DIRECTIONS.append(DIRECTIONS[0]-DIRECTIONS[-1])
    return np.array(DIRECTIONS)

KNOTS = {"minimal_lattice_trefoil": get_minimal_lattice_trefoil, "lattice_trefoil_vd_10_33": get_lattice_trefoil_vd_10_33, "smooth_figure8": get_smooth_figure8, "figure8_extra_crossing": get_figure8_extra_crossing, "smooth_trefoil": get_smooth_trefoil, "trefoil_extra_crossing": get_trefoil_extra_crossing, "smooth_torus_trefoil": get_smooth_torus_trefoil, "tref_unknot": get_tref_unknot, "simple_unknot" : get_simple_unknot}

def get_knot_point_cloud(knot_name, size, pt_cloud_size):
    return KNOTS[knot_name](size, pt_cloud_size)
