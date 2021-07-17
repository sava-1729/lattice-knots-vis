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

#################################### INSTRUCTIONS #######################################
# Edit the variable below to construct your knot!
# The constants W A S D Q E shown above represent unit movement in the respective directions.
# Replace the list below with an ordered list of directions that you want your knot to follow.
#########################################################################################

####################### Trefoil with varying distortion as scaled up ####################
N = 1 # SCALE FACTOR
DIRECTIONS = np.array([D*41, Q*2, W, A*40, E*3, S*2, D, Q*2, W*3, A*2, E]) * N
#########################################################################################

####################### Minimal Stick Lattice Conformation of Trefoil ###################
# DIRECTIONS = np.array([D*3 Q*2, W, A*2, E*3, S*2, D, Q*2, W*3, A*2, E])
#########################################################################################

"""
!!! CAUTION !!!
DO NOT append the *last* direction that completes the knot.
Example: If you wish to plot the unknot whose vertices are (0,0,0), (0,0,1), (0,1,1), (0,1,0)
Then the DIRECTIONS variable should look like:
DIRECTIONS = [W, Q, S]
"""

START = (0,0,0)

def draw_knot():
    my_knot = construct_knot(DIRECTIONS, start=START, distortion_mode="taxicab")
    my_knot.plot(bgcolor=(0,0,0), mode="tube", thickness=0.5, label_vertices=False, highlight_vertices=1)
    print("Edge length: %f" % my_knot.edge_length)
    print("Stick number: %f" % my_knot.num_sticks)
    print("Vertex Distortion: %f" % my_knot.vertex_distortion)
    print("Vertex Distortion Pairs:")
    for i, j in my_knot.vertex_distortion_pairs:
        print("%s and %s" % (my_knot.vertices[i], my_knot.vertices[j]))
    mlab.show()

draw_knot()