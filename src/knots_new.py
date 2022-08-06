"""
This file contains the StickKnot class which is used to construct
knots and efficiently compute their distortion.
Copyright (C) 2022-23 Vatsal Srivastava

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can find a copy of the GNU General Public License in the root
directory of this repository, named `LICENSE.md`.
If you do not find it, see <https://www.gnu.org/licenses/>.
"""


from sticks import *

class StickKnot(object):
    def __init__(self, directions, compute_distortion=True, validate=True, mode="euclidean"):
        assert isinstance(directions, (np.ndarray, list, tuple))
        self._store_directions(directions)
        self._generate_sticks()
        if validate:
            self._validate()
        if compute_distortion:
            self.mode = mode
            self._compute_distortion_fast()


    def _store_directions(self, directions):
        self.num_vertices = len(directions)
        self.directions = np.zeros((self.num_vertices, 3))
        for i, d in enumerate(directions):
            assert isinstance(d, Direction)
            self.directions[i] = d.get_vector()


    def _generate_sticks(self):
        N = self.num_vertices
        self.vertices = np.zeros((N, 3))
        self.vertices_loop = np.zeros((N+2, 3))
        self.sticks = [None for i in range(N)]
        for i in range(N):
            self.vertices_loop[i+1] = self.vertices_loop[i] + self.directions[i]
            self.sticks[i] = Stick(self.vertices_loop[i], self.vertices_loop[i+1], i)
        self.vertices[:] = self.vertices_loop[:N]
        midpoint = (self.vertices_loop[0] + self.vertices_loop[1]) * 0.5
        self.vertices_loop[0] = midpoint
        self.vertices_loop[-1] = midpoint


    def _validate(self):
        assert np.allclose(self.vertices[-1] + self.directions[-1], np.zeros(3), rtol=0)
        for i in range(self.num_vertices):
            for j in range(i+2, self.num_vertices-1 if i == 0 else self.num_vertices):
                assert not self.sticks[i].intersects(self.sticks[j])


    def contains(self, point):
        return any([s.contains(point) for s in self.sticks])


    def _compute_distance_matrix(self):
        N = self.num_vertices
        O = np.ones((N, N))
        diag_b = np.identity(N, dtype=bool)
        self.distance_matrix = np.zeros((N, N))
        self.distance_matrix[diag_b] = [s.length for s in self.sticks]
        self.total_length = np.trace(self.distance_matrix)
        self.distance_matrix = np.triu(O) @ (self.distance_matrix @ np.triu(O, k=1))
        self.distance_matrix = np.minimum(self.total_length - self.distance_matrix, self.distance_matrix)
        Lt_b = np.tril(np.full((N, N), True), k=-1)
        self.distance_matrix[Lt_b] = (self.distance_matrix.T)[Lt_b]


    def distance_between(self, x, y):
        pass


    def _compute_distortion(self):
        # by iterating over vertices
        pass


    def _compute_distortion_fast(self):
        N = int(self.num_vertices)
        O = np.ones((N, N))
        Tr = np.full((N, N), True)
        UT_b = np.triu(Tr, k=1)
        X = O * self.vertices[:, 0]
        Y = O * self.vertices[:, 1]
        Z = O * self.vertices[:, 2]
        self._compute_distance_matrix()
        D_knot = self.distance_matrix

        D_euclidean = np.zeros_like(X)
        D_euclidean[UT_b] = np.sqrt(np.abs(X[UT_b] - X.T[UT_b])**2 + \
                                    np.abs(Y[UT_b] - Y.T[UT_b])**2 + \
                                    np.abs(Z[UT_b] - Z.T[UT_b])**2)
        distortion_ratios = {"euclidean": np.ones_like(X)}
        distortion_ratios["euclidean"][UT_b] = D_knot[UT_b] / D_euclidean[UT_b]
        distortion_ratios["euclidean"][UT_b.T] = (distortion_ratios["euclidean"].T)[UT_b.T]

        if self.mode == "taxicab":
            D_taxicab = np.zeros_like(X)
            D_taxicab[UT_b] = np.abs(X[UT_b] - X.T[UT_b]) + \
                                np.abs(Y[UT_b] - Y.T[UT_b]) + \
                                np.abs(Z[UT_b] - Z.T[UT_b])
            distortion_ratios["taxicab"] = np.ones_like(X)
            distortion_ratios["taxicab"][UT_b] = D_knot[UT_b] / D_taxicab[UT_b]
            distortion_ratios["taxicab"][UT_b.T] = (distortion_ratios["taxicab"].T)[UT_b.T]

        self.distortion_ratios = distortion_ratios
        self.highest_distortion_ratio_of_vertex = np.amax(self.distortion_ratios[self.mode], 0)
        self.vertex_distortion = np.amax(distortion_ratios[self.mode][UT_b]) # self.highest_distortion_ratio_of_vertex)
        XY = np.mgrid[0:N, 0:N]
        self.vertex_distortion_pairs = XY[:, np.isclose(distortion_ratios[self.mode], self.vertex_distortion, rtol=0)].T
        print(self.vertex_distortion_pairs.shape)
        self.highest_distortion_ratio_of_vertex_loop = np.empty((N+2,))
        self.highest_distortion_ratio_of_vertex_loop[:N] = self.highest_distortion_ratio_of_vertex
        b, a = self.highest_distortion_ratio_of_vertex[0], self.highest_distortion_ratio_of_vertex[-1]
        self.highest_distortion_ratio_of_vertex_loop[N] = (a + (2. * b))/3
        self.highest_distortion_ratio_of_vertex_loop[N+1] = (b + (2. * a))/3


    def plot(self, scalars=None, colormap=None, colorbar=True, scene_mlab=None):
        if scene_mlab is None:
            scene_mlab = mlab
        if scalars is None:
            self.default_plot_scalars = np.arange(self.num_vertices+2)
            scalars = self.default_plot_scalars
        if colormap is None:
            colormap = "hsv"
        X, Y, Z = self.vertices_loop.T
        args = [X, Y, Z, scalars]
        kwargs = {"colormap": colormap, "tube_radius": 0.05, "tube_sides": 12}
        self.plot_obj = scene_mlab.plot3d(*args, **kwargs)
        # scene_mlab.colorbar(object=self.plot_obj, title="Colorbar", orientation="horizontal")
        return self.plot_obj


