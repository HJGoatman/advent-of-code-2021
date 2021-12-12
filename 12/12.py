import sys
import numpy as np
from functools import reduce
from itertools import product, groupby


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


def _find_paths(adjacency_list, start, end, visited):
    if start == end:
        return visited + [end]

    paths = [
        _find_paths(adjacency_list, connected, end, visited + [start])
        for connected in adjacency_list[start]
        if (connected not in visited) or connected[0].isupper()
    ]

    return reduce(list.__add__, paths, [])


def find_paths(adjacency_list, start, end, visited):
    paths = _find_paths(adjacency_list, start, end, visited)
    ends = [i for i in range(len(paths)) if paths[i] == "end"]
    starts = [i for i in range(len(paths)) if paths[i] == "start"]

    return [paths[starts[i] : ends[i]] + ["end"] for i in range(len(starts))]


# print(len(find_paths(adjacency_list, "start", "end", [])))

# Idea: Add a second vertex to 1 small cave, run get paths, rename the vertex back. Convert to Set.
# print(adjacency_list)
caves = adjacency_list.keys()
small_caves = [
    cave for cave in caves if (cave not in ["start", "end"]) and cave[0].islower()
]

paths = []

for small_cave in small_caves:
    new_adjacency_list = adjacency_list.copy()

    fake_cave = small_cave + "2"

    new_adjacency_list[fake_cave] = adjacency_list[small_cave]
    for key, values in new_adjacency_list.items():
        if small_cave in values:
            new_adjacency_list[key] = values + [fake_cave]

    cave_paths = find_paths(new_adjacency_list, "start", "end", [])

    # Rename fake cave backs
    cave_paths = [
        [small_cave if vertex == fake_cave else vertex for vertex in path]
        for path in cave_paths
    ]

    paths = paths + cave_paths


paths.sort()
paths = list(paths for paths, _ in groupby(paths))

print(len(paths))
