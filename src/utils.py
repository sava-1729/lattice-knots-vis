from sys import excepthook
import numpy as np
from numpy.core.fromnumeric import argmax
import matplotlib.colors as mcolors
import mayavi.mlab as mlab
from random import randint

PRE_COLORS = list(mcolors.BASE_COLORS.values()) + list(mcolors.XKCD_COLORS.values())
PRE_COLORS.remove(mcolors.BASE_COLORS["w"])
PRE_COLORS.remove(mcolors.BASE_COLORS["k"])
COLORS = [mcolors.hex2color(clr) for clr in list(PRE_COLORS)]
NUM_COLORS = len(COLORS)
FIGURE = None

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

def create_new_figure(bgcolor=(0,0,0)):
    global FIGURE
    FIGURE = mlab.figure(bgcolor=bgcolor)

def plot_3d_line(X, Y, Z, label=0, color=None, mode="line", thickness=2):
    global FIGURE
    if color is None:
        if label >= 0:
            color = get_color(label)
        else:
            color = (0.5,0.5,0.5)
    if mode == "tube":
        return mlab.plot3d(X, Y, Z, figure=FIGURE, color=color, tube_radius=thickness/10)
    else:
        return mlab.plot3d(X, Y, Z, figure=FIGURE, color=color, line_width=thickness)

def plot_3d_points(X, Y, Z, scalars=None, monochromatic=True, color=(0.5,0.5,0.5), colormap="blue-red", scale_factor=0.25, mode="sphere"):
    global FIGURE
    if monochromatic:
        return mlab.points3d(X, Y, Z, figure=FIGURE, color=color, scale_factor=scale_factor, mode=mode)
    elif scalars is not None:
        return mlab.points3d(X, Y, Z, scalars, figure=FIGURE, colormap=colormap, scale_factor=scale_factor, mode=mode)
    else:
        raise AttributeError("Invalid Arguments to function plot_3d_points")
