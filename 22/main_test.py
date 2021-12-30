from functools import reduce
from main import (
    Range,
    ReactorCore,
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
        OnRebootStep(x=Range(10, 13), y=Range(10, 13), z=Range(10, 13)),
        OnRebootStep(x=Range(11, 14), y=Range(11, 14), z=Range(11, 14)),
        OffRebootStep(x=Range(9, 12), y=Range(9, 12), z=Range(9, 12)),
        OnRebootStep(x=Range(10, 11), y=Range(10, 11), z=Range(10, 11)),
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


def is_inside(core, inside, value=1):
    for x, y, z in inside:
        print(x, y, z)
        assert core.has((x, y, z), value)


def test_steps_1():

    core = ReactorCore(Range(0, 100), Range(0, 100), Range(0, 100))

    core = execute_step(core, input_1[0], is_initialization=True)

    is_inside(core, inside_1)

    core = execute_step(core, input_1[1], is_initialization=True)

    is_inside(core, inside_2)

    core = execute_step(core, input_1[2], is_initialization=True)

    is_inside(core, not_inside, value=0)

    core = execute_step(core, input_1[3], is_initialization=True)

    is_inside(core, [(10, 10, 10)])

    assert core.count_on() == 39


def test_steps_2():
    with open("tests/test2.txt") as test_file:
        test_str = test_file.read()

    steps = load_input(test_str)
    core = ReactorCore(*load_ranges("x=-50..50,y=-50..50,z=-50..50"))
    core = reduce(
        lambda core, step: execute_step(core, step, is_initialization=True), steps, core
    )
    assert core.count_on() == 590784


def test_part_2():
    with open("tests/test3.txt") as test_file:
        test_str = test_file.read()

    steps = load_input(test_str)

    core = ReactorCore(
        Range(min([step.x.min for step in steps]), max([step.x.max for step in steps])),
        Range(min([step.y.min for step in steps]), max([step.y.max for step in steps])),
        Range(min([step.z.min for step in steps]), max([step.z.max for step in steps])),
    )

    core = reduce(execute_step, steps, core)
    assert core.count_on() == 2758514936282235
