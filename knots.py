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
                    exit()
            k = 1 if (i == (len(sticks)-1)) else 0
            for j in range(k, i-1):
                intersects, debug = sticks[i].is_intersecting(sticks[j])
                if intersects:
                    print("Sticks %d and %d are intersecting:" % (j, i))
                    print("DEBUG DATA:")
                    sticks[j].identify()
                    sticks[i].identify()
                    print(debug)
                    exit()
        self.sticks = sticks
        self.vertices = vertices
        self.length = len(vertices)

    def plot(self, highlight_vertices=True):
        create_new_figure(bgcolor=(1,1,1))
        self.stick_figures = [None for i in range(len(self.sticks))]
        for i, stick in enumerate(self.sticks):
            self.stick_figures[i] = stick.plot()
        if highlight_vertices:
            self.vertex_figures = plot_3d_points(*list(zip(*self.vertices)))

def construct_knot(directions):
    origin = np.array([0,0,0])
    vertices = [origin]
    for d in directions:
        vertices.append(vertices[-1] + d)
    return StickKnot(vertices)
