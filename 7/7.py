import sys
import numpy as np

def calculate_fuel(steps):
    return (steps * (steps + 1)) / 2

with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

positions = np.asarray([int(val) for val in input.split(',')])

target_positions = []
fuels = []
fuel_totals = []
for target_position in range(min(positions), max(positions)):
# target_position = np.median(calculate_fuel(positions))
    steps = np.abs(positions - target_position)

    fuel = calculate_fuel(steps)

    target_positions.append(target_position)
    fuels.append(fuel)
    fuel_totals.append(np.sum(fuel))


least_fuel_index = np.argmin(np.asarray(fuel_totals))
print(target_positions[least_fuel_index])
print(fuels[least_fuel_index])
print(int(fuel_totals[least_fuel_index]))