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

DIRECTIONS = []

###################################### TORUS KNOTS ###########################################

################################## K_p (Campisi-Cazet) #######################################
P = 10
def get_torus_param(P):
    DIRECTIONS = []
    x_len = 2
    sign = 1
    for i in range(1, 2*P - 1):
        y_len = (P - 1) if i % 2 == 1 else P
        DIRECTIONS.append(sign * W * (2*P - i))
        DIRECTIONS.append(sign * D * x_len)
        DIRECTIONS.append(sign * Q * y_len)
        if i % 2 == 1:
            x_len += 1
        sign = -sign
    DIRECTIONS.append(sign * W * 1)
    DIRECTIONS.append(sign * D * P)
    DIRECTIONS.append(sign * Q * (2*P - 1))
    sign = -sign
    DIRECTIONS.append(sign * W * P)
    DIRECTIONS.append(sign * D * 1)
    return DIRECTIONS
DIRECTIONS = get_torus_param(P)

################################### Toroidal Unknot ########################################
# DIRECTIONS = [D, Q, S, D, E, W, D, Q*2, A, S, Q, D, W, Q, A*2, E, S, A, Q, W, A, E*2, D, S, E, A, W, E]
# N = 30
# DIRECTIONS = []
# for i in range(N):
#     DIRECTIONS = DIRECTIONS + [D, Q, S, D, E, W, D]
# DIRECTIONS.append(Q)
# for i in range(N):
#     DIRECTIONS = DIRECTIONS + [Q, A, S, Q, D, W, Q]
# DIRECTIONS.append(A)
# for i in range(N):
#     DIRECTIONS = DIRECTIONS + [A, E, S, A, Q, W, A]
# DIRECTIONS.append(E)
# for i in range(N):
#     DIRECTIONS = DIRECTIONS + [E, D, S, E, A, W, E]

####################################### TREFOILS #############################################

####################### Minimal Stick Lattice Conformation of Trefoil ###################
# N = 25
# DIRECTIONS = np.array([D*3, Q*2, W, A*2, E*3, S*2, D, Q*2, W*3, A*2, E])*N

######################### 10.5-vd Lattice Conformation of Trefoil #####################
# N = 5
# DIRECTIONS = np.array([D*9, Q*6, W*4, A*5, E*3, A*1, E*2, D*1, E*5, S*8, Q*8, W*4, D*1, W*1, D*1, W*1, D*1, E*2, W*6, A*7, E*2])*N

######################### 10.33-vd Lattice Conformation of Trefoil #####################
# N = 1
# DIRECTIONS = np.array([D*8, Q*5, W*4, A*5, E*5, D, E*4, S*8, Q*8, W*5, E, D, W, D, E, W, D, E, W*5, A*7, E*1])*N

##################### Trefoil with varying 1-distortion as scaled up ####################
# N = 3
# DIRECTIONS = np.array([D*31, Q*2, W, A*30, E*3, S*2, D, Q*2, W*3, A*2, E])*N

################################### David's Trefoil ######################################
# N = 1
# DIRECTIONS = np.array([D * 32, Q * 21, W * 10, A * 21, E * 32, S * 21, D * 10, Q * 21, W * 32, A * 21, E * 10])*N

######################### 44-edge, 11-vd Lattice Conformation of Trefoil #####################
# N = 1
# DIRECTIONS = np.array([D*5, Q*3, W*2, A*3, E*5, S*4, Q*4, W*2, D, W, D, E, W*3, A*4, E])*N

################################# Curvy Trefoil 4 ############################################
# DIRECTIONS = np.array([W*3, Q*4, D, S*3, E, D, S, E*2, W, E*2, A, E, A*3, W, Q*4, D*5, Q*3, S*2, A*3, E*5])
##############################################################################################

####################################### UNKNOTS #############################################

##################################### Minimal Unknot ####################################
# N = 1
# DIRECTIONS = np.array([D, W, A]) *N

############################### Non-trivial VD-1 Unknot #################################
# N = 2
# DIRECTIONS = np.array([D, W, Q, A, S])*N

########################## 1-distortion constant on scaling #############################
# N = 2
# DIRECTIONS = np.array([D, Q, A, S, E, D, E, W, A])*N
#########################################################################################

##################################### Rectangle #####################################
# N = 6
# DIRECTIONS = np.array([D*N, W, A*N])
#########################################################################################

