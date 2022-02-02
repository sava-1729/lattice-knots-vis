from matplotlib.pyplot import axis
from sticks import *

class StickKnot:
    def __init__(self, directions, compute_distortion=True, validate=True):
        assert isinstance(directions, np.ndarray)
        self.directions = np.append(directions, [-np.sum(directions, axis=0)], axis=0)
        self.length = self.directions.shape[0]
        self.__generate_sticks__()
        if validate:
            self.__validate__()
        if compute_distortion:
            self.__compute_distortion__()

    def __generate_sticks__(self):
        N = self.length
        self.vertices = np.zeros((N, 3))
        self.vertices_loop = np.zeros((N+2, 3))
        self.sticks = [None for i in range(N)]
        for i in range(N):
            self.vertices_loop[i+1] = self.vertices_loop[i] + self.directions[i]
            self.sticks[i] = Stick(self.vertices_loop[i], self.vertices_loop[i+1], i)
        self.vertices = self.vertices_loop[:N]
        midpoint = (self.vertices_loop[0] + self.vertices_loop[1]) * 0.5
        self.vertices_loop[0] = midpoint
        self.vertices_loop[-1] = midpoint

    def __validate__(self):
        assert np.allclose(self.vertices[-1] + self.directions[-1], np.zeros(3), rtol=0)
        for i in range(self.length):
            for j in range(i+2, self.length):
                assert not self.sticks[i].intersects(self.sticks[j])

    def contains(self, point):
        return any([s.contains(point) for s in self.sticks])

    def __compute_distance_matrix__(self):
        pass

    def distance_between(self, x, y):
        pass
    def __compute_distortion__(self):
        # by iterating over vertices
        pass
    def __compute_distortion_fast__(self):
        # using numpy
        pass

    def plot(self):
        X, Y, Z = self.vertices_loop.T
        mlab.plot3d(X, Y, Z, np.arange(self.length+2), colormap='hsv', tube_radius=0.05, tube_sides=12)


class LatticeKnot(StickKnot):
    def __init__(self, directions, compute_distortion=True, divisions=1):
        assert isinstance(divisions, int)
        self.divisions = divisions
        self.unit_edge_length = 1. / divisions
        StickKnot.__init__(self, directions, compute_distortion=compute_distortion)
        pass
    def __compute_vertices__(self):
        pass
    def __validate__(self):
        pass
    def __compute_distance_matrix__(self):
        # only this needs to be changed to make distortion calculation efficient for lattice knots.
        pass
