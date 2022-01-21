from sticks import *

PROGRESS_UPDATES = False

class StickKnot:
    def __init__(self, vertices, analyse_distortion=True, distortion_mode="taxicab"):
        assert isinstance(vertices, (list, tuple))
        self.vertices = deepcopy(vertices)
        self.critical_vertices = []
        for i in range(len(vertices)):
            assert any(vertices[i] != vertices[i-1])
            v_prev = [p - q for (p, q) in zip(vertices[i-1], vertices[i])]
            v_next = [p - q for (p, q) in zip(vertices[i], vertices[(i+1) % len(vertices)])]
            if are_vectors_parallel(v_prev, v_next):
                continue
            if len(self.critical_vertices) == 0:
                self.critical_vertices.append(vertices[i])
            elif any(vertices[i] != self.critical_vertices[-1]): # HACK - TO BE REMOVED
                self.critical_vertices.append(vertices[i])
        if PROGRESS_UPDATES:
            print("############ Critical Vertices Identified ############", flush=True)
        sticks = [None for v in self.critical_vertices]
        for i in range(len(self.critical_vertices)):
            sticks[i] = Stick(self.critical_vertices[i-1], self.critical_vertices[i], index=i)
        if PROGRESS_UPDATES:
            print("############ Stick Objects Constructed ############", flush=True)
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
        if PROGRESS_UPDATES:
            print("############ Checked. Valid Knot. ############", flush=True)
        self.sticks = sticks
        self.edges = [Stick(vertices[i-1], vertices[i]) for i in range(len(vertices))]
        self.num_sticks = len(sticks)
        self.num_vertices = len(vertices)
        self.edge_length = sum(stick.length for stick in self.sticks)

        # assert self.edge_length == self.num_vertices
        if analyse_distortion:
            self.__analyse_distortion__()
            if PROGRESS_UPDATES:
                print("############ Distortion Analysis Complete ############", flush=True)
            print(distortion_mode)
            print(distortion_mode=="taxicab")
            if distortion_mode == "taxicab":
                self.vertex_distortion = self.vertex_distortion_taxicab
                self.vertex_distortion_pairs = self.vertex_distortion_pairs_taxicab
            else:
                self.vertex_distortion = self.vertex_distortion_euclidean
                self.vertex_distortion_pairs = self.vertex_distortion_pairs_euclidean
            self.distortion_mode = distortion_mode
        self.__setup_colors__()

    def __setup_colors__(self):
        l = 0
        for s in self.sticks:
            s.id = l/(self.edge_length)
            l += s.length

    def is_point_on_knot(self, point):
        for i, s in enumerate(self.edges):
            if s.is_point_on_stick(point):
                return i
        return -1

    def distance(self, x, y):
        x_edge_num = self.is_point_on_knot(x)
        y_edge_num = self.is_point_on_knot(y)
        assert x_edge_num != -1 and y_edge_num != -1
        if x_edge_num == y_edge_num:
            return distance_taxicab(x, y)
        if x_edge_num > y_edge_num:
            x_edge_num, y_edge_num = y_edge_num, x_edge_num
            x, y = y, x
        dx = distance_taxicab(x, self.edges[x_edge_num].end)
        dy = distance_taxicab(self.edges[y_edge_num].start, y)
        delta_xy = sum(self.edges[i].length for i in range(x_edge_num+1, y_edge_num))
        distance_forward = dx + delta_xy + dy
        shortest_distance = min(distance_forward, self.edge_length - distance_forward)
        return shortest_distance

    def __analyse_distortion_fast__(self):
        # INCOMPLETE
        N = self.edge_length
        O = np.ones((N, N))
        UT = np.triu(O, k=1)
        UT_b = np.triu(O, k=1, dtype=bool)
        X = UT * self.vertices[:, 0]
        Y = UT * self.vertices[:, 1]
        Z = UT * self.vertices[:, 2]
        D_knot = UT * np.arange(N)
        D_taxicab = np.zeros_like(X)
        D_taxicab[UT_b] = np.abs(X[UT_b] - X.T[UT_b]) + \
                               np.abs(Y[UT_b] - Y.T[UT_b]) + \
                               np.abs(Z[UT_b] - Z.T[UT_b])
        

    def __analyse_distortion__(self):
        distortion_ratios = {}
        max_knot_dist = int(self.edge_length) // 2
        for d in range(1, max_knot_dist + 1):
            for i in range(self.num_vertices):
                j = (i - d) % self.num_vertices
                if (j, i) in distortion_ratios.keys():
                    if d != max_knot_dist:
                        print("Distortion Analysis: Strange Case.")
                    continue
                vertex_1 = self.vertices[i]
                vertex_2 = self.vertices[j]
                euclidean_distance = distance_euclidean(vertex_1, vertex_2)
                taxicab_distance = distance_taxicab(vertex_1, vertex_2)
                if euclidean_distance > 0 and taxicab_distance > 0:
                    distortion_ratios[(i,j)] = {}
                    distortion_ratios[(i,j)]["euclidean"] = d / euclidean_distance
                    distortion_ratios[(i,j)]["taxicab"] = d / taxicab_distance
        self.vertex_distortion_euclidean = max(dr["euclidean"] for dr in distortion_ratios.values())
        self.vertex_distortion_taxicab = max(dr["taxicab"] for dr in distortion_ratios.values())
        self.vertex_distortion_pairs_euclidean = []
        self.vertex_distortion_pairs_taxicab = []
        for pair in distortion_ratios.keys():
            if distortion_ratios[pair]["euclidean"] == self.vertex_distortion_euclidean:
                self.vertex_distortion_pairs_euclidean.append(pair)
            if distortion_ratios[pair]["taxicab"] == self.vertex_distortion_taxicab:
                self.vertex_distortion_pairs_taxicab.append(pair)
        self.distortion_ratios = distortion_ratios

    def plot(self, bgcolor=(1,1,1), highlight_vertices=0, label_vertices=True, highlight_vertex_distortion_pairs=True, stick_color=None, thickness=5, mode="line", new_figure=True, ref_vertex_index=-1, highlight_high_distortion_pairs=False):
        figure = None
        if new_figure:
            figure = create_new_figure(bgcolor=bgcolor)
        else:
            figure = mlab.gcf()
        if highlight_high_distortion_pairs:
            stick_color = (0.5,0.5,0.5)
        self.stick_objs = [None for i in range(len(self.sticks))]
        self.all_visual_objects = []
        for i, stick in enumerate(self.sticks):
            if stick_color is not None:
                self.stick_objs[i] = stick.plot(color=stick_color, thickness=thickness, mode=mode)
            else:
                self.stick_objs[i] = stick.plot(thickness=thickness, mode=mode)
            self.all_visual_objects.append(self.stick_objs[i])
        if highlight_vertices >= 0:
            if ref_vertex_index == -1:
                if highlight_high_distortion_pairs:
                    labels = ["" for i in range(self.num_vertices)]
                    scalar_data = [0 for i in range(self.num_vertices)]
                    for i in range(self.num_vertices):
                        i_dist_ratios = [d[self.distortion_mode] for (pair, d) in self.distortion_ratios.items() if i in pair]
                        i_partners = [sum(pair)-i for pair in self.distortion_ratios.keys() if i in pair]
                        scalar_data[i] = max(i_dist_ratios)
                        j = i_partners[i_dist_ratios.index(scalar_data[i])]
                        labels[i] = "(%d, %d)" % (i, j)
                    vertex_objs = plot_3d_points(*list(zip(*self.vertices)), scalars=scalar_data, monochromatic=False, scale_factor=0.5/max(scalar_data))
                    mlab.colorbar(object=vertex_objs, title="High Vertex Distortion Ratios", orientation="vertical")
                    if label_vertices:
                        figure.scene.disable_render = True
                        for i, v in enumerate(self.vertices):
                            mlab.text3d(v[0], v[1]+0.2, v[2], labels[i], scale=(0.15,0.15,0.15),color=(0.5,0.5,0.5))
                        figure.scene.disable_render = False
                        label_vertices = False
                else:
                    if highlight_vertices == 0:
                        self.vertex_objs = plot_3d_points(*list(zip(*self.critical_vertices)))
                        self.all_visual_objects.append(self.vertex_objs)
                    if highlight_vertices == 1:
                        self.vertex_objs = plot_3d_points(*list(zip(*self.vertices)))
                        self.all_visual_objects.append(self.vertex_objs)
                    if highlight_vertex_distortion_pairs:
                        for (i, j) in self.vertex_distortion_pairs:
                            X = [self.vertices[i][0], self.vertices[j][0]]
                            Y = [self.vertices[i][1], self.vertices[j][1]]
                            Z = [self.vertices[i][2], self.vertices[j][2]]
                            self.all_visual_objects.append(plot_3d_points(X, Y, Z, color=get_random_color(), mode="cube", scale_factor=0.5))
            else:
                scalar_data = [1 for i in range(self.num_vertices)]
                for i in range(self.num_vertices):
                    key = None
                    if (i, ref_vertex_index) in self.distortion_ratios.keys():
                        key = (i, ref_vertex_index)
                    elif (ref_vertex_index, i) in self.distortion_ratios.keys():
                        key = (ref_vertex_index, i)
                    else:
                        print("Distortion Ratio not found! Pair: (%d, %d)" % (i, ref_vertex_index))
                        continue
                    scalar_data[i] = self.distortion_ratios[key][self.distortion_mode]
                print("Scalar data: %s" % scalar_data)
                self.vertex_objs = plot_3d_points(*list(zip(*self.vertices)), scalars=scalar_data, monochromatic=False, scale_factor=1/max(scalar_data))
                vertex = self.vertices[ref_vertex_index]
                plot_3d_points([vertex[0]], [vertex[1]], [vertex[2]], color=(1,1,1), scale_factor=0.5, mode="cube")
                mlab.colorbar(object=self.vertex_objs, title="Vertex Distortion w.r.t " + str(self.vertices[ref_vertex_index]))
            if label_vertices and figure is not None:
                figure.scene.disable_render = True
                for i, v in enumerate(self.vertices):
                    mlab.text3d(v[0], v[1]+0.25, v[2], str(i), scale=(0.15,0.15,0.15),color=(0.5,0.5,0.5))
                figure.scene.disable_render = False
        # fused = tvtk.AppendPolyData()
        # i = 0
        # for obj in self.all_visual_objects:
        #     actor = obj.actor.actors[0]
        #     polydata = tvtk.to_vtk(actor.mapper.input)
        #     fused.add_input_data(polydata)
        # fused.update()
        # write_data(fused.get_output_data_object(0), '/home/sava/output.vtk')

W = np.array([0,0,1])  # +z
A = np.array([-1,0,0]) # -x
S = np.array([0,0,-1]) # -z
D = np.array([1,0,0])  # +x
Q = np.array([0,1,0])  # +y
E = np.array([0,-1,0]) # -y

def construct_knot(directions, distortion_mode, start=(0,0,0), unit_length_sticks=True, div = 1):
    origin = np.array(start)
    vertices = [origin]
    for d in directions:
        if unit_length_sticks:
            n = int(max(np.absolute(d))) * div
            d_unit = d / n
            for i in range(n):
                vertices.append(vertices[-1] + d_unit)
        else:
            vertices.append(vertices[-1] + d)
    last_vec = vertices[0] - vertices[-1]
    n = int(max(np.absolute(last_vec))) * div
    d_unit = last_vec / n
    for i in range(n-1):
        vertices.append(vertices[-1] + d_unit)
    # if temp_flag:
    # vertices = list(np.array(vertices)/div)
    print(distortion_mode)
    if distortion_mode in ("euclidean", "taxicab"):
        print("Hello")
        return StickKnot(vertices, analyse_distortion=True, distortion_mode=distortion_mode)
    else:
        print("what the hell")
        return StickKnot(vertices)
