import sys
import numpy as np
from functools import reduce
from itertools import product


def remove_vertex(target_node, edge):
    edge_list = list(edge)
    edge_list.remove(target_node)

    return edge_list[0]


with open(sys.argv[1], "r") as input_file:
    input = input_file.read()


edges = [tuple(line.split("-")) for line in input.split("\n") if line != ""]
vertices = set(reduce(lambda edge1, edge2: edge1 + edge2, edges))

adjacency_list = {
    vertex: list(
        map(
            lambda edge: remove_vertex(vertex, edge),
            filter(lambda edge: vertex in edge, edges),
        )
    )
    for vertex in vertices
}


def expand_path(compressed):
    return list(map(lambda x: compressed[0] + x, compressed[1:]))


def find_paths(adjacency_list, start, end, visited):
    if start == end:
        return visited + [end]

    paths = [
        find_paths(adjacency_list, connected, end, visited + [start])
        for connected in adjacency_list[start]
        if (connected not in visited) or connected[0].isupper()
    ]

    return reduce(list.__add__, paths, [])


paths = find_paths(adjacency_list, "start", "end", [])
ends = [i for i in range(len(paths)) if paths[i] == "end"]
starts = [i for i in range(len(paths)) if paths[i] == "start"]

print(len([paths[starts[i] : ends[i]] for i in range(len(starts))]))

# def flatten(list_of_lists):
#     if len(list_of_lists) == 0:
#         return list_of_lists
#     if isinstance(list_of_lists[0], list):
#         return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
#     return list_of_lists[:1] + flatten(list_of_lists[1:])


# print(flatten(paths))
# print()
# data = ["b", ["A", ["end"]], ["d"], ["end"]]


# def expand(paths):
#     print(paths)
#     if len(paths) == 1:
#         if isinstance(paths[0], str):
#             print(1)
#             expanded = [paths[0]]
#         else:
#             print(2)
#             expanded = paths[0]

#     else:
#         print(3)
#         expanded = [[paths[0]] + expand(path) for path in paths[1:]]

#     print(expanded)
#     print()
#     return expanded


# print(expand(data))
