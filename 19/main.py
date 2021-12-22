from dataclasses import dataclass
from functools import reduce
from itertools import permutations, combinations, product


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
) -> list[Beacon]:
    edge_pairs = product(
        *[
            [
                Edge(id=i, start=start, end=end)
                for i, (start, end) in enumerate(combinations(report.beacons, 2))
            ]
            for report in [scanner_report_1, scanner_report_2]
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

    if (len(beacon_mapping) / 2) >= min_overlapping_beacons:
        return beacon_mapping
    else:
        return {}


def create_map(scanner_reports: list[ScannerReport], min_overlapping_beacons):
    the_map = set()

    beacon_map = find_overlapping_beacons(
        scanner_reports[0], scanner_reports[1], min_overlapping_beacons
    )

    differences = [
        (beacon1.x - beacon2.x, beacon1.y - beacon2.y, beacon1.z - beacon2.z)
        for beacon1, beacon2 in beacon_map.items()
        if beacon1 in scanner_reports[0].beacons
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
