from utils import *

class Stick:
    def __init__(self, start, end, index=0):
        are_3d_points(start, end)
        assert not all(start == end), ("Index %d, Start %s, End %s" % (index, start, end))
        self.start = start.copy()
        self.end = end.copy()
        self.id = index
        self.X = np.linspace(self.start[0], self.end[0], 3)
        self.Y = np.linspace(self.start[1], self.end[1], 3)
        self.Z = np.linspace(self.start[2], self.end[2], 3)
        self.vector = self.end - self.start
        self.length = np.sqrt(sum((self.end - self.start) ** 2))
        self.unit_vector = self.vector / self.length

    def identify(self):
        print("Stick %d: %s, %s" % (self.id, self.start, self.end))

    def plot(self, color=None, mode="line", thickness=5):
        if color is None:
            return plot_3d_line(self.X, self.Y, self.Z, label=self.id, mode=mode, thickness=thickness)
        else:
            return plot_3d_line(self.X, self.Y, self.Z, color=color, mode=mode, thickness=thickness)

    def shares_plane_with(self, other_stick):
        assert isinstance(other_stick, Stick)
        normal_abc = np.cross(self.vector, other_stick.start - self.start)
        vector_ad = other_stick.end - self.start
        return np.dot(normal_abc, vector_ad) == 0

    def is_parallel_to(self, other_stick):
        assert isinstance(other_stick, Stick)
        return are_vectors_parallel(self.vector, other_stick.vector)

    def contains(self, point):
        assert_is_3d_point(point)
        if all(self.start == point):
            return True
        on_line = self.is_parallel_to(Stick(self.start, point))
        x_in_range = point[0] <= max(self.X) and point[0] >= min(self.X)
        y_in_range = point[1] <= max(self.Y) and point[1] >= min(self.Y)
        z_in_range = point[2] <= max(self.Z) and point[2] >= min(self.Z)
        return (x_in_range and y_in_range and z_in_range and on_line)

    def intersects(self, other_stick):
        """
        self.stick: (a1+t*v1, a2+t*v2, a3+t*v3)
        other_stick: (b1+s*w1, b2+s*w2, b3+s*w3)
        t*v1 - s*w1 = b1 - a1, t*v2 - s*w2 = b2 - a2, t*v3 - s*w3 = b3 - a3

        If det([[v1, -w1], [v2, -w2]]) != 0, solve:
        | v1  -w1 | | t |   | b1-a1 |
        | v2  -w2 | | s | = | b2-a2 |
        and verify t*v3 - s*w3 = b3 - a3

        If det([[v1, -w1], [v3, -w3]]) != 0, solve:
        | v1  -w1 | | t |   | b1-a1 |
        | v3  -w3 | | s | = | b3-a3 |
        and verify t*v2 - s*w2 = b2 - a2

        If det([[v3, -w3], [v2, -w2]]) != 0, solve:
        | v3  -w3 | | t |   | b3-a3 |
        | v2  -w2 | | s | = | b2-a2 |
        and verify t*v1 - s*w1 = b1 - a1
        """
        a1, a2, a3 = self.start
        v1, v2, v3 = self.vector
        b1, b2, b3 = other_stick.start
        w1, w2, w3 = other_stick.vector
        if not isclose(np.linalg.det([[v1, -w1], [v2, -w2]]), 0, rel_tol=0, abs_tol=ABS_TOL):
            t, s = np.linalg.solve([[v1, -w1], [v2, -w2]], [b1-a1, b2-a2])
            lines_intersect = isclose(t*v3 - s*w3, b3 - a3, rel_tol=0, abs_tol=ABS_TOL)
            if lines_intersect:
                print("Case 1")
                return (0 <= t) and (t <= 1) and (0 <= s) and (s <= 1)
            else:
                print("Case 2")
                return False
        elif not isclose(np.linalg.det([[v1, -w1], [v3, -w3]]), 0, rel_tol=0, abs_tol=ABS_TOL):
            t, s = np.linalg.solve([[v1, -w1], [v3, -w3]], [b1-a1, b3-a3])
            lines_intersect = isclose(t*v2 - s*w2, b2 - a2, rel_tol=0, abs_tol=ABS_TOL)
            if lines_intersect:
                print("Case 1")
                return (0 <= t) and (t <= 1) and (0 <= s) and (s <= 1)
            else:
                print("Case 2")
                return False
        elif not isclose(np.linalg.det([[v2, -w2], [v3, -w3]]), 0, rel_tol=0, abs_tol=ABS_TOL):
            t, s = np.linalg.solve([[v2, -w2], [v3, -w3]], [b2-a2, b3-a3])
            lines_intersect = isclose(t*v1 - s*w1, b1 - a1, rel_tol=0, abs_tol=ABS_TOL)
            if lines_intersect:
                print("Case 1")
                return (0 <= t) and (t <= 1) and (0 <= s) and (s <= 1)
            else:
                print("Case 2")
                return False
        else:
            other_ends_on_self = self.contains(other_stick.start) or \
                                     self.contains(other_stick.end)
            self_ends_on_others = other_stick.contains(self.start) or \
                                    other_stick.contains(self.end)
            if (other_ends_on_self or self_ends_on_others):
                print("Self: %s -> %s" % (self.start, self.end))
                print("Other: %s -> %s" % (other_stick.start, other_stick.end))  
            print("Case 5")
            return other_ends_on_self or self_ends_on_others


    def is_intersecting(self, other_stick):
        debug = ""
        stick_ids = "\nSticks " + str(self.id) + " " + str(other_stick.id)
        self_stick_id = "Stick " + str(self.id)
        other_stick_id = "Stick " + str(other_stick.id)
        if all(other_stick.start == self.start) or all(other_stick.start == self.end) or all(other_stick.end == self.start) or all(other_stick.end == self.end):
            debug += stick_ids + " share an endpoint"
            return (True, debug)
        if not self.shares_plane_with(other_stick):
            debug += stick_ids + " do not share a plane"
            return (False, debug)
        else:
            debug += stick_ids + " share a plane"
        if self.is_parallel_to(other_stick):
            debug += stick_ids + " are parallel"
            connector = other_stick.start - self.end
            if all(np.cross(connector, self.vector) == 0):
                debug += stick_ids + " are colinear"
                return ((self.contains(other_stick.start) or self.contains(other_stick.end)), debug)
            else:
                debug += stick_ids + " are not colinear"
                return (False, debug)
        else:
            debug += stick_ids + " are not parallel"
            connector1 = other_stick.start - self.start
            connector2 = other_stick.end - self.start
            cross1 = np.cross(self.vector, connector1)
            cross2 = np.cross(self.vector, connector2)
            dot12 = np.dot(cross1, cross2)
            if dot12 <= 0:
                debug += "\n" + other_stick_id + " start and end are on opposite sides of " + self_stick_id
                connector3 = self.start - other_stick.start
                connector4 = self.end - other_stick.start
                cross3 = np.cross(other_stick.vector, connector3)
                cross4 = np.cross(other_stick.vector, connector4)
                dot34 = np.dot(cross3, cross4)
                if dot34 <= 0:
                    debug += "\n" + self_stick_id + " start and end are on opposite sides of " + other_stick_id
                    if dot12 == 0 and dot34 == 0:
                        debug += "\nStrange case."
                        debug += "\nstick1: %s -> %s" % str((self.start, self.end))
                        debug += "\nstick2: %s -> %s" % str((other_stick.start, other_stick.end))
                    return (True, debug)
                else:
                    debug += "\n " + self_stick_id + " start and end are on same side of " + other_stick_id
                    return (False, debug)
            else:
                debug += "\n " + other_stick_id + " start and end are on same of " + self_stick_id
                return (False, debug)
