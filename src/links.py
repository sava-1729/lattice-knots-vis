"""
This file contains the StickLink class which is used to construct links.
Copyright (C) 2022-23 Vatsal Srivastava

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can find a copy of the GNU General Public License in the root
directory of this repository, named `LICENSE.md`.
If you do not find it, see <https://www.gnu.org/licenses/>.
"""


from knots import *

class StickLink:
    def __init__(self, knots):
        self.knots = knots
    def plot(self, knot_colors=None, bgcolor=(0,0,0)):
        if knot_colors is not None:
            assert isinstance(knot_colors, list)
            assert len(knot_colors) == len(self.knots)
        else:
            knot_colors = [get_color(i) for i in range(len(self.knots))]
        create_new_figure(bgcolor=bgcolor)
        for i, knot in enumerate(self.knots):
            knot.plot(new_figure=False, stick_color=knot_colors[i], thickness=15, highlight_vertex_distortion_pairs=False, label_vertices=False)

def get_u_unknot(plane, base_center, lx, ly, lz):
    directions = None
    start = [0,0,0]
    if plane == "zx":
        directions = [W*lz, Q*ly, S*lz, D*lx, W*lz, E*ly, S*lz]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2]
    if plane == "zy":
        directions = [W*lz, D*lx, S*lz, Q*ly, W*lz, A*lx, S*lz]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2]
    if plane == "xz":
        directions = [D*lx, Q*ly, A*lx, W*lz, D*lx, E*ly, A*lx]
        start[0] = base_center[0]
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2] - (lz / 2)
    if plane == "xy":
        directions = [D*lx, W*lz, A*lx, Q*ly, D*lx, S*lz, A*lx]
        start[0] = base_center[0]
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2] - (lz / 2)
    if plane == "yz":
        directions = [Q*ly, D*lx, E*ly, W*lz, Q*ly, A*lx, E*ly]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1]
        start[2] = base_center[2] - (lz / 2)
    if plane == "yx":
        directions = [Q*ly, W*lz, E*ly, D*lx, Q*ly, S*lz, E*ly]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1]
        start[2] = base_center[2] - (lz / 2)
    return construct_knot(directions, start)

def plot_brunnian_4_link():
    directions = [D*8, W*12, Q*4, S*12, A*8, W*12, E*4]
    start = (0,0,0)
    comp1 = construct_knot(directions, start)

    directions = [Q*12, S*2, E*12, D*12, Q*12, W*2, E*12]
    start = (-2,2,11)
    comp2 = construct_knot(directions, start)

    directions = [S*10, Q*2, W*10, D*16, S*10, E*2, W*10]
    start = (-4,9,10)
    comp3 = construct_knot(directions, start)

    directions = [Q*8, A*8, Q*4, D*20, E*12, S*2, A*8, Q*8, D*8, Q*4, A*20, E*12, W*2]
    start = (2,-2,4)
    comp4 = construct_knot(directions, start)
    StickLink([comp1,comp2,comp3,comp4]).plot([(1,0,0),(0,1,0),(0,0,1),(1,1,0)])
    mlab.show()

plot_brunnian_4_link()