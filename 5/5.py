import sys
import numpy as np


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return str([(self.x1, self.y1), (self.x2, self.y2)])

    @staticmethod
    def from_str(line_str):
        line_data = [
            (int(coord.split(",")[0]), int(coord.split(",")[1]))
            for coord in line_str.split(" -> ")
        ]

        return Line(line_data[0][0], line_data[0][1], line_data[1][0], line_data[1][1])

    __repr__ = __str__


def is_point_on_line(iy, ix, line):
    dy = line.y2 - line.y1
    dx = line.x2 - line.x1

    within_bounds = (min(line.x1, line.x2) <= ix <= max(line.x1, line.x2)) and (
        min(line.y1, line.y2) <= iy <= max(line.y1, line.y2)
    )

    if dy == 0 or dx == 0:
        return within_bounds

    gradient = dy / dx
    intercept1 = line.y1 - gradient * line.x1

    return within_bounds and iy == (gradient * ix + intercept1)


with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

lines = [Line.from_str(line) for line in input.split("\n") if line != ""]

max_x = max([max(line.x1, line.x2) for line in lines])
max_y = max([max(line.y1, line.y2) for line in lines])

# This is a very slow way of doing this.
diagram = np.zeros((max_x + 1, max_y + 1))
for iy, ix in np.ndindex(diagram.shape):
    for line in lines:
        if is_point_on_line(iy, ix, line):
            diagram[iy, ix] = diagram[iy, ix] + 1

print(diagram)

print(np.sum(diagram >= 2))
