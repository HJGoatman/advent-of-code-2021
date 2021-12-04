import sys
import numpy as np
from scipy.stats import mode


def binary_to_decimal(binary_list):
    return int("".join(binary_list), 2)


def most_common(input):
    return mode(input, axis=0)


def least_common(input):
    most_common_values, count = most_common(input)

    least_common_values = [
        str(int(bool_val))
        for bool_val in ~(most_common_values[0].astype(int).astype(bool))
    ]
    return [least_common_values], [input.shape[0] - count[0]]


with open(sys.argv[1], "r") as input_file:
    input = [line for line in input_file.read().split("\n") if line != ""]

input = np.asarray([list(row) for row in input])

gamma_rate = binary_to_decimal(most_common(input)[0][0])
# epsilon_rate = [not bool(int(value)) for value in most_common]
epsilon_rate = binary_to_decimal(least_common(input)[0][0])

power_consumption = gamma_rate * epsilon_rate

print("Gamma Rate:", gamma_rate)
print("Epsilon Rate:", epsilon_rate)
print("Power Consumption:", power_consumption)


def get_rating(input, mode_function, eq_val):
    rating = input.copy()
    for i in range(input.shape[1]):
        if rating.shape[0] == 1:
            break

        mode_output = mode_function(rating)
        common = mode_output[0][0]

        if mode_output[1][0][i] == rating.shape[0] / 2:
            target_val = eq_val
        else:
            target_val = common[i]

        if rating.shape[0] == 1:
            break

        rating = rating[rating[:, i] == target_val]

    return rating[0]


print()
oxygen_generator_rating = binary_to_decimal(get_rating(input, most_common, "1"))
co2_scrubber_rating = binary_to_decimal(get_rating(input, least_common, "0"))
print("Oxygen Generator Rating:", oxygen_generator_rating)
print("CO2 Scrubber Rating:", co2_scrubber_rating)
print("Life Support Rating:", oxygen_generator_rating * co2_scrubber_rating)
