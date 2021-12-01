import sys

with open(sys.argv[1], 'r') as input_file:
    data = [int(d) for d in input_file.read().split('\n') if d != '']

data = [sum(data[i: i+3]) for i in range(len(data) - 2)]

total_increasing = 0

for i in range(0, len(data) - 1):
    if (data[i + 1] > data[i]):
        total_increasing = total_increasing + 1

print(total_increasing)