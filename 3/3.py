import sys
import numpy as np
from scipy.stats import mode


def binary_to_decimal(binary_list):
    return int("".join(binary_list), 2)


with open(sys.argv[1], "r") as input_file:
    input = [line for line in input_file.read().split("\n") if line != '']

input = np.asarray([list(row) for row in input])

most_common = mode(input, axis=0)[0][0]
gamma_rate = binary_to_decimal(most_common)
# epsilon_rate = [not bool(int(value)) for value in most_common]
epsilon_rate = binary_to_decimal(
    [str(int(bool_val)) for bool_val in ~(most_common.astype(int).astype(bool))]
)

power_consumption = gamma_rate * epsilon_rate

print("Gamma Rate:", gamma_rate)
print("Epsilon Rate:", epsilon_rate)
print("Power Consumption:", power_consumption)

