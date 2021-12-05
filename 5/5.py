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
    return (
        (ix >= line.x1 and ix <= line.x2) and (iy >= line.y1 and iy <= line.y2)
    ) or ((ix <= line.x1 and ix >= line.x2) and (iy <= line.y1 and iy >= line.y2))


with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

lines = [Line.from_str(line) for line in input.split("\n") if line != ""]

max_x = max([max(line.x1, line.x2) for line in lines])
max_y = max([max(line.y1, line.y2) for line in lines])

lines = list(filter(lambda line: line.x1 == line.x2 or line.y1 == line.y2, lines))

diagram = np.zeros((max_x + 1, max_y + 1))
for iy, ix in np.ndindex(diagram.shape):
    for line in lines:
        if is_point_on_line(iy, ix, line):
            diagram[iy, ix] = diagram[iy, ix] + 1

print(diagram)

print(np.sum(diagram >= 2))