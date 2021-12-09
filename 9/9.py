from os import pipe
import sys
import numpy as np
from scipy.ndimage.interpolation import shift
from functools import reduce

with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

data = np.asarray(
    [list(map(int, list(line))) for line in input.split("\n") if line != ""]
)

DOWN = np.asarray([1, 0])
UP = np.asarray([-1, 0])
RIGHT = np.asarray([0, 1])
LEFT = np.asarray([0, -1])


is_low_point = reduce(
    lambda x, y: x & y,
    [
        (data - shift(data, direction, cval=np.inf)) < 0
        for direction in [UP, DOWN, LEFT, RIGHT]
    ],
)
risk_levels = np.sum(data[is_low_point] + 1)

def find_basin(low_point):
    stack = []
    basin_points = []

    stack.append(low_point)
    while len(stack) != 0:
        point = stack.pop()

        if np.any(np.asarray(point) < [0, 0]) or (np.asarray(point) >= data.shape).any():
            continue

        # If stopping point
        if data[point] == 9:
            continue

        

        basin_points.append(point)

        search_values = [tuple(point + direction) for direction in [UP, DOWN, LEFT, RIGHT]]
        [stack.append(search_point) for search_point in search_values if search_point not in basin_points]

    return basin_points






low_point_coordinates = np.where(is_low_point)
low_point_coordinates = list(zip(low_point_coordinates[0], low_point_coordinates[1]))

basins = [set(find_basin(low_point)) for low_point in low_point_coordinates]
print(reduce(lambda x, y: x * y, sorted(map(len, basins))[-3:]))
