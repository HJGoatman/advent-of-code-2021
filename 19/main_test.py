from os import read
from main import (
    read_scanner_reports,
    Beacon,
    ScannerReport,
    find_overlapping_beacons,
    Scanner,
    create_map,
    get_rotations,
)

with open("tests/test1.txt") as input_file:
    test_1_str = input_file.read()


def test_read_scanner_reports():
    assert read_scanner_reports(test_1_str) == [
        ScannerReport(0, [Beacon(0, 2, 0), Beacon(4, 1, 0), Beacon(3, 3, 0)]),
        ScannerReport(1, [Beacon(-1, -1, 0), Beacon(-5, 0, 0), Beacon(-2, 1, 0)]),
    ]


scanner_reports = read_scanner_reports(test_1_str)


def test_find_overlapping_beacons():
    assert find_overlapping_beacons(
        scanner_report_1=scanner_reports[0],
        scanner_report_2=scanner_reports[1],
        min_overlapping_beacons=3,
    ) == {
        Beacon(3, 3, 0): Beacon(-2, 1, 0),
        Beacon(0, 2, 0): Beacon(-5, 0, 0),
        Beacon(4, 1, 0): Beacon(-1, -1, 0),
        Beacon(-2, 1, 0): Beacon(3, 3, 0),
        Beacon(-5, 0, 0): Beacon(0, 2, 0),
        Beacon(-1, -1, 0): Beacon(4, 1, 0),
    }


def test_create_map():
    assert create_map(scanner_reports, 3) == {
        Beacon(0, 2, 0),
        Beacon(4, 1, 0),
        Beacon(3, 3, 0),
        Scanner(0, 0, 0),
        Scanner(5, 2, 0),
    }


def test_get_rotations():
    with open("tests/test2.txt") as input_file:
        input = input_file.read()

    scanner_reports = read_scanner_reports(input)

    rotations = get_rotations(scanner_reports[0])

    assert all([report in rotations for report in scanner_reports[1:]])


def test_overlapping_beacons_2():
    with open("tests/test3.txt") as input_file:
        input = input_file.read()

    scanner_reports = read_scanner_reports(input)

    beacon_mapping = find_overlapping_beacons(
        scanner_reports[0], scanner_reports[1], 12
    )

    assert {
        beacon1
        for beacon1 in beacon_mapping.keys()
        if beacon1 in scanner_reports[0].beacons
    } == {
        Beacon(-618, -824, -621),
        Beacon(-537, -823, -458),
        Beacon(-447, -329, 318),
        Beacon(404, -588, -901),
        Beacon(544, -627, -890),
        Beacon(528, -643, 409),
        Beacon(-661, -816, -575),
        Beacon(390, -675, -793),
        Beacon(423, -701, 434),
        Beacon(-345, -311, 381),
        Beacon(459, -707, 401),
        Beacon(-485, -357, 347),
    }

    assert {
        beacon1
        for beacon1 in beacon_mapping.keys()
        if beacon1 in scanner_reports[1].beacons
    } == {
        Beacon(686, 422, 578),
        Beacon(605, 423, 415),
        Beacon(515, 917, -361),
        Beacon(-336, 658, 858),
        Beacon(-476, 619, 847),
        Beacon(-460, 603, -452),
        Beacon(729, 430, 532),
        Beacon(-322, 571, 750),
        Beacon(-355, 545, -477),
        Beacon(413, 935, -424),
        Beacon(-391, 539, -444),
        Beacon(553, 889, -390),
    }
