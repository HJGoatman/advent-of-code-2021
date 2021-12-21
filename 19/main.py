from dataclasses import dataclass
from functools import reduce
from itertools import permutations


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


def create_map(scanner_reports: list[ScannerReport], min_overlapping_beacons):
    the_map = set()

    beacon_map = find_overlapping_beacons(
        scanner_reports[0], scanner_reports[1], min_overlapping_beacons
    )

    matching_beacons = [
        (beacon, scanner_reports[1].beacons[beacon_map[i]])
        for i, beacon in enumerate(scanner_reports[0].beacons)
    ]

    differences = [
        (beacon1.x - beacon2.x, beacon1.y - beacon2.y, beacon1.z - beacon2.z)
        for beacon1, beacon2 in matching_beacons
    ]

    if len(set(differences)) != 1:
        return {}

    x_diff, y_diff, z_diff = differences[0]
    the_map.add(Scanner(0, 0, 0))

    for beacon in scanner_reports[0].beacons:
        the_map.add(beacon)

    the_map.add(Scanner(0 + x_diff, 0 + y_diff, 0 + z_diff))

    for beacon in scanner_reports[1].beacons:
        the_map.add(Beacon(beacon.x + x_diff, beacon.y + y_diff, beacon.z + z_diff))

    return the_map


def _get_rotation(
    scanner_report: ScannerReport, x_mul: int, y_mul: int, z_mul: int
) -> ScannerReport:

    beacons = [
        Beacon(beacon.x * x_mul, beacon.y * y_mul, beacon.z * z_mul)
        for beacon in scanner_report.beacons
    ]

    return ScannerReport(scanner_report.id, beacons)


def _swap_columns(scanner_report: ScannerReport) -> list[ScannerReport]:
    accessors = [
        ("X", lambda beacon: beacon.x),
        ("Y", lambda beacon: beacon.y),
        ("Z", lambda beacon: beacon.z),
    ]

    reports = []

    for accessor in permutations(accessors, 3):
        print([access[0] for access in accessor])
        reports.append(
            ScannerReport(
                scanner_report.id,
                [
                    Beacon(
                        *map(lambda ac: ac(beacon), [access[1] for access in accessor])
                    )
                    for beacon in scanner_report.beacons
                ],
            )
        )

    return reports


def get_rotations(scanner_report: ScannerReport) -> list[ScannerReport]:
    potential_reports = _swap_columns(scanner_report)

    rotations = [
        (
            [report for i, report in enumerate(potential_reports) if i in [0, 3, 4]],
            [(1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)],
        ),
        (
            [report for i, report in enumerate(potential_reports) if i in [1, 2, 5]],
            [(1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1)],
        ),
    ]

    reports = [
        [
            _get_rotation(report, x_mul, y_mul, z_mul)
            for x_mul, y_mul, z_mul in rotation_set
            for report in report_subset
        ]
        for report_subset, rotation_set in rotations
    ]

    return reports[0] + reports[1]
