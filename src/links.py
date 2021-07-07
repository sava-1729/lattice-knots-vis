from numpy.lib.arraysetops import isin
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
            knot.plot(new_figure=False, stick_color=knot_colors[i], thickness=15, highlight_vertex_distortion_pair=False)#, mode="tube")

def get_u_unknot(plane, base_center, orientation, lx, ly, lz):
    directions = None
    start = [0,0,0]
    if plane == "y" and orientation == "+z":
        directions = [W*lz, Q*ly, S*lz, D*lx, W*lz, E*ly, S*lz]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2]
    if plane == "y" and orientation == "-z":
        directions = [S*lz, Q*ly, W*lz, D*lx, S*lz, E*ly, W*lz]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2]
    if plane == "y" and orientation == "+x":
        directions = [D*lx, Q*ly, A*lx, W*lz, D*lx, E*ly, A*lx]
        start[0] = base_center[0]
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2] - (lz / 2)
    if plane == "y" and orientation == "-x":
        directions = [A*lx, Q*ly, D*lx, W*lz, A*lx, E*ly, D*lx]
        start[0] = base_center[0]
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2] - (lz / 2)
    if plane == "x" and orientation == "+z":
        directions = [W*lz, D*lx, S*lz, Q*ly, W*lz, A*lx, S*lz]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2]
    if plane == "x" and orientation == "-z":
        directions = [S*lz, D*lx, W*lz, Q*ly, S*lz, A*lx, W*lz]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2]
    if plane == "x" and orientation == "+y":
        directions = [Q*ly, D*lx, E*ly, W*lz, Q*ly, A*lx, E*ly]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1]
        start[2] = base_center[2] - (lz / 2)
    if plane == "x" and orientation == "-y":
        directions = [E*ly, D*lx, Q*ly, W*lz, E*ly, A*lx, Q*ly]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1]
        start[2] = base_center[2] - (lz / 2)
    if plane == "z" and orientation == "+x":
        directions = [D*lx, W*lz, A*lx, Q*ly, D*lx, S*lz, A*lx]
        start[0] = base_center[0]
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2] - (lz / 2)
    if plane == "z" and orientation == "-x":
        directions = [A*lx, W*lz, D*lx, Q*ly, A*lx, S*lz, D*lx]
        start[0] = base_center[0]
        start[1] = base_center[1] - (ly / 2)
        start[2] = base_center[2] - (lz / 2)
    if plane == "z" and orientation == "+y":
        directions = [Q*ly, W*lz, E*ly, D*lx, Q*ly, S*lz, E*ly]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1]
        start[2] = base_center[2] - (lz / 2)
    if plane == "z" and orientation == "-y":
        directions = [E*ly, W*lz, Q*ly, D*lx, E*ly, S*lz, Q*ly]
        start[0] = base_center[0] - (lx / 2)
        start[1] = base_center[1]
        start[2] = base_center[2] - (lz / 2)
    return construct_knot(directions, start)

def get_simple_unknot(plane, center, lx=1, ly=1, lz=1):
    directions = None
    start = [0,0,0]
    if plane == "x":
        directions = [Q*ly, W*lz, E*ly]
        start[0] = center[0]
        start[1] = center[1] - (ly / 2)
        start[2] = center[2] - (lz / 2)
    if plane == "y":
        directions = [W*lz, D*lx, S*lz]
        start[0] = center[0] - (lx / 2)
        start[1] = center[1]
        start[2] = center[2] - (lz / 2)
    if plane == "z":
        directions = [D*lx, Q*ly, A*lx]
        start[0] = center[0] - (lx / 2)
        start[1] = center[1] - (ly / 2)
        start[2] = center[2]
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
    print("RED: %d" % comp1.num_sticks)
    print("GREEN: %d" % comp2.num_sticks)
    print("BLUE: %d" % comp3.num_sticks)
    print("YELLOW: %d" % comp4.num_sticks)
    print("TOTAL: %d" % sum([c.num_sticks for c in [comp1,comp2,comp3,comp4]]))

def experimental_link(n):
    assert n % 4 == 2 and n > 2
    k = (n+2) // 4
    print(k)
    print(list(range(5, 10*(k-2) + 5 + 1, 10)))
    print(list(range(0, 10*(k-1) + 1, 10)))
    print(list(range(4, 10*(k-1) + 1, 10)))
    print(list(range(6, 10*(k-1) + 1, 10)))
    zrings = [get_simple_unknot("z", (x,0,0), 4, 4) for x in range(5, 10*(k-2) + 5 + 1, 10)]
    yrings = [get_simple_unknot("y", (x,0,0), 4, 0, 4) for x in range(0, 10*(k-1) + 1, 10)]
    yrings.pop()
    yconnectors_right = [get_u_unknot("y", (x,0,0), "-x", 3, 2, 2) for x in range(4, 10*(k-1) + 1, 10)]
    yconnectors_left = [get_u_unknot("y", (x,0,0), "+x", 3, 2, 2) for x in range(6, 10*(k-1) + 1, 10)]
    yconnectors_left.pop()
    legs = [get_u_unknot("x", (0,0,0), "-z", 1, 2, 4), get_u_unknot("x", (10*(k-1)-3,0,-4), "+z", 2, 2, 5)]
    directions = [Q*8, A*8, Q*4, D*20, E*12, S*2, A*8, Q*8, D*8, Q*4, A*20, E*12, W*2]
    start = (5*(k-1),0,-6)
    bottom_connector = construct_knot(directions, start)
    components = zrings + yrings + yconnectors_right + yconnectors_left + legs + [bottom_connector]
    comp_colors = [(0,1,0) for i in zrings] + [(1,0,1) for i in yrings] + [(1,1,0) for i in yconnectors_right] + [(1,1,0) for i in yconnectors_left] + [(0,0,1), (0,0,1), (1,0.5,0)]
    # comp1 = get_simple_unknot("z", (0,0,0), 4, 4)

    # comp2 = get_u_unknot("y", (1,0,0), "+x", 3, 2, 2)

    # comp3 = get_u_unknot("y", (-1,0,0), "-x", 3, 2, 2)

    # comp4 = get_simple_unknot("y", (5,0,0), 4, 0, 4)

    # comp5 = get_simple_unknot("y", (-5,0,0), 4, 0, 4)

    # comp6 = get_u_unknot("y", (0,0,-4), "+z", 10, 2, 4)
    # StickLink([comp1,comp2,comp3,comp4,comp5,comp6]).plot([(0,1,0),(1,1,0),(1,1,0),(1,0,1),(1,0,1),(0,0,1)])
    StickLink(components).plot(comp_colors)

plot_brunnian_4_link()
# experimental_link(10)
mlab.show()