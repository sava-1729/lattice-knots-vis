from math import sqrt, isclose
from random import randint

import matplotlib.cm as colormap
import matplotlib.colors as mcolors
import mayavi.mlab as mlab
import numpy as np
from copy import deepcopy
from time import perf_counter

W = np.array([0,0,1])  # +z
A = np.array([-1,0,0]) # -x
S = np.array([0,0,-1]) # -z
D = np.array([1,0,0])  # +x
Q = np.array([0,1,0])  # +y
E = np.array([0,-1,0]) # -y

ABS_TOL = 1e-10

PRE_COLORS = list(mcolors.BASE_COLORS.values()) + list(mcolors.XKCD_COLORS.values())
PRE_COLORS.remove(mcolors.BASE_COLORS["w"])
PRE_COLORS.remove(mcolors.BASE_COLORS["k"])
COLORS = [mcolors.hex2color(clr) for clr in list(PRE_COLORS)]
NUM_COLORS = len(COLORS)
FIGURE = None
COLORS = [(1,0,0),(1,0.5,0),(1,1,0),(0.5,1,0),(0,1,0),(0,1,0.5),(0,1,1),(0,0.5,1),(0,0,1),(0.5,0,1),(1,0,1),(1,0,0.5), (1,0.5,0.5), (0.5,1,0.5), (0.5,0.5,1)]+COLORS

def get_random_color():
    global NUM_COLORS
    color = COLORS.pop(randint(0, NUM_COLORS))
    NUM_COLORS -= 1
    return color

def get_color(i):
    return COLORS[i % NUM_COLORS]

def get_error_msg(name_of_erroneous_item, expected_value, actual_value):
    msg = name_of_erroneous_item + " incorrect! \n"
    msg += "Expected: %s \n" % str(expected_value)
    msg += "Given: %s \n" % str(actual_value)
    return msg

def are_3d_points(*points):
    for p in points:
        assert isinstance(p, np.ndarray)
        assert p.shape == (3,)

def assert_is_3d_point(x):
    assert isinstance(x, (tuple, list, np.ndarray)), get_error_msg("Point datatype", "list or tuple", type(x))
    assert len(x) == 3, get_error_msg("Point dimension", 3, len(x))
    for c in x:
        assert isinstance(c, (int, float)) or np.issubdtype(c, np.number), get_error_msg("Point coordinate datatype", "int or float", type(c))

def are_vectors_parallel(x, y):
    are_3d_points(x, y)
    return np.allclose(x / np.sqrt(np.sum(x ** 2)), y / np.sqrt(np.sum(y ** 2)), rtol=0)

def create_new_figure(bgcolor=(0,0,0)):
    global FIGURE
    FIGURE = mlab.figure(bgcolor=bgcolor)
    return FIGURE

def plot_3d_line(X, Y, Z, label=0, color=None, mode="line", thickness=2):
    global FIGURE
    if color is None:
        if isinstance(label, float):
            color = colormap.hsv(label)[:3]
        elif label >= 0:
            color = get_color(label)
        else:
            color = (0.5,0.5,0.5)
    if mode == "tube":
        return mlab.plot3d(X, Y, Z, figure=FIGURE, color=color, tube_radius=thickness/10)
    else:
        return mlab.plot3d(X, Y, Z, figure=FIGURE, color=color, line_width=thickness)

def plot_3d_points(X, Y, Z, scalars=None, monochromatic=True, color=(1,1,1), colormap="blue-red", scale_factor=0.25, mode="sphere"):
    global FIGURE
    if monochromatic:
        return mlab.points3d(X, Y, Z, figure=FIGURE, color=color, scale_factor=scale_factor, mode=mode)
    elif scalars is not None:
        return mlab.points3d(X, Y, Z, scalars, figure=FIGURE, colormap=colormap, scale_factor=scale_factor, mode=mode)
    else:
        raise AttributeError("Invalid Arguments to function plot_3d_points")

