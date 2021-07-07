from knots import *

"""
z    y (into the plane)
|   /
|  /
| /
|/
--------- x
"""

# W = +z
# A = -x
# S = -z
# D = +x
# Q = +y
# E = -y

###########################################
# Edit the variable below to construct your knot!
# The constants W A S D Q E shown above represent unit movement in the respective directions.
DIRECTIONS = [W*4, E*2, D*5, Q*2, A*4, S*4, D*2, W*3, D*2, E*2, A*4, S*3, A*1]
# Replace the list below with an ordered list of directions that you want your knot to follow.
# DIRECTIONS = [W, Q, S]
# The above is a lattice conformation of the Trefoil Knot.
###########################################

"""
!!! CAUTION !!!
DO NOT append the *last* direction that completes the knot.
Example: If you wish to plot the unknot whose vertices are (0,0,0), (0,0,1), (0,1,1), (0,1,0)
Then the DIRECTIONS variable should look like:
DIRECTIONS = [W, Q, S]
"""

def draw_knot():
    global DIRECTIONS
    N = 15
    start = [(i*3, i*(-1), i*2) for i in range(N)]
    my_knots = [construct_knot(DIRECTIONS, start=s) for s in start]
    print(my_knots[0].num_sticks)
    # my_knot_1 = construct_knot(DIRECTIONS)
    # my_knot_2 = 
    create_new_figure()
    for i, knot in enumerate(my_knots):
        knot.plot(bgcolor=(0,0,0), highlight_vertices=True,mode="tube",thickness=0.5,highlight_vertex_distortion_pair=False, new_figure=False, stick_color=get_color(i))
    # for s in my_knot.sticks:
    #     s.id += 24
    #     s.id *= 7
    # my_knot_1.plot(bgcolor=(0,0,0), highlight_vertices=True,mode="tube",thickness=0.5,highlight_vertex_distortion_pair=False)
    # my_knot_2.plot(bgcolor=(0,0,0), highlight_vertices=True,mode="tube",thickness=0.5,highlight_vertex_distortion_pair=False, new_figure=False)
    #, stick_color=(0.5,0.5,0.5), ref_vertex_index=index)
    # mlab.colorbar(object=my_knot.stick_objs[0])
    # origin = np.array((0,0,0))
    # vertices = [origin]
    # directions = [Q, Q, D, W, W, W, E, E, A, S, S]
    # for d in directions:
    #     vertices.append(vertices[-1] + d)
    # X, Y, Z = list(zip(*vertices))
    # plot_3d_points(X, Y, Z, color=(1,1,1), scale_factor=0.25)
    # vertices = [origin]
    # directions = [Q*2, D, W*3, E*2, A]
    # for d in directions:
    #     vertices.append(vertices[-1] + d)
    # X, Y, Z = list(zip(*vertices))
    # plot_3d_points(X, Y, Z, color=(0.5,0.5,0.5), scale_factor=0.25, mode="cube")
    # print("Vertex Distortion: %f" % my_knot.vertex_distortion)
    # i, j = my_knot.vertex_distortion_pair_indices
    # print("Realized between: %s and %s" % (my_knot.vertices[i], my_knot.vertices[j]))
    # print(my_knot.distortion_ratios)
    mlab.show()

draw_knot()