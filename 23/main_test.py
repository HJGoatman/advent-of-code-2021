from main import *


def test_load_input():
    with open("tests/state0.txt", "r") as input_file:
        input_str = input_file.read()

    assert load_input(input_str) == State(
        Burrow(
            Hallway([None, None, None, None, None, None, None, None, None, None, None]),
            [
                Room(type=Amber, number=2, occupants=[Bronze(1), Amber(2)]),
                Room(type=Bronze, number=4, occupants=[Copper(3), Desert(4)]),
                Room(type=Copper, number=6, occupants=[Bronze(5), Copper(6)]),
                Room(type=Desert, number=8, occupants=[Desert(7), Amber(8)]),
            ],
        )
    )

