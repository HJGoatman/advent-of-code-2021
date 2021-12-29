from dataclasses import dataclass
import re
import numpy as np
from functools import reduce
import sys


@dataclass
class Range:
    min: int
    max: int


@dataclass
class RebootStep:
    x: Range
    y: Range
    z: Range


@dataclass
class OnRebootStep(RebootStep):
    pass


@dataclass
class OffRebootStep(RebootStep):
    pass


class ReactorCore:
    def __init__(self, x: Range, y: Range, z: Range) -> None:
        self.x_range = x
        self.y_range = y
        self.z_range = z
        self.x_offset, self.y_offset, self.z_offset = 0 - x.min, 0 - y.min, 0 - z.min
        self.array = np.zeros(
            (x.max - x.min + 1, y.max - y.min + 1, z.max - z.min + 1), np.bool_
        )

    def set(self, x: Range, y: Range, z: Range, value) -> None:
        self.array[
            x.min + self.x_offset : x.max + self.x_offset + 1,
            y.min + self.y_offset : y.max + self.y_offset + 1,
            z.min + self.z_offset : z.max + self.z_offset + 1,
        ] = value

    def has(self, coordinate, value) -> bool:
        x, y, z = coordinate
        return (
            self.array[x + self.x_offset, y + self.y_offset, z + self.z_offset] == value
        )

    def count_on(self) -> int:
        return np.sum(self.array == 1)


def load_range(range: str) -> Range:
    min_str, max_str = re.search(r"[x|y|z]=(-?\d+)..(-?\d+)", range).groups()
    return Range(int(min_str), int(max_str))


def load_ranges(ranges: str) -> list[Range]:
    return map(load_range, ranges.split(","))


def load_step(step: str) -> RebootStep:
    step_type, ranges_str = step.split(" ")
    ranges = load_ranges(ranges_str)
    if step_type == "on":
        return OnRebootStep(*ranges)
    else:
        return OffRebootStep(*ranges)


def load_input(input: str) -> list[RebootStep]:
    return [load_step(line) for line in input.split("\n") if line != ""]


def execute_step(core: ReactorCore, step: RebootStep) -> ReactorCore:
    x, y, z = step.x, step.y, step.z

    if (
        (x.min < core.x_range.min)
        or (x.max > core.x_range.max)
        or (y.min < core.y_range.min)
        or (y.max > core.y_range.max)
        or (z.min < core.z_range.min)
        or (z.max > core.z_range.max)
    ):
        return core

    if isinstance(step, OnRebootStep):
        value = 1
    else:
        value = 0

    core.set(x, y, z, value)

    return core


if __name__ == "__main__":
    with open(sys.argv[1]) as input_file:
        input_str = input_file.read()

    steps = load_input(input_str)
    cube = ReactorCore(*load_ranges("x=-50..50,y=-50..50,z=-50..50"))
    cube = reduce(execute_step, steps, cube)
    print(cube.count_on())