def distance_euclidean(x, y):
    # x = np.array(x)
    # y = np.array(y)
    return sqrt(sum((x-y)**2))

def distance_taxicab(x, y):
    # x = np.array(x)
    # y = np.array(y)
    return sum(np.absolute(x-y))

def smooth_distortion(knot, num_divisions=10, mode=2):
    N = knot.num_sticks * num_divisions
    distortion_ratios = {}

    for i in range(N):
        stick = knot.sticks[i // num_divisions]
        vertex_i = stick.start + ((i % num_divisions) / num_divisions) * stick.vector
        for j in range(0, i):
            stick = knot.sticks[j // num_divisions]
            vertex_j = stick.start + ((j % num_divisions) / num_divisions) * stick.vector
            try:
                distance_along_knot = knot.distance(vertex_i, vertex_j)
            except AssertionError:
                print("Vertex %d: %s" % (i, vertex_i))
                print("Vertex %d: %s" % (j, vertex_j))
            distance_in_space = distance_euclidean(vertex_i, vertex_j) if mode == 2 else distance_taxicab(vertex_i, vertex_j)
            distortion_ratios[(i,j)] = distance_along_knot / distance_in_space
    distortion = max(distortion_ratios.values())
    distortion_pairs = []
    for pair in distortion_ratios.keys():
        if distortion_ratios[pair] == distortion:
            i, j = pair
            stick = knot.sticks[i // num_divisions]
            vertex_i = stick.start + ((i % num_divisions) / num_divisions) * stick.vector
            stick = knot.sticks[j // num_divisions]
            vertex_j = stick.start + ((j % num_divisions) / num_divisions) * stick.vector
            distortion_pairs.append((vertex_i, vertex_j))
    return (distortion, distortion_pairs)

class Direction:
    def __init__(self, x=0, y=0, z=0):
        self.__vector = np.array((x, y, z))
        if np.issubdtype(self.__vector.dtype, np.signedinteger):
            self.type_ = int
        elif np.issubdtype(self.__vector.dtype, np.floating):
            self.type_ = float
        else:
            raise TypeError("Coordinates of directions must be real numbers.")
        assert (x != 0) or (y != 0) or (z != 0)
    def get_vector(self):
        return self.__vector
    def __sub__(self, other_dir):
        assert isinstance(other_dir, Direction)
        return Direction(*(self.get_vector() - other_dir.get_vector()))
    def __add__(self, other_dir):
        assert isinstance(other_dir, Direction)
        return Direction(*(self.get_vector() + other_dir.get_vector()))

def X(t=1):
    return Direction(x=t)
def Y(t=1):
    return Direction(y=t)
def Z(t=1):
    return Direction(z=t)
def XYZ(p, q, r):
    return Direction(x=p, y=q, z=r)

def plot_3d_lattice(fig=None, xlim=(-10, 10), ylim=(-10, 10), zlim=(-10, 10), res=5):
    if fig is None:
        fig = mlab.gcf()
    X = np.linspace(xlim[0], xlim[1], num=res, endpoint=False)
    Y = np.linspace(ylim[0], ylim[1], num=res, endpoint=False)
    Z = np.linspace(zlim[0], zlim[1], num=res, endpoint=False)

    for x in X:
        for y in Y:
            for z in Z:
                mlab.plot3d((x, x), (y, y), zlim, tube_radius=0.15, color=(1,1,1))
                mlab.plot3d((x, x), ylim, (z, z), tube_radius=0.15, color=(1,1,1))
                mlab.plot3d(xlim, (y, y), (z, z), tube_radius=0.15, color=(1,1,1))
    # X, Y, Z = np.mgrid[xlim[0]:xlim[1]:res, ylim[0]:ylim[1]:res, zlim[0]:zlim[1]:res]
    # mlab.mesh(X, Y, Z, figure=fig)