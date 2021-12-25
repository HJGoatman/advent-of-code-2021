from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from itertools import permutations, combinations, product
from os import access
from queue import PriorityQueue
import numpy as np
import sys


@dataclass(frozen=True, eq=True)
class Beacon:
    x: int
    y: int
    z: int


@dataclass(frozen=True, eq=True)
class Scanner:
    x: int
    y: int
    z: int


@dataclass
class ScannerReport:
    id: int
    beacons: list[Beacon]

    def __eq__(self, __o: object) -> bool:
        return (self.id == __o.id) and (set(self.beacons) == set(__o.beacons))


@dataclass(frozen=True, eq=True)
class Edge:
    id: int
    start: Beacon
    end: Beacon


def read_beacon(beacon: str) -> Beacon:
    coordinates = beacon.split(",")
    coordinates = coordinates + [0 for _ in range(3 - len(coordinates))]
    return Beacon(*map(int, coordinates))


def read_scanner_report(scanner_report: str) -> ScannerReport:
    lines = [line for line in scanner_report.split("\n") if line != ""]
    return ScannerReport(
        id=int(lines[0][12:-4]), beacons=list(map(read_beacon, lines[1:]))
    )


def read_scanner_reports(scanner_reports: str) -> list[ScannerReport]:
    return list(map(read_scanner_report, scanner_reports.split("\n\n")))


def get_beacon_displacements(beacons: list[Beacon], accessor):
    values = [accessor(beacon) for beacon in beacons]
    return [
        abs(value_1 - value_2)
        for j, value_1 in enumerate(values)
        for i, value_2 in enumerate(values)
        if i != j and i < j
    ]


def combine_dicts(dict1, dict2):
    return {
        **{
            k: (v.intersection(dict2[k]) if k in dict2 else v) for k, v in dict1.items()
        },
        **{k: v for k, v in dict2.items() if k not in dict1},
    }


def have_same_distances(pair):
    a, b = pair

    return (
        (abs(a.start.x - a.end.x) == abs(b.start.x - b.end.x))
        and (abs(a.start.y - a.end.y) == abs(b.start.y - b.end.y))
        and (abs(a.start.z - a.end.z) == abs(b.start.z - b.end.z))
    )


def find_overlapping_beacons(
    scanner_report_1: ScannerReport,
    scanner_report_2: ScannerReport,
    min_overlapping_beacons: int,
):
    for accessor, rotation, alt_scanner_report_2 in get_rotations(scanner_report_2):
        edge_pairs = product(
            *[
                [
                    Edge(id=i, start=start, end=end)
                    for i, (start, end) in enumerate(combinations(report.beacons, 2))
                ]
                for report in [scanner_report_1, alt_scanner_report_2]
            ]
        )

        matching_edges = list(
            filter(
                have_same_distances,
                edge_pairs,
            )
        )

        beacon_mapping = {}
        for edge1, edge2 in matching_edges:
            x1_displacement = edge1.start.x - edge1.end.x
            y1_displacement = edge1.start.y - edge1.end.y
            z1_displacement = edge1.start.z - edge1.end.z

            x2_displacement = edge2.start.x - edge2.end.x
            y2_displacement = edge2.start.y - edge2.end.y
            z2_displacement = edge2.start.z - edge2.end.z

            if (
                x1_displacement == x2_displacement
                and y1_displacement == y2_displacement
                and z1_displacement == z2_displacement
            ):
                beacon_mapping[edge1.start] = edge2.start
                beacon_mapping[edge2.start] = edge1.start
                beacon_mapping[edge1.end] = edge2.end
                beacon_mapping[edge2.end] = edge1.end
            else:
                beacon_mapping[edge1.end] = edge2.start
                beacon_mapping[edge2.start] = edge1.end
                beacon_mapping[edge1.start] = edge2.end
                beacon_mapping[edge2.end] = edge1.start

        displacements = [
            (beacon1.x - beacon2.x, beacon1.y - beacon2.y, beacon1.z - beacon2.z)
            for beacon1, beacon2 in beacon_mapping.items()
            if beacon1 in scanner_report_1.beacons
        ]

        if (len(set(displacements)) != 1) or (
            (len(beacon_mapping) / 2) < min_overlapping_beacons
        ):
            continue
        else:
            break

    if (len(beacon_mapping) / 2) >= min_overlapping_beacons:
        return accessor, rotation, displacements[0], beacon_mapping
    else:
        return None


def vector_less_than(vec1, vec2):
    return (vec1[0] < vec2[0]) and (vec1[1] < vec2[1]) and (vec1[2] < vec2[2])


def vector_add(vec1, vec2):
    return (vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2])


# Python implementation to find the
# shortest path in the graph using
# dictionaries

# Function to find the shortest
# path between two nodes of a graph
def BFS_SP(graph, start, goal):
    explored = []

    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]

    # If the desired node is
    # reached
    if start == goal:
        # print("Same Node")
        return

    # Loop to traverse the graph
    # with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]

        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]

            # Loop to iterate over the
            # neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                # Condition to check if the
                # neighbour node is the goal
                if neighbour == goal:
                    # print("Shortest path = ", *new_path)
                    return new_path
            explored.append(node)

    # Condition when the nodes
    # are not connected
    # print("So sorry, but a connecting" "path doesn't exist :(")
    return


