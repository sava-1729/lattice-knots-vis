from sticks import *

class StickKnot:
    def __init__(self, vertices):
        assert isinstance(vertices, (list, tuple))
        sticks = [None for i in range(len(vertices))]
        for i in range(len(vertices)):
            sticks[i] = Stick(vertices[i-1], vertices[i], index=i)
        for i in range(len(sticks)):
            if sticks[i-1].is_parallel_to(sticks[i]):
                if np.dot(sticks[i].vector, sticks[i-1].vector) <= 0:
                    print("Sticks %d and %d are overlapping:" % (i-1, i))
                    print("DEBUG DATA:")
                    sticks[i-1].identify()
                    sticks[i].identify()
                    # exit()
            k = 1 if (i == (len(sticks)-1)) else 0
            for j in range(k, i-1):
                intersects, debug = sticks[i].is_intersecting(sticks[j])
                if intersects:
                    print("Sticks %d and %d are intersecting:" % (j, i))
                    print("DEBUG DATA:")
                    sticks[j].identify()
                    sticks[i].identify()
                    print(debug)
                    # exit()
        self.sticks = sticks
        self.vertices = [v for v in vertices]
        self.num_sticks = len(self.vertices)
        self.distortion_ratios = [[1 for i in range(self.num_sticks)] for i in range(self.num_sticks)]
        for i in range(len(vertices)):
            for j in range(0, i):
                distance_along_knot_forward = sum(sticks[k].length for k in range(j+1, i+1))
                distance_along_knot_backward = sum(sticks[k].length for k in range(len(sticks))) - distance_along_knot_forward
                distance_along_knot = min(distance_along_knot_forward, distance_along_knot_backward)
                distance_taxicab = sum(np.absolute(self.vertices[j] - self.vertices[i]))
                self.distortion_ratios[i][j] = distance_along_knot / distance_taxicab
                self.distortion_ratios[j][i] = distance_along_knot / distance_taxicab
        max_distortion_ratios = [1 for i in range(self.num_sticks)]
        max_distortion_ratios_indices = [0 for i in range(self.num_sticks)]
        for i, x in enumerate(self.distortion_ratios):
            max_distortion_ratios[i] = max(x)
            max_distortion_ratios_indices[i] = argmax(x)
        max_index = argmax(max_distortion_ratios)
        self.vertex_distortion_pair_indices = (max_index, max_distortion_ratios_indices[max_index])
        self.vertex_distortion = max(max_distortion_ratios)

    def plot(self, bgcolor=(1,1,1), highlight_vertices=True, highlight_vertex_distortion_pair=True, stick_color=None, ref_vertex_index=-1, thickness=5, mode="line", new_figure=True):
        if new_figure:
            create_new_figure(bgcolor=bgcolor)
        self.stick_objs = [None for i in range(len(self.sticks))]
        for i, stick in enumerate(self.sticks):
            if stick_color is not None:
                self.stick_objs[i] = stick.plot(color=stick_color, thickness=thickness, mode=mode)
            else:
                self.stick_objs[i] = stick.plot(thickness=thickness, mode=mode)
        if highlight_vertices:
            if ref_vertex_index == -1:
                self.vertex_objs = plot_3d_points(*list(zip(*self.vertices)))
                if highlight_vertex_distortion_pair:
                    self.vertex_objs = plot_3d_points(*list(zip(*self.vertices)))
                    i, j = self.vertex_distortion_pair_indices
                    X = [self.vertices[i][0], self.vertices[j][0]]
                    Y = [self.vertices[i][1], self.vertices[j][1]]
                    Z = [self.vertices[i][2], self.vertices[j][2]]
                    plot_3d_points(X, Y, Z, color=(1,1,1), mode="cube", scale_factor=0.5)
            else:
                scalar_data = self.distortion_ratios[ref_vertex_index]
                self.vertex_objs = plot_3d_points(*list(zip(*self.vertices)), scalars=scalar_data, monochromatic=False, scale_factor=1/max(scalar_data))
                vertex = self.vertices[ref_vertex_index]
                plot_3d_points([vertex[0]], [vertex[1]], [vertex[2]], color=(1,1,1), scale_factor=0.5, mode="cube")
                mlab.colorbar(object=self.vertex_objs, title="Vertex Distortion w.r.t " + str(self.vertices[ref_vertex_index]))

W = np.array([0,0,1])  # +z
A = np.array([-1,0,0]) # -x
S = np.array([0,0,-1]) # -z
D = np.array([1,0,0])  # +x
Q = np.array([0,1,0])  # +y
E = np.array([0,-1,0]) # -y

def construct_knot(directions, start=(0,0,0)):
    origin = np.array(start)
    vertices = [origin]
    for d in directions:
        vertices.append(vertices[-1] + d)
    return StickKnot(vertices)
