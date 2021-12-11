import sys
import time
import numpy as np
from scipy.ndimage.interpolation import shift
from functools import reduce
import os


def delete_multiple_lines(n=1):
    """Delete the last line in the STDOUT."""
    for _ in range(n):
        sys.stdout.write("\x1b[1A")  # cursor up one line
        sys.stdout.write("\x1b[2K")  # delete the last line


with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

octopuses = np.asarray(
    [list(map(int, list(line))) for line in input.split("\n") if line != ""]
)

print(octopuses)
number_of_flashes = 0
for step in range(100):
    # Increment octopuses by 1
    octopuses = octopuses + 1

    has_flashed = np.zeros_like(octopuses).astype(bool)
    new_flashes = octopuses > 9
    # Octopuses greater than 9 flash.

    while new_flashes.any():
        new_flashes = (octopuses > 9) & ~has_flashed

        energy_level_increase = reduce(
            np.add,
            [
                shift(new_flashes.astype(int), (i, j), cval=False)
                for i in [-1, 0, 1]
                for j in [-1, 0, 1]
            ],
        )

        octopuses = octopuses + energy_level_increase

        has_flashed = has_flashed | new_flashes

    # Set flashed octopuses to zero
    octopuses[has_flashed] = 0
    number_of_flashes = number_of_flashes + np.sum(has_flashed)

    delete_multiple_lines(10)
    print(octopuses, flush=True)
    time.sleep(0.1)

print(number_of_flashes)
