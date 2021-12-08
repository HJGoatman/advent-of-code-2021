import sys
from collections import Counter

with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

values = [new_line.split(' | ') for new_line in input.split("\n") if new_line != '']
values = [(input_str.split(), output_str.split() )for input_str, output_str in values]

number_unique = 0
for input_values, output_values in values:
    input_counts = Counter(list(map(len, input_values)))

    unique_lengths = [key for key in input_counts if input_counts.get(key) == 1]

    number_unique = number_unique + len(filter(lambda val_len: val_len in unique_lengths, map(len, output_values)))

print(number_unique)