##################################### Two L's #####################################
# N = 20
# DIRECTIONS = np.array([D*N, W*N*2, A*N*2, S*N, A*N, S*N*2, D*N*2])
#########################################################################################

####################################### FIGURE 8 #############################################

############################# Minimal Stick Number Conformation ##############################
# N = 1
# DIRECTIONS = np.array([D, Q*2, W*2, E*3, A*2, Q*4, D*3, S, E*2, A*2, Q*3, W*2, E*4])*N
###########################################################################################################

########################## Replicating Standard Smooth Conformation ##########################
# N = 1
# DIRECTIONS = np.array([D, W*2, D*2, Q*6, A*7, S, E*7, D*6, Q*2, A*3, S, E*5, D*6, W*3, Q*7, A*5, S*3])*N
###########################################################################################################
# N = 1
# DIRECTIONS = np.array([D*2, Q*6, S*2, A*2, S*2, E*6, D*2, E*6, W*2, A*2, W*2])*N

########################## Twisted Brunnian 3-link ##########################
# components = [None, None, None]
# starts = [None, None, None]
# components[0] = np.array([D*8, Q*4, A*8])
# starts[0] = (0,0,0)
# components[1] = np.array([Q*5, D*4, E*5, S*2, Q*5, A*4, E*5])
# starts[1] = (2,3,1)
# components[2] = np.array([Q*6, S*2, E*6])
# starts[2] = (4,-1,1)

########################## Brunnian 3-link + extra-link ##########################
# components = [None, None, None, None]
# starts = [None, None, None, None]
# components[0] = np.array([D*4, Q*4, W*4, A*4, S*4])
# starts[0] = (0,0,0)
# components[1] = np.array([D*6, S*2, A*6])
# starts[1] = (-1,2,1)
# components[2] = np.array([D*6, Q*2, A*6])
# starts[2] = (-1,3,2)
# components[3] = np.array([Q*6, S*6, E*6])
# starts[3] = (2,1,3)

########################## Supposed Brunnian 4-link ##########################
# components = [None, None, None, None]
# starts = [None, None, None, None]
# components[0] = np.array([D*4, Q*4, W*4, A*4, S*4])
# starts[0] = (0,0,0)
# components[1] = np.array([D*6, S*2, A*6])
# starts[1] = (-1,2,1)
# components[2] = np.array([D*6, Q*2, A*6])
# starts[2] = (-1,3,2)
# components[3] = np.array([Q*6, S*6, E*6])
# starts[3] = (2,1,3)

######################### Brunnian 3-link with odd stick number ##########################
# components = [None, None, None]
# starts = [None, None, None]
# components[0] = np.array([E*4, S*2, D*3, Q*2, W, D, Q*2, A*4])
# starts[0] = (0,0,0)
# components[1] = np.array([W*4, D*6, S*4])
# starts[1] = (-1,-2,-3)
# components[2] = np.array([E*2, S*6, Q*2])
# starts[2] = (2,-1, 2)

# # BEST
# DIRECTIONS = np.array([D* 245, Q* 158, S* 71, A* 158, E* 245, W* 158, D* 71, Q* 158, S* 245, A* 158, E* 71])

#########################################
# A generic trefoil conformation. This cannot have distortion less than 11
# 11 is achieved iff b = 2a

# a = 30
# b = 70
# b must be bigger than a

# DIRECTIONS = np.array([D*b, Q*a, S*(a+b), A*a, E*b, W*b, Q*(a+b), D*a*2, S*a, E*a*2, A*(a+b)])
#########################################

#########################################
# Another generic trefoil conformation. This cannot have distortion less than 9.89897948557...
# Minima is achieved iff b/a = 1+sqrt(1.5)

# a = 4
# b = 9
# # b must be bigger than a

# DIRECTIONS = np.array([D*(2*b-a), Q*b + Q, S*a, A*b, E*(2*b-a) + E, W*b, D*a, Q*b + Q, S*(2*b-a), A*b, E*a + E])
#########################################

################ c > b < a #################
# a = 2
# b = 1
# c = 2


