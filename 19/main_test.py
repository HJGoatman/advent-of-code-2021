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
    )[3] == {
        Beacon(3, 3, 0): Beacon(-2, 1, 0),
        Beacon(0, 2, 0): Beacon(-5, 0, 0),
        Beacon(4, 1, 0): Beacon(-1, -1, 0),
        Beacon(-2, 1, 0): Beacon(3, 3, 0),
        Beacon(-5, 0, 0): Beacon(0, 2, 0),
        Beacon(-1, -1, 0): Beacon(4, 1, 0),
    }


def test_create_map():
    scanners, beacons = create_map(scanner_reports, 3)
    assert scanners[1] == (5, 2, 0)
    assert beacons == {
        Beacon(0, 2, 0),
        Beacon(4, 1, 0),
        Beacon(3, 3, 0),
    }


def test_get_rotations():
    with open("tests/test2.txt") as input_file:
        input = input_file.read()

    scanner_reports = read_scanner_reports(input)

    rotation_info = get_rotations(scanner_reports[0])
    list_of_reports = [report for _, _, report in rotation_info]

    assert all([report in list_of_reports for report in scanner_reports[1:]])


def test_overlapping_beacons_2():
    with open("tests/test3.txt") as input_file:
        input = input_file.read()

    scanner_reports = read_scanner_reports(input)

    accessor, rotation, displacement, beacon_mapping = find_overlapping_beacons(
        scanner_reports[0], scanner_reports[1], 12
    )

    print(accessor, rotation, displacement, beacon_mapping)

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

    assert displacement == (68, -1246, -43)


def test_get_list_of_beacons():
    with open("tests/test3.txt") as input_file:
        input = input_file.read()

    scanner_reports = read_scanner_reports(input)

    scanners, beacons = create_map(scanner_reports, 12)

    assert scanners[1] == (68, -1246, -43)
    assert scanners[4] == (-20, -1133, 1061)
    assert scanners[2] == (1105, -1205, 1229)
    assert scanners[3] == (-92, -2380, -20)
    assert beacons == {
        Beacon(-892, 524, 684),
        Beacon(-876, 649, 763),
        Beacon(-838, 591, 734),
        Beacon(-789, 900, -551),
        Beacon(-739, -1745, 668),
        Beacon(-706, -3180, -659),
        Beacon(-697, -3072, -689),
        Beacon(-689, 845, -530),
        Beacon(-687, -1600, 576),
        Beacon(-661, -816, -575),
        Beacon(-654, -3158, -753),
        Beacon(-635, -1737, 486),
        Beacon(-631, -672, 1502),
        Beacon(-624, -1620, 1868),
        Beacon(-620, -3212, 371),
        Beacon(-618, -824, -621),
        Beacon(-612, -1695, 1788),
        Beacon(-601, -1648, -643),
        Beacon(-584, 868, -557),
        Beacon(-537, -823, -458),
        Beacon(-532, -1715, 1894),
        Beacon(-518, -1681, -600),
        Beacon(-499, -1607, -770),
        Beacon(-485, -357, 347),
        Beacon(-470, -3283, 303),
        Beacon(-456, -621, 1527),
        Beacon(-447, -329, 318),
        Beacon(-430, -3130, 366),
        Beacon(-413, -627, 1469),
        Beacon(-345, -311, 381),
        Beacon(-36, -1284, 1171),
        Beacon(-27, -1108, -65),
        Beacon(7, -33, -71),
        Beacon(12, -2351, -103),
        Beacon(26, -1119, 1091),
        Beacon(346, -2985, 342),
        Beacon(366, -3059, 397),
        Beacon(377, -2827, 367),
        Beacon(390, -675, -793),
        Beacon(396, -1931, -563),
        Beacon(404, -588, -901),
        Beacon(408, -1815, 803),
        Beacon(423, -701, 434),
        Beacon(432, -2009, 850),
        Beacon(443, 580, 662),
        Beacon(455, 729, 728),
        Beacon(456, -540, 1869),
        Beacon(459, -707, 401),
        Beacon(465, -695, 1988),
        Beacon(474, 580, 667),
        Beacon(496, -1584, 1900),
        Beacon(497, -1838, -617),
        Beacon(527, -524, 1933),
        Beacon(528, -643, 409),
        Beacon(534, -1912, 768),
        Beacon(544, -627, -890),
        Beacon(553, 345, -567),
        Beacon(564, 392, -477),
        Beacon(568, -2007, -577),
        Beacon(605, -1665, 1952),
        Beacon(612, -1593, 1893),
        Beacon(630, 319, -379),
        Beacon(686, -3108, -505),
        Beacon(776, -3184, -501),
        Beacon(846, -3110, -434),
        Beacon(1135, -1161, 1235),
        Beacon(1243, -1093, 1063),
        Beacon(1660, -552, 429),
        Beacon(1693, -557, 386),
        Beacon(1735, -437, 1738),
        Beacon(1749, -1800, 1813),
        Beacon(1772, -405, 1572),
        Beacon(1776, -675, 371),
        Beacon(1779, -442, 1789),
        Beacon(1780, -1548, 337),
        Beacon(1786, -1538, 337),
        Beacon(1847, -1591, 415),
        Beacon(1889, -1729, 1762),
        Beacon(1994, -1805, 1792),
    }
    assert len(beacons) == 79
