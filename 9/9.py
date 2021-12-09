import sys
import numpy as np
from scipy.ndimage.interpolation import shift
from functools import reduce

with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

data = np.asarray([list(map(int, list(line))) for line in input.split('\n') if line != ''])

DOWN = (1, 0)
UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)


is_low_point = reduce(lambda x, y: x & y, [(data - shift(data, direction, cval=np.inf)) < 0 for direction in [UP, DOWN, LEFT, RIGHT]])
risk_levels = np.sum(data[is_low_point] + 1 )
print(risk_levels)