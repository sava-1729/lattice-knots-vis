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

###################################### INSTRUCTIONS ##########################################
# Edit the variable below to construct your knot!
# The constants W A S D Q E shown above represent unit movement in the respective directions.
# Replace the list below with an ordered list of directions that you want your knot to follow.
##############################################################################################

###################### Trefoil with varying 1-distortion as scaled up ####################
# N = 3 # SCALE FACTOR
# DIRECTIONS = np.array([D*31, Q*2, W, A*30, E*3, S*2, D, Q*2, W*3, A*2, E])
########################################################################################

####################### Minimal Stick Lattice Conformation of Trefoil ###################
N = 2
DIRECTIONS = np.array([D*3, Q*2, W, A*2, E*3, S*2, D, Q*2, W*3, A*2, E])# * N
#########################################################################################

######################### 44-edge, 11-vd Lattice Conformation of Trefoil ###################
# N = 10
# DIRECTIONS = np.array([D*5, Q*3, W*2, A*3, E*5, S*4, Q*4, W*2, D, W, D, E, W*3, A*4, E]) * N
############################################################################################

##################################### Minimal Unknot ####################################
# N = 5
# DIRECTIONS = np.array([D, W, A])
#########################################################################################

############################### Non-trivial VD-1 Unknot #################################
# N = 5
# DIRECTIONS = np.array([D, W, Q, A, S])
#########################################################################################

############################################ Trefoil 4 ####################################################
# DIRECTIONS = np.array([W*3, Q*4, D, S*3, E, D, S, E*2, W, E*2, A, E, A*3, W, Q*4, D*5, Q*3, S*2, A*3, E*5])
###########################################################################################################

############################################ Figure 8 ####################################################
# DIRECTIONS = np.array([D, Q*2, W*2, E*3, A*2, Q*4, D*3, S, E*2, A*2, Q*3, W*2, E*4])
###########################################################################################################
"""
!!! CAUTION !!!
DO NOT append the *last* direction that completes the knot.
Example: If you wish to plot the unknot whose vertices are (0,0,0), (0,0,1), (0,1,1), (0,1,0)
Then the DIRECTIONS variable should look like:
DIRECTIONS = [W, Q, S]
"""

START = (0,0,0)

def draw_knot(dir=DIRECTIONS, new_figure=True, show=True):
    my_knot = construct_knot(dir, start=START, distortion_mode="euclidean")
    my_knot.plot(bgcolor=(0,0,0), mode="tube", thickness=0.5, label_vertices=False, highlight_vertices=1, highlight_vertex_distortion_pairs=False, new_figure=new_figure)
    print("Edge length: %f" % my_knot.edge_length)
    print("Stick number: %f" % my_knot.num_sticks)
    print("Vertex Distortion: %f" % my_knot.vertex_distortion)
    print("Vertex Distortion Pairs:")
    for i, j in my_knot.vertex_distortion_pairs:
        print("(%d, %d) = %s and %s" % (i, j, my_knot.vertices[i], my_knot.vertices[j]))
    if show:
        mlab.show()

def analyse_2_distortion_of_knot_scalings(knot_name, max_scale_factor=6):
    vds = []
    vd_pair_dist_avg = []
    for N in range(1, max_scale_factor):
        dn = DIRECTIONS * (2**N)
        my_knot = construct_knot(dn, start=START, distortion_mode="euclidean")
        vds.append(my_knot.vertex_distortion)
        vertex_distortion_pair_distance = []
        for i, j in my_knot.vertex_distortion_pairs:
            vertex_distortion_pair_distance.append((min(abs(j-i), my_knot.edge_length - abs(j-i)) / my_knot.edge_length))
        vd_pair_dist_avg.append(mean((vertex_distortion_pair_distance)))

    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2)
    fig.suptitle("Distortion Analysis of exponential scalings of the " + knot_name + " by factors 1 to %d" % (2**max_scale_factor))
    axs[0].plot(list(range(1,N+1)), vds, color="blue")
    axs[0].set_title("Vertex 2-Distortion of N-scaling of the " + knot_name)
    axs[1].plot(list(range(1,N+1)), vd_pair_dist_avg, color="green")
    axs[1].set_title("Fractional Knot Distance b/w Vertices achieving 2-Distortion")
    plt.show()

analyse_2_distortion_of_knot_scalings("Minimal Trefoil")#, max_scale_factor=40)

# draw_knot()

# DIRECTIONS = DIRECTIONS*2
# START = (5,0,0)

# draw_knot(dir=DIRECTIONS)