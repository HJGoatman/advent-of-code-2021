with open('input.txt', 'r') as input_file:
    data = [int(d) for d in input_file.read().split('\n') if d != '']

total_increasing = 0

for i in range(0, len(data) - 1):
    if (data[i + 1] >= data[i]):
        total_increasing = total_increasing + 1

print(total_increasing)