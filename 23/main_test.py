from main import *


def test_load_input():
    with open("tests/state0.txt", "r") as input_file:
        input_str = input_file.read()

    assert load_input(input_str) == State(
        Burrow(
            Hallway([None, None, None, None, None, None, None, None, None, None, None]),
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        )
    )

