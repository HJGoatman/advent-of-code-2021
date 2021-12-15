import sys
import numpy as np


def reconstruct_path(came_from, current_node):
    total_path = [current_node]
    while current_node in came_from.keys():
        current_node = came_from[current_node]
        total_path = [current_node] + total_path
    return total_path


def is_in_bounds(neighbour):
    return (
        neighbour[0] >= 0
        and neighbour[1] >= 0
        and neighbour[0] < risk_map.shape[0]
        and neighbour[1] < risk_map.shape[1]
    )


def d(current_node, neighbour):
    return risk_map[neighbour]


def get_neighbours(node):
    DOWN = (0, 1)
    UP = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    return [
        neighbour
        for neighbour in [
            (node[0] + direction[0], node[1] + direction[1])
            for direction in [DOWN, UP, LEFT, RIGHT]
        ]
        if is_in_bounds(neighbour)
    ]


def a_star(start, goal, h):
    open_set = {start}

    came_from = {}

    g_score = {
        (x, y): np.inf
        for x in range(risk_map.shape[0])
        for y in range(risk_map.shape[1])
    }
    g_score[start] = 0

    f_score = {
        (x, y): np.inf
        for x in range(risk_map.shape[0])
        for y in range(risk_map.shape[1])
    }
    f_score[start] = h(start)

    while len(open_set) != 0:
        open_f_scores = {key: f_score[key] for key in f_score if key in open_set}

        min_open_f_score = min(open_f_scores.values())
        current_node = [
            key for key in open_f_scores if open_f_scores[key] == min_open_f_score
        ][0]

        if current_node == goal:
            return reconstruct_path(came_from, current_node)

        open_set.remove(current_node)
        for neighbour in get_neighbours(current_node):
            tentative_g_score = g_score[current_node] + d(current_node, neighbour)
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current_node
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + h(neighbour)
                if neighbour not in open_set:
                    open_set.add(neighbour)

    return "Failure"


with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

risk_map = np.asarray(
    [list(map(int, list(line))) for line in input.split("\n") if line != ""]
)

size_x = risk_map.shape[0]
size_y = risk_map.shape[1]

large_map = np.zeros(np.asarray(risk_map.shape) * 5)

for i in range(5):
    for j in range(5):
        large_map[
            i * size_x : i * size_x + size_x, j * size_y : j * size_y + size_y
        ] = (((risk_map + i + j) - 1) % 9) + 1


risk_map = large_map.astype(int)

print(risk_map)


TARGET_X = risk_map.shape[0] - 1
TARGET_Y = risk_map.shape[1] - 1

path = a_star(
    (0, 0),
    (TARGET_X, TARGET_Y),
    lambda node: abs(node[0] - TARGET_X) + abs(node[1] - TARGET_Y),
)

# print(path)

print(sum(risk_map[[x for x, _ in path[1:]], [y for _, y in path[1:]]]))
