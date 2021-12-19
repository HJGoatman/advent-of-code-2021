from main import read_scanner_reports, Beacon, ScannerReport


def test_read_scanner_reports():
    with open("tests/test1.txt") as input_file:
        input_str = input_file.read()

    assert read_scanner_reports(input_str) == [
        ScannerReport(0, [Beacon(0, 2, 0), Beacon(4, 1, 0), Beacon(3, 3, 0)]),
        ScannerReport(1, [Beacon(-1, -1, 0), Beacon(-5, 0, 0), Beacon(-2, 1, 0)]),
    ]
