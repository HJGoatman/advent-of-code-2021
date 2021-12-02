import sys

with open(sys.argv[1], 'r') as input_file:
    course = input_file.read().split('\n')

course = [(x.split(' ')[0], x.split(' ')[1]) for x in course if x != '']

horizontal_position = 0
depth = 0
aim = 0

for direction, distance in course:

    distance = int(distance)

    if direction == 'forward':
        horizontal_position = horizontal_position + distance
        depth = depth + aim * distance
    elif direction == 'down':
        aim = aim + distance
    elif direction == "up":
        aim = aim - distance

print(horizontal_position, depth, horizontal_position * depth)