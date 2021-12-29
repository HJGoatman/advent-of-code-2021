from dataclasses import dataclass
import re
import numpy as np


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


def load_range(range: str) -> Range:
    min_str, max_str = re.search(r"[x|y|z]=(\d+)..(\d+)", range).groups()
    return Range(int(min_str), int(max_str))


def load_step(step: str) -> RebootStep:
    step_type, ranges_str = step.split(" ")
    ranges = map(load_range, ranges_str.split(","))
    if step_type == "on":
        return OnRebootStep(*ranges)
    else:
        return OffRebootStep(*ranges)


def load_input(input: str) -> list[RebootStep]:
    return [load_step(line) for line in input.split("\n") if line != ""]


def create_cube(x_size, y_size, z_size):
    array = np.zeros(
        (
            x_size + 1,
            y_size + 1,
            z_size + 1,
        )
    ).astype(int)

    return array


def execute_step(cube: np.ndarray, step: RebootStep) -> np.ndarray:
    x, y, z = step.x, step.y, step.z
    if isinstance(step, OnRebootStep):
        value = 1
    else:
        value = 0

    cube = cube.copy()

    cube[x.min : x.max + 1, y.min : y.max + 1, z.min : z.max + 1] = value

    return cube
