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

    assert (
        find_overlapping_beacons(
            scanner_report_1=scanner_reports[0],
            scanner_report_2=scanner_reports[1],
            min_overlapping_beacons=3,
        )
        == {2: 2, 0: 1, 1: 0}
    )


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