# DIRECTIONS = np.array([D*a, Q*b, S*(a+c-b), A*b, E*c, W*a, Q*(a+c-b), D*c, S*b, E*a, A*(a+c-b)])
# DIRECTIONS = np.array([D*(a-b+c), Q*c, S*b, A*a, E*(a-b+c), W*c, D*b, Q*a, S*(a-b+c), A*c, E*b])
#########################################

"""
!!! CAUTION !!!
DO NOT append the *last* direction that completes the knot.
Example: If you wish to plot the unknot whose vertices are (0,0,0), (0,0,1), (0,1,1), (0,1,0)
Then the DIRECTIONS variable should look like:
DIRECTIONS = [W, Q, S]
"""

START = (0,0,0)
SHOW = True

def draw_knot(dir=DIRECTIONS, start=START, new_figure=True, show=SHOW, div=1, color=None):
    my_knot = construct_knot(dir, start=start, distortion_mode="taxicab", div=div)
    print("Edge length: %f" % my_knot.edge_length)
    print("Stick number: %f" % my_knot.num_sticks)
    print("Vertex Distortion: %f" % my_knot.vertex_distortion)
    print("Euclidean Vertex Distortion: %f" % my_knot.vertex_distortion_euclidean)
    print("Taxicab Vertex Distortion: %f" % my_knot.vertex_distortion_taxicab)
    print("Vertex Distortion Pairs:")
    for i, j in my_knot.vertex_distortion_pairs:
        print("(%d, %d) = %s and %s" % (i, j, my_knot.vertices[i], my_knot.vertices[j]))
    if show:
        my_knot.plot(bgcolor=(0,0,0), mode="tube", thickness=0.5, label_vertices=False, highlight_vertices=1, highlight_vertex_distortion_pairs=False, new_figure=new_figure, highlight_high_distortion_pairs=True, ref_vertex_index=-1, stick_color=(0,0,0))
        mlab.show()
    return my_knot

def analyse_2_distortion_of_knot_scalings(knot_name, max_scale_factor=20):
    vds = []
    vd_pair_dist_avg = []
    for N in range(1, max_scale_factor+1):
        dn = DIRECTIONS*N #(2**N)
        my_knot = construct_knot(dn, start=START, distortion_mode="taxicab")#, div=8)
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

def draw_link(components, starts):
    knot_cmps = []
    for i, knot in enumerate(components):
        knot_cmps.append(draw_knot(dir=knot, start=starts[i], new_figure=(i==0), color=colormap.hsv(i/len(components))[:3], show=False))
    print("Stick Number: %d" % sum([k.num_sticks for k in knot_cmps]))
    print("Edge Length: %d" % sum([k.edge_length for k in knot_cmps]))
    mlab.show()

# draw_link(components, starts)
draw_knot(DIRECTIONS, div=5)
# my_knot = draw_knot(DIRECTIONS, show=False)
# dist = my_knot.distance(my_knot.vertices[0]+np.array([0.5,0,0]),my_knot.vertices[0]+np.array([0.5,0,-4]))
# print("DISTANCE between midpoints: %f" % dist)
# dist = my_knot.distance(my_knot.vertices[0]+np.array([0.5,0,0]),my_knot.vertices[0]+np.array([0.5,0,-4]))
# print("DISTANCE between midpoints: %f" % dist)
# draw_knot(DIRECTIONS, start=(4,0,0), new_figure=False, div=2, show=False)

# draw_knot(DIRECTIONS, start=(8,0,0), new_figure=False, div=4)

# draw_knot()
# start = (0,0,0)
# P_max = 10
# for p in range(3, P_max+1):
#     start = (start[0] + p + (p//2), 0, 0)
#     draw_knot(get_torus_param(p), new_figure=(p==3), start=start, show=(p==P_max))

# create_new_figure()
# my_knot = draw_knot(DIRECTIONS, start=(0,0,0), show=False, new_figure=False)
# my_knot = draw_knot(DIRECTIONS*2, start=(8,0,0), new_figure=False)

# d1_distances_between_antipodals = []
# for i in range(my_knot.num_vertices//2):
#     x = my_knot.vertices[i]
#     y = my_knot.vertices[i - (my_knot.num_vertices//2)]
#     print((x,y))
#     d1_distances_between_antipodals.append(distance_taxicab(x, y))

# print(d1_distances_between_antipodals)
# print(sum(d1_distances_between_antipodals))#/len(d1_distances_between_antipodals))
# print(my_knot.edge_length)


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