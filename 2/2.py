import sys

with open(sys.argv[1], 'r') as input_file:
    course = input_file.read().split('\n')

course = [(x.split(' ')[0], x.split(' ')[1]) for x in course if x != '']

horizontal_position = 0
depth = 0

for direction, distance in course:

    distance = int(distance)

    if direction == 'forward':
        horizontal_position = horizontal_position + distance
    elif direction == 'down':
        depth = depth + distance
    elif direction == "up":
        depth = depth - distance

print(horizontal_position, depth, horizontal_position * depth)