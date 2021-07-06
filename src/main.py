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
# Replace the list below with an ordered list of directions that you want your knot to follow.
DIRECTIONS = [D*3, S, E*2, A*2, Q*3, W*2, D, E*2, S*3, A*2, W*2]
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
    my_knot = construct_knot(DIRECTIONS)
    index = 10
    my_knot.plot(bgcolor=(0,0,0), stick_color=(0.5,0.5,0.5), ref_vertex_index=index)
    print("Vertex Distortion: %f" % my_knot.vertex_distortion)
    i, j = my_knot.vertex_distortion_pair_indices
    print("Realized between: %s and %s" % (my_knot.vertices[i], my_knot.vertices[j]))
    print(my_knot.distortion_ratios)
    mlab.show()

draw_knot()