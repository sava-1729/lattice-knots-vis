from utils import *

class Stick:
    def __init__(self, start, end, index=0):
        assert_is_3d_point(start)
        assert_is_3d_point(end)
        self.start = np.array(start)
        self.end = np.array(end)
        self.id = index
        assert any(self.start != self.end)
        self.X = np.linspace(self.start[0], self.end[0], 3)
        self.Y = np.linspace(self.start[1], self.end[1], 3)
        self.Z = np.linspace(self.start[2], self.end[2], 3)
        self.vector = self.end - self.start
        self.length = np.sqrt(sum((self.end - self.start) ** 2))

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
        cross = np.cross(self.vector, other_stick.vector)
        return all(cross == 0)

    def is_point_on_stick(self, point):
        assert_is_3d_point(point)
        if all(self.start == point):
            return True
        on_line = self.is_parallel_to(Stick(self.start, point))
        x_in_range = point[0] <= max(self.X) and point[0] >= min(self.X)
        y_in_range = point[1] <= max(self.Y) and point[1] >= min(self.Y)
        z_in_range = point[2] <= max(self.Z) and point[2] >= min(self.Z)
        return (x_in_range and y_in_range and z_in_range and on_line)

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
                return ((self.is_point_on_stick(other_stick.start) or self.is_point_on_stick(other_stick.end)), debug)
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
