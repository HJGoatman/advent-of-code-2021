import sys
import numpy as np

with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

positions = np.asarray([int(val) for val in input.split(',')])

target_position = np.median(positions)
fuel_used = int(np.sum(np.abs(positions - target_position)))

print(fuel_used)
