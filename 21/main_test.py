from main import Player, load_input

with open("tests/test1.txt") as test_file:
    test_str = test_file.read()


def test_load_input():
    assert load_input(test_str) == [
        Player(1, 4, 0),
        Player(2, 8, 0),
    ]
