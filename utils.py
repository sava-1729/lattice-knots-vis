import numpy as np
import matplotlib.colors as mcolors

COLORS = [mcolors.hex2color(clr) for clr in list(mcolors.XKCD_COLORS.values())]
NUM_COLORS = len(COLORS)

def get_color(i):
    return COLORS[i % NUM_COLORS]

def get_error_msg(name_of_erroneous_item, expected_value, actual_value):
    msg = name_of_erroneous_item + " incorrect! \n"
    msg += "Expected: %s \n" % str(expected_value)
    msg += "Given: %s \n" % str(actual_value)
    return msg

def assert_is_3d_point(x):
    assert isinstance(x, (tuple, list, np.ndarray)), get_error_msg("Point datatype", "list or tuple", type(x))
    assert len(x) == 3, get_error_msg("Point dimension", 3, len(x))
    for c in x:
        assert isinstance(c, (int, float)) or np.issubdtype(c, np.number), get_error_msg("Point coordinate datatype", "int or float", type(c))

# def assert_is_matrix(M, n):
#     assert isinstance(M, (tuple, list))
#     assert len(M) == n
#     for row in M:
#         assert isinstance(row, (tuple, list))
#         assert len(row) == n

# def mat_det_2d(M):
#     assert_is_matrix(M, 2)
#     return (M[0][0]) * (M[1][1]) - (M[1][0]) * (M[0][1])

# def mat_inv_2d(M):
#     assert mat_det_2d(M) != 0
#     A = [[0,0],[0,0]]


