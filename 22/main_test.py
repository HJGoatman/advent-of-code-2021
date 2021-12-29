from functools import reduce
from main import (
    Range,
    Cube,
    OnRebootStep,
    OffRebootStep,
    load_input,
    execute_step,
    load_ranges,
)
import numpy as np

with open("tests/test1.txt") as test_file:
    test_str = test_file.read()

input_1 = load_input(test_str)


def test_load_input():

    assert input_1 == [
        OnRebootStep(x=Range(10, 12), y=Range(10, 12), z=Range(10, 12)),
        OnRebootStep(x=Range(11, 13), y=Range(11, 13), z=Range(11, 13)),
        OffRebootStep(x=Range(9, 11), y=Range(9, 11), z=Range(9, 11)),
        OnRebootStep(x=Range(10, 10), y=Range(10, 10), z=Range(10, 10)),
    ]


inside_1 = [
    (10, 10, 10),
    (10, 10, 11),
    (10, 10, 12),
    (10, 11, 10),
    (10, 11, 11),
    (10, 11, 12),
    (10, 12, 10),
    (10, 12, 11),
    (10, 12, 12),
    (11, 10, 10),
    (11, 10, 11),
    (11, 10, 12),
    (11, 11, 10),
    (11, 11, 11),
    (11, 11, 12),
    (11, 12, 10),
    (11, 12, 11),
    (11, 12, 12),
    (12, 10, 10),
    (12, 10, 11),
    (12, 10, 12),
    (12, 11, 10),
    (12, 11, 11),
    (12, 11, 12),
    (12, 12, 10),
    (12, 12, 11),
    (12, 12, 12),
]

inside_2 = [
    (11, 11, 13),
    (11, 12, 13),
    (11, 13, 11),
    (11, 13, 12),
    (11, 13, 13),
    (12, 11, 13),
    (12, 12, 13),
    (12, 13, 11),
    (12, 13, 12),
    (12, 13, 13),
    (13, 11, 11),
    (13, 11, 12),
    (13, 11, 13),
    (13, 12, 11),
    (13, 12, 12),
    (13, 12, 13),
    (13, 13, 11),
    (13, 13, 12),
    (13, 13, 13),
]

not_inside = [
    (10, 10, 10),
    (10, 10, 11),
    (10, 11, 10),
    (10, 11, 11),
    (11, 10, 10),
    (11, 10, 11),
    (11, 11, 10),
    (11, 11, 11),
]


def is_inside(cube, inside, value=1):
    for x, y, z in inside:
        print(x, y, z)
        assert cube.has((x, y, z), value)


def test_steps_1():

    cube = Cube(Range(0, 100), Range(0, 100), Range(0, 100))

    cube = execute_step(cube, input_1[0])

    is_inside(cube, inside_1)

    cube = execute_step(cube, input_1[1])

    is_inside(cube, inside_2)

    cube = execute_step(cube, input_1[2])

    is_inside(cube, not_inside, value=0)

    cube = execute_step(cube, input_1[3])

    is_inside(cube, [(10, 10, 10)])

    assert cube.count_on() == 39


def test_steps_2():
    with open("tests/test2.txt") as test_file:
        test_str = test_file.read()

    steps = load_input(test_str)
    cube = Cube(*load_ranges("x=-50..50,y=-50..50,z=-50..50"))
    cube = reduce(execute_step, steps, cube)
    assert cube.count_on() == 590784