def get_all_distances(edges):
    adjacency_list = {node1: [] for node1, _ in edges.keys()}
    for node1, node2 in edges.keys():
        adjacency_list[node1] = adjacency_list[node1] + [node2]

    return {
        node: BFS_SP(adjacency_list, 0, node) for node, _ in edges.keys() if node != 0
    }


def transform_beacons(beacons, accessor, rotation, displacement):
    accessor_mapping = {
        "X": lambda beacon: beacon.x,
        "Y": lambda beacon: beacon.y,
        "Z": lambda beacon: beacon.z,
    }

    beacons = [
        Beacon(
            accessor_mapping[accessor[0]](beacon),
            accessor_mapping[accessor[1]](beacon),
            accessor_mapping[accessor[2]](beacon),
        )
        for beacon in beacons
    ]

    beacons = [
        Beacon(
            beacon.x * rotation[0],
            beacon.y * rotation[1],
            beacon.z * rotation[2],
        )
        for beacon in beacons
    ]

    beacons = [
        Beacon(
            beacon.x + displacement[0],
            beacon.y + displacement[1],
            beacon.z + displacement[2],
        )
        for beacon in beacons
    ]

    return beacons


def create_map(scanner_reports: list[ScannerReport], min_overlapping_beacons):
    scanners = {}
    for scanner_report_1, scanner_report_2 in permutations(scanner_reports, 2):
        result = find_overlapping_beacons(
            scanner_report_1, scanner_report_2, min_overlapping_beacons
        )

        if not result:
            continue

        accessor, rotation, displacement, beacon_mapping = result

        scanners[(scanner_report_1.id, scanner_report_2.id)] = (
            accessor,
            rotation,
            displacement,
        )

    scanners = {
        **{
            (edge[0], edge[1]): scanners[(edge[1], edge[0])]
            for edge, _ in scanners.items()
        },
        **{
            (edge[1], edge[0]): scanners[(edge[0], edge[1])]
            for edge, _ in scanners.items()
        },
    }

    # print(scanners)
    paths = get_all_distances(scanners)
    # print()
    # print(paths)
    # print()
    # print(scanners)
    all_beacons = [scanner_reports[0].beacons]
    scanner_positions = [(0, 0, 0)]
    for i in range(1, len(scanner_reports)):
        path = list(reversed(paths[i]))
        beacons = scanner_reports[i].beacons
        scanner_position = Beacon(0, 0, 0)
        for j in range(len(path) - 1):
            accessor, rotation, displacement = scanners[(path[j], path[j + 1])]
            beacons = transform_beacons(beacons, accessor, rotation, displacement)
            scanner_position = transform_beacons(
                [scanner_position], accessor, rotation, displacement
            )[0]

        scanner_positions.append(
            (scanner_position.x, scanner_position.y, scanner_position.z)
        )
        all_beacons.append(beacons)

    return scanner_positions, set(reduce(list.__add__, all_beacons))


def _get_rotation(
    scanner_report: ScannerReport, x_mul: int, y_mul: int, z_mul: int
) -> ScannerReport:

    beacons = [
        Beacon(beacon.x * x_mul, beacon.y * y_mul, beacon.z * z_mul)
        for beacon in scanner_report.beacons
    ]

    return (x_mul, y_mul, z_mul), ScannerReport(scanner_report.id, beacons)


def _swap_columns(scanner_report: ScannerReport) -> list[ScannerReport]:
    accessors = [
        ("X", lambda beacon: beacon.x),
        ("Y", lambda beacon: beacon.y),
        ("Z", lambda beacon: beacon.z),
    ]

    reports = []

    for accessor in permutations(accessors, 3):
        reports.append(
            (
                tuple([label for label, _ in accessor]),
                ScannerReport(
                    scanner_report.id,
                    [
                        Beacon(
                            *map(
                                lambda ac: ac(beacon),
                                [access[1] for access in accessor],
                            )
                        )
                        for beacon in scanner_report.beacons
                    ],
                ),
            )
        )

    return reports


def get_rotations(scanner_report):
    potential_reports = _swap_columns(scanner_report)

    rotations = [
        (
            [report for i, (report) in enumerate(potential_reports) if i in [0, 3, 4]],
            [(1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)],
        ),
        (
            [report for i, (report) in enumerate(potential_reports) if i in [1, 2, 5]],
            [(1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1)],
        ),
    ]

    reports = [
        [
            (accessor, *_get_rotation(report, x_mul, y_mul, z_mul))
            for x_mul, y_mul, z_mul in rotation_set
            for accessor, report in report_subset
        ]
        for report_subset, rotation_set in rotations
    ]

    return reports[0] + reports[1]


def get_manhatten_distance(beacon1, beacon2):
    return (
        abs(beacon1[0] - beacon2[0])
        + abs(beacon1[1] - beacon2[1])
        + abs(beacon1[2] - beacon2[2])
    )


def get_maximum_manhatten_distance(scanners):
    return max(map(lambda x: get_manhatten_distance(*x), combinations(scanners, 2)))


if __name__ == "__main__":
    with open(sys.argv[1], "r") as input_file:
        input = input_file.read()

    scanner_reports = read_scanner_reports(input)

    scanners, beacons = create_map(scanner_reports, 12)

    print(len(beacons))

    print(get_maximum_manhatten_distance(scanners))
