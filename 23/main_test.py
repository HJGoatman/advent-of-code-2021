from main import *
from states import possible_moves_1


def get_initial_state():
    with open("tests/state0.txt", "r") as input_file:
        input_str = input_file.read()

    return load_input(input_str)


def test_load_input():

    assert get_initial_state() == State(
        Burrow(
            [None, None, None, None, None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        )
    )


def test_get_moves():
    state = get_initial_state()

    assert get_moves(state) == possible_moves_1
