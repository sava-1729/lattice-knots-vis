from knots import *

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

my_knot = construct_knot(DIRECTIONS)
my_knot.plot()
mlab.show()