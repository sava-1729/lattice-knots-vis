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

####################################### TREFOILS #############################################

####################### Minimal Stick Lattice Conformation of Trefoil ###################
# N = 1
# DIRECTIONS = np.array([D*3, Q*2, W, A*2, E*3, S*2, D, Q*2, W*3, A*2, E])*N

######################### 10.5-vd Lattice Conformation of Trefoil #####################
N = 1
DIRECTIONS = [D*9, Q*6, W*4, A*5, E*3, A*1, E*2, D*1, E*5, S*8, Q*8, W*4, D*1, W*1, D*1, W*1, D*1, E*2, W*6, A*7, E*2]*N

##################### Trefoil with varying 1-distortion as scaled up ####################
# N = 3
# DIRECTIONS = np.array([D*31, Q*2, W, A*30, E*3, S*2, D, Q*2, W*3, A*2, E])*N

######################### 44-edge, 11-vd Lattice Conformation of Trefoil #####################
# N = 2
# DIRECTIONS = np.array([D*5, Q*3, W*2, A*3, E*5, S*4, Q*4, W*2, D, W, D, E, W*3, A*4, E])*N

################################# Curvy Trefoil 4 ############################################
# DIRECTIONS = np.array([W*3, Q*4, D, S*3, E, D, S, E*2, W, E*2, A, E, A*3, W, Q*4, D*5, Q*3, S*2, A*3, E*5])
##############################################################################################

####################################### UNKNOTS #############################################

##################################### Minimal Unknot ####################################
# N = 8
# DIRECTIONS = np.array([D, W, A]) *N

############################### Non-trivial VD-1 Unknot #################################
# N = 5
# DIRECTIONS = np.array([D, W, Q, A, S])*N

########################## 1-distortion constant on scaling #############################
# N = 2
# DIRECTIONS = np.array([D, Q, A, S, E, D, E, W, A])*N
#########################################################################################

####################################### FIGURE 8 #############################################

############################# Minimal Stick Number Conformation ##############################
# N = 1
# DIRECTIONS = np.array([D, Q*2, W*2, E*3, A*2, Q*4, D*3, S, E*2, A*2, Q*3, W*2, E*4])*N
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
    my_knot = construct_knot(dir, start=START, distortion_mode="taxicab")
    my_knot.plot(bgcolor=(0,0,0), mode="tube", thickness=0.5, label_vertices=False, highlight_vertices=1, highlight_vertex_distortion_pairs=True, new_figure=new_figure, highlight_high_distortion_pairs=False, ref_vertex_index=-1, stick_color=None)
    print("Edge length: %f" % my_knot.edge_length)
    print("Stick number: %f" % my_knot.num_sticks)
    print("Euclidean Vertex Distortion: %f" % my_knot.vertex_distortion_euclidean)
    print("Taxicab Vertex Distortion: %f" % my_knot.vertex_distortion_taxicab)
    print("Vertex Distortion Pairs:")
    for i, j in my_knot.vertex_distortion_pairs:
        print("(%d, %d) = %s and %s" % (i, j, my_knot.vertices[i], my_knot.vertices[j]))
    if show:
        mlab.show()

def analyse_2_distortion_of_knot_scalings(knot_name, max_scale_factor=64):
    vds = []
    vd_pair_dist_avg = []
    for N in range(1, max_scale_factor+1):
        dn = DIRECTIONS*N #(2**N)
        my_knot = construct_knot(dn, start=START, distortion_mode="euclidean", div=8)
        vds.append(my_knot.vertex_distortion)
        vertex_distortion_pair_distance = []
        for i, j in my_knot.vertex_distortion_pairs:
            vertex_distortion_pair_distance.append((min(abs(j-i), my_knot.edge_length - abs(j-i)) / my_knot.edge_length))
        vd_pair_dist_avg.append(mean((vertex_distortion_pair_distance)))

    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2)
    fig.suptitle("Distortion Analysis of scalings of the " + knot_name)
    axs[0].plot(list(range(1,max_scale_factor+1)), vds, color="blue")
    axs[0].scatter(list(range(1,max_scale_factor+1)), vds, color="black", s=9)
    exp_scalings = [(2**i, vds[2**i-1]) for i in range(int(log2(max_scale_factor)+1))]
    axs[0].scatter(*list(zip(*exp_scalings)), color="red", zorder=10, s=25)
    axs[0].set_title("Vertex 2-Distortion of N-scalings of the " + knot_name)
    axs[0].grid(color='tab:gray', linestyle="--")
    axs[1].plot(list(range(1,max_scale_factor+1)), vd_pair_dist_avg, color="green")
    axs[1].scatter(list(range(1,max_scale_factor+1)), vd_pair_dist_avg, color="black", s=9)
    exp_scalings = [(2**i, vd_pair_dist_avg[2**i-1]) for i in range(int(log2(max_scale_factor)+1))]
    axs[1].scatter(*list(zip(*exp_scalings)), color="red", zorder=10, s=25)
    axs[1].set_title("Fractional Knot Distance b/w Vertices achieving 2-Distortion")
    axs[1].grid(color='tab:gray', linestyle="--")
    plt.show()

draw_knot()
# analyse_2_distortion_of_knot_scalings("Max-Cubed Unknot")#, max_scale_factor=40)
# k1 = construct_knot(DIRECTIONS, start=START, div=2)

# # DIRECTIONS = DIRECTIONS*2
# START = (5,0,0)
# k2 = construct_knot(DIRECTIONS, start=START, div=3)

# START = (-5,0,0)

# k3 = construct_knot(DIRECTIONS, start=START, div=1)



# k1.plot(bgcolor=(0,0,0), mode="tube", thickness=0.5, label_vertices=False, highlight_vertices=1, highlight_vertex_distortion_pairs=False, new_figure=True)

# k2.plot(bgcolor=(0,0,0), mode="tube", thickness=0.5, label_vertices=False, highlight_vertices=1, highlight_vertex_distortion_pairs=False, new_figure=False)

# k3.plot(bgcolor=(0,0,0), mode="tube", thickness=0.5, label_vertices=False, highlight_vertices=1, highlight_vertex_distortion_pairs=False, new_figure=False)

# mlab.show()