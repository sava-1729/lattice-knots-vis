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
        self.vertex_distortion = [[1 for i in range(self.num_sticks)] for i in range(self.num_sticks)]
        for i in range(len(vertices)):
            for j in range(0, i):
                distance_along_knot_forward = sum(sticks[k].length for k in range(j+1, i+1))
                distance_along_knot_backward = sum(sticks[k].length for k in range(len(sticks))) - distance_along_knot_forward
                distance_along_knot = min(distance_along_knot_forward, distance_along_knot_backward)
                distance_taxicab = sum(np.absolute(self.vertices[j] - self.vertices[i]))
                self.vertex_distortion[i][j] = distance_along_knot / distance_taxicab
                self.vertex_distortion[j][i] = distance_along_knot / distance_taxicab

    def plot(self, bgcolor=(1,1,1), highlight_vertices=True, monochromatic_sticks=False, vertex_distortion_index=-1):
        create_new_figure(bgcolor=bgcolor)
        self.stick_objs = [None for i in range(len(self.sticks))]
        for i, stick in enumerate(self.sticks):
            if monochromatic_sticks:
                self.stick_objs[i] = stick.plot(fix_color=True)
            else:
                self.stick_objs[i] = stick.plot()
        if highlight_vertices:
            if vertex_distortion_index == -1:
                self.vertex_objs = plot_3d_points(*list(zip(*self.vertices)))
            else:
                scalar_data = self.vertex_distortion[vertex_distortion_index]
                self.vertex_objs = plot_3d_points(*list(zip(*self.vertices)), scalars=scalar_data, monochromatic=False, scale_factor=1/max(scalar_data))
                vertex = self.vertices[vertex_distortion_index]
                plot_3d_points([vertex[0]], [vertex[1]], [vertex[2]], color=(1,1,1), scale_factor=0.5, mode="cube")
                mlab.colorbar(object=self.vertex_objs, title="Vertex Distortion w.r.t " + str(self.vertices[vertex_distortion_index]))

def construct_knot(directions):
    origin = np.array([0,0,0])
    vertices = [origin]
    for d in directions:
        vertices.append(vertices[-1] + d)
    return StickKnot(vertices)
