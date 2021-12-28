from main import Range, OnRebootStep, OffRebootStep, load_input


def test_load_input():
    with open("tests/test1.txt") as test_file:
        test_str = test_file.read()
    assert load_input(test_str) == [
        OnRebootStep(x=Range(10, 12), y=Range(10, 12), z=Range(10, 12)),
        OnRebootStep(x=Range(11, 13), y=Range(11, 13), z=Range(11, 13)),
        OffRebootStep(x=Range(9, 11), y=Range(9, 11), z=Range(9, 11)),
        OnRebootStep(x=Range(10, 10), y=Range(10, 10), z=Range(10, 10)),
    ]