class LatticeKnot(StickKnot):
    def __init__(self, directions, mode="taxicab", **kwargs):
        assert isinstance(directions, (np.ndarray, list, tuple))
        super().__init__(directions, mode=mode, **kwargs)


    def _store_directions(self, directions):
        lengths = [0 for d in directions]
        self.num_vertices = 0
        for i, d in enumerate(directions):
            assert isinstance(d, Direction)
            assert d.type_ is int
            v = d.get_vector()
            flag = False
            # write the code in the for loop more efficiently, check axial directions in a single line
            for v_j in v:
                if v_j != 0:
                    if flag is True:
                        raise ValueError("Expected axial directions only.")
                    flag = True
                    self.num_vertices += abs(v_j)
                    lengths[i] = abs(v_j)
        self.directions = np.zeros((self.num_vertices, 3))
        index = 0
        for i, d in enumerate(directions):
            for j in range(lengths[i]):
                self.directions[index] = d.get_vector() // lengths[i]
                index += 1


    # def _validate(self):
    #     pass


    def _compute_distance_matrix(self):
        N = int(self.num_vertices)
        O = np.ones((N, N))
        Tr = np.full((N, N), True)
        UT_b = np.triu(Tr)
        D_knot = O * np.arange(N)
        D_knot[UT_b] = np.abs(D_knot[UT_b] - D_knot.T[UT_b])
        D_knot[UT_b] = np.minimum(D_knot[UT_b], N - D_knot[UT_b])
        D_knot[UT_b.T] = (D_knot.T)[UT_b.T]
        self.distance_matrix = D_knot
