from dataclasses import dataclass
from functools import reduce


@dataclass
class Beacon:
    x: int
    y: int
    z: int


@dataclass
class ScannerReport:
    id: int
    beacons: list[Beacon]


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


def find_overlapping_beacons(
    scanner_report_1: ScannerReport,
    scanner_report_2: ScannerReport,
    min_overlapping_beacons,
) -> list[Beacon]:

    matches = []

    for accessor in [
        lambda beacon: beacon.x,
        lambda beacon: beacon.y,
        lambda beacon: beacon.z,
    ]:

        displacements_1, displacements_2 = (
            get_beacon_displacements(scanner_report.beacons, accessor)
            for scanner_report in [scanner_report_1, scanner_report_2]
        )

        common_distances = set(displacements_1).intersection(set(displacements_2))

        common_displacements_1, common_displacements_2 = (
            [
                (i, dist)
                for i, dist in enumerate(displacements)
                if dist in common_distances
            ]
            for displacements in [displacements_1, displacements_2]
        )

        matches.append(
            {
                i: [j for j, v2 in common_displacements_2 if v1 == v2]
                for i, v1 in common_displacements_1
            }
        )

    edge_match = {
        i: reduce(
            lambda list1, list2: set(list1).intersection(list2),
            [match[i] for match in matches],
        )
        for i in matches[0]
    }
    if all([len(s) == 1 for _, s in edge_match.items()]):
        edge_map = {k: next(iter(v)) for k, v in edge_match.items()}
        edges_1 = [
            (i, j)
            for j in range(len(edge_match))
            for i in range(len(edge_match))
            if i != j and i < j
        ]
        edges_2 = [edges_1[edge_map[i]] for i, _ in enumerate(edges_1)]

        node_matches = reduce(
            combine_dicts,
            [{i: {k, l}, j: {k, l}} for (i, j), (k, l) in zip(edges_1, edges_2)],
        )

        if all([len(s) == 1 for _, s in node_matches.items()]):
            node_map = {k: next(iter(v)) for k, v in node_matches.items()}
            if len(node_map) >= min_overlapping_beacons:
                return node_map
            else:
                return {}
