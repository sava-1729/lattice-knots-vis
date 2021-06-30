import enum
import numpy as np
import mayavi.mlab as mlab
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
from utils import *

"""
z    y (into the plane)
|   /
|  /
| /
|/
--------- x
"""

W = np.array([0,0,1])  # +z
A = np.array([-1,0,0]) # -x
S = np.array([0,0,-1]) # -z
D = np.array([1,0,0])  # +x
Q = np.array([0,1,0])  # +y
E = np.array([0,-1,0]) # -y

###########################################
# Edit the variable below to construct your knot!
# The constants defined above represent unit movement in the respective directions.
# Replace the list below with an ordered list of directions that you want your knot to follow.
DIRECTIONS = [D, D, D, S, E, E, A, A, Q, Q, Q, W, W, D, E, E, S, S, S, A, A, W, W]
# The above is a lattice conformation of the Trefoil Knot.
###########################################

"""
!!! CAUTION !!!
DO NOT append the *last* direction that completes the knot.
Example: If you wish to plot the unknot whose vertices are (0,0,0), (0,0,1), (0,1,1), (0,1,0)
Then the DIRECTIONS variable should look like:
DIRECTIONS = [W, Q, S]
"""

class Stick:
    def __init__(self, start, end):
        assert_is_3d_point(start)
        assert_is_3d_point(end)
        self.start = np.array(start)
        self.end = np.array(end)
        assert any(self.start != self.end)
        self.X = np.linspace(self.start[0], self.end[0], 3)
        self.Y = np.linspace(self.start[1], self.end[1], 3)
        self.Z = np.linspace(self.start[2], self.end[2], 3)
        self.vector = self.end - self.start

    def plot(self, fig, color="b"):
        mlab.plot3d(self.X, self.Y, self.Z, color=color, line_width=8, figure=fig)

    def shares_plane_with(self, other_stick):
        assert isinstance(other_stick, Stick)
        normal_abc = np.cross(self.vector, other_stick.start - self.start)
        vector_ad = other_stick.end - self.start
        return np.dot(normal_abc, vector_ad)

    def is_parallel_to(self, other_stick):
        assert isinstance(other_stick, Stick)
        cross = np.cross(self.vector, other_stick.vector)
        return all(cross == 0)

    def is_point_on_stick(self, point):
        assert_is_3d_point(point)
        x_in_range = point[0] <= max(self.X) and point[0] >= min(self.X)
        y_in_range = point[1] <= max(self.Y) and point[1] >= min(self.Y)
        z_in_range = point[2] <= max(self.Z) and point[2] >= min(self.Z)
        return (x_in_range and y_in_range and z_in_range)

    def is_intersecting(self, other_stick):
        if all(other_stick.start == self.start) or all(other_stick.start == self.end) or all(other_stick.end == self.start) or all(other_stick.end == self.end):
            return True
        if not self.shares_plane_with(other_stick):
            return False
        if self.is_parallel_to(other_stick):
            connector = other_stick.start - self.end
            if all(np.cross(connector, self.vector) == 0):
                # if the sticks are parallel and also colinear
                return self.is_point_on_stick(other_stick.start) or self.is_point_on_stick(other_stick.end)
            else:
                # if the sticks are parallel but not colinear
                return False
        else:
            connector1 = other_stick.start - self.start
            connector2 = other_stick.end - self.start
            cross1 = np.cross(self.vector, connector1)
            cross2 = np.cross(self.vector, connector2)
            dot12 = np.dot(cross1, cross2)
            if dot12 <= 0:
                connector3 = self.start - other_stick.start
                connector4 = self.end - other_stick.start
                cross3 = np.cross(self.vector, connector3)
                cross4 = np.cross(self.vector, connector4)
                dot34 = np.dot(cross3, cross4)
                if dot34 <= 0:
                    if dot12 == 0 and dot34 == 0:
                        print("Strange case.")
                        print("stick1: %s -> %s" % str((self.start, self.end)))
                        print("stick2: %s -> %s" % str((other_stick.start, other_stick.end)))
                    return True
                else:
                    return False

class StickKnot:
    def __init__(self, vertices):
        assert isinstance(vertices, (list, tuple))
        sticks = [None for i in range(len(vertices))]
        for i in range(len(vertices)):
            sticks[i] = Stick(vertices[i-1], vertices[i])
        # assert isinstance(sticks, (list, tuple))
        # for stick in sticks:
        #     assert isinstance(stick, Stick)
        # assert all(sticks[0].start == sticks[-1].end), "Given stick chain do not form a closed loop"
        for i in range(len(sticks)):
            # assert all(sticks[i].start == sticks[i-1].end), "Given stick chain has a discontinuity"
            if sticks[i-1].is_parallel_to(sticks[i]):
                assert np.dot(sticks[i].vector, sticks[i-1].vector) > 0
            k = 1 if (i == (len(sticks)-1)) else 0
            for j in range(k, i-1):
                assert not sticks[i].is_intersecting(sticks[j]), ("Sticks %d and %d are intersecting" % (j+1, i+1))
        self.sticks = sticks
        self.vertices = vertices
        self.length = len(vertices)

    def plot(self, color="b", highlight_vertices=True):
        fig = mlab.figure(bgcolor=(1,1,1))
        for i, stick in enumerate(self.sticks):
            stick.plot(fig, color=get_color(i))
        if highlight_vertices:
            mlab.points3d(*list(zip(*self.vertices)), figure=fig, color=(0,0,0), scale_factor=0.1)
        # ax.set_xlabel("X")
        # ax.set_ylabel("Y")
        # ax.set_zlabel("Z")
        return fig

def construct_knot(directions):
    origin = np.array([0,0,0])
    vertices = [origin]
    for d in directions:
        vertices.append(vertices[-1] + d)
    return StickKnot(vertices)

my_knot = construct_knot(DIRECTIONS)
my_knot.plot()
mlab.show()
# plt.show()
