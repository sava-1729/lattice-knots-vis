from knots_new import *

P = 20
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
    # DIRECTIONS.append(DIRECTIONS[0]-DIRECTIONS[-1])
    return np.array(DIRECTIONS)
DIRECTIONS = get_torus_param(P)
# DIRECTIONS = np.array([D* 245, Q* 158, S* 71, A* 158, E* 245, W* 158, D* 71, Q* 158, S* 245, A* 158, E* 71])
# DIRECTIONS = np.array([D, Q*2, W*2, E*3, A*2, Q*4, D*3, S, E*2, A*2, Q*3, W*2, E*4])
mlab.figure(bgcolor=(0,0,0))
StickKnot(DIRECTIONS, validate=False).plot()
mlab.show()
