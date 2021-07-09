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
        self.vertices = vertices
        self.num_sticks = len(vertices)
        self.edge_length = sum(stick.length for stick in self.sticks)
        self.__analyse_distortion__()

    def is_point_on_knot(self, point):
        for i, s in enumerate(self.sticks):
            if s.is_point_on_stick(point):
                return i
        return -1

    def distance(self, x, y):
        x_stick_num = self.is_point_on_knot(x)
        y_stick_num = self.is_point_on_knot(y)
        assert x_stick_num != -1 and y_stick_num != -1
        if x_stick_num == y_stick_num:
            return distance_1(x, y)
        if x_stick_num > y_stick_num:
            x_stick_num, y_stick_num = y_stick_num, x_stick_num
            x, y = y, x
        dx = distance_1(x, self.sticks[x_stick_num].end)
        dy = distance_1(self.sticks[y_stick_num].start, y)
        delta_xy = sum(self.sticks[i].length for i in range(x_stick_num+1, y_stick_num))
        distance_forward = dx + delta_xy + dy
        shortest_distance = min(distance_forward, self.edge_length - distance_forward)
        return shortest_distance

    def __analyse_distortion__(self, mode="L1-norm"):
        distortion_ratios = {}
        for i in range(self.num_sticks):
            for j in range(0, i):
                vertex_i = self.vertices[i]
                vertex_j = self.vertices[j]
                distance_along_knot = self.distance(vertex_i, vertex_j)
                distance_in_space = distance_1(vertex_i, vertex_j) if mode == "L1-norm" else distance_2(vertex_i, vertex_j)
                distortion_ratios[(i,j)] = distance_along_knot / distance_in_space
        self.vertex_distortion = max(distortion_ratios.values())
        self.vertex_distortion_pairs = []
        for pair in distortion_ratios.keys():
            if distortion_ratios[pair] == self.vertex_distortion:
                self.vertex_distortion_pairs.append(pair)

    def plot(self, bgcolor=(1,1,1), highlight_vertices=True, label_vertices=True, highlight_vertex_distortion_pairs=True, stick_color=None, ref_vertex_index=-1, thickness=5, mode="line", new_figure=True):
        figure = None
        if new_figure:
            figure = create_new_figure(bgcolor=bgcolor)
        self.stick_objs = [None for i in range(len(self.sticks))]
        for i, stick in enumerate(self.sticks):
            if stick_color is not None:
                self.stick_objs[i] = stick.plot(color=stick_color, thickness=thickness, mode=mode)
            else:
                self.stick_objs[i] = stick.plot(thickness=thickness, mode=mode)
        if highlight_vertices:
            if ref_vertex_index == -1:
                self.vertex_objs = plot_3d_points(*list(zip(*self.vertices)))
                if highlight_vertex_distortion_pairs:
                    n = 0
                    for (i, j) in self.vertex_distortion_pairs:
                        X = [self.vertices[i][0], self.vertices[j][0]]
                        Y = [self.vertices[i][1], self.vertices[j][1]]
                        Z = [self.vertices[i][2], self.vertices[j][2]]
                        plot_3d_points(X, Y, Z, color=get_color(n), mode="cube")
                        n += 1
            else:
                scalar_data = self.distortion_ratios[ref_vertex_index]
                self.vertex_objs = plot_3d_points(*list(zip(*self.vertices)), scalars=scalar_data, monochromatic=False, scale_factor=1/max(scalar_data))
                vertex = self.vertices[ref_vertex_index]
                plot_3d_points([vertex[0]], [vertex[1]], [vertex[2]], color=(1,1,1), scale_factor=0.5, mode="cube")
                mlab.colorbar(object=self.vertex_objs, title="Vertex Distortion w.r.t " + str(self.vertices[ref_vertex_index]))
            if label_vertices and figure is not None:
                figure.scene.disable_render = True
                for i, v in enumerate(self.vertices):
                    mlab.text3d(v[0], v[1], v[2], str(i), scale=(0.25,0.25,0.25),color=(0.5,0.5,0.5))
                figure.scene.disable_render = False

W = np.array([0,0,1])  # +z
A = np.array([-1,0,0]) # -x
S = np.array([0,0,-1]) # -z
D = np.array([1,0,0])  # +x
Q = np.array([0,1,0])  # +y
E = np.array([0,-1,0]) # -y

def construct_knot(directions, start=(0,0,0), unit_length_sticks=False):
    origin = np.array(start)
    vertices = [origin]
    for d in directions:
        if unit_length_sticks:
            n = int(max(np.absolute(d)))
            d_unit = d / n
            for i in range(n):
                vertices.append(vertices[-1] + d_unit)
        else:
            vertices.append(vertices[-1] + d)
    return StickKnot(vertices)
