from math import sqrt
from random import randint

import matplotlib.cm as colormap
import matplotlib.colors as mcolors
import mayavi.mlab as mlab
import numpy as np
from copy import deepcopy
from time import perf_counter



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

def assert_is_3d_point(x):
    assert isinstance(x, (tuple, list, np.ndarray)), get_error_msg("Point datatype", "list or tuple", type(x))
    assert len(x) == 3, get_error_msg("Point dimension", 3, len(x))
    for c in x:
        assert isinstance(c, (int, float)) or np.issubdtype(c, np.number), get_error_msg("Point coordinate datatype", "int or float", type(c))

def are_vectors_parallel(x, y):
    assert_is_3d_point(x)
    assert_is_3d_point(y)
    cross = np.cross(np.array(x), np.array(y))
    return all(cross == 0)

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
