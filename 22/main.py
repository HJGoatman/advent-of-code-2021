from dataclasses import dataclass
from itertools import product
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


@dataclass
class Cuboid:
    x: Range
    y: Range
    z: Range


class ReactorCore:
    def __init__(self, x: Range, y: Range, z: Range) -> None:
        self.x_range = x
        self.y_range = y
        self.z_range = z
        self.cuboids = []

    @staticmethod
    def _fully_contained(cuboid1: Cuboid, cuboid2: Cuboid) -> bool:
        return (
            (cuboid1.x.min >= cuboid2.x.min and cuboid1.x.max <= cuboid2.x.max)
            and (cuboid1.y.min >= cuboid2.y.min and cuboid1.y.max <= cuboid2.y.max)
            and (cuboid1.z.min >= cuboid2.z.min and cuboid1.z.max <= cuboid2.z.max)
        )

    @staticmethod
    def _range_overlap(range1: Range, range2: Range) -> bool:
        return max(range1.min, range2.min) < min(range1.max, range2.max)

    @staticmethod
    def _no_overlap(cuboid1: Cuboid, cuboid2: Cuboid) -> bool:
        # For two cuboids to overlap,
        # the range of one cuboid should be partially contained in the other, for all dimensions.

        return not (
            ReactorCore._range_overlap(cuboid1.x, cuboid2.x)
            and ReactorCore._range_overlap(cuboid1.y, cuboid2.y)
            and ReactorCore._range_overlap(cuboid1.z, cuboid2.z)
        )

    @staticmethod
    def _split_cubes(insert_cuboid, overlapping):
        split_ranges = []
        for range1, range2 in zip(
            [insert_cuboid.x, insert_cuboid.y, insert_cuboid.z],
            [overlapping.x, overlapping.y, overlapping.z],
        ):
            # if (range1.min == range2.min) and (range1.max == range2.max):
            #     potential_ranges = [(range1.min, range1.max)]
            # elif (range1.min >= range2.min) and (range1.max <= range2.max):
            #     potential_ranges = [(range1.min, range1.max)]
            # elif (range1.min <= range2.min) and (range1.max <= range2.max):
            #     potential_ranges = [(range1.min, range2.min), (range2.min, range1.max)]
            # elif (range1.min <= range2.max) and (range2.max <= range1.max):
            #     potential_ranges = [(range1.min, range2.max), (range2.max, range1.max)]
            # else:
            #     potential_ranges = [
            #         (range1.min, range2.min),
            #         (range2.min, range2.max),
            #         (range2.max, range1.max),
            #     ]

            # Try to intersect with range 2 min and max.
            range_filter = (
                [range1.min]
                + list(
                    filter(
                        lambda val: range1.min < val < range1.max,
                        [range2.min, range2.max],
                    )
                )
                + [range1.max]
            )

            ranges = []
            for i in range(len(range_filter) - 1):
                ranges.append(Range(range_filter[i], range_filter[i + 1]))

            split_ranges.append(ranges)

        return [
            Cuboid(ranges[0], ranges[1], ranges[2]) for ranges in product(*split_ranges)
        ]

    def _set_on(self, x: Range, y: Range, z: Range) -> None:
        stack = [Cuboid(x, y, z)]

        while stack:
            insert_cuboid = stack.pop()

            # If cuboid is fully contained.
            if any(
                [
                    ReactorCore._fully_contained(insert_cuboid, cuboid)
                    for cuboid in self.cuboids
                ]
            ):
                continue

            # If cuboid is not overlapping for all.
            if all(
                [
                    ReactorCore._no_overlap(insert_cuboid, cuboid)
                    for cuboid in self.cuboids
                ]
            ):
                self.cuboids.append(insert_cuboid)
                continue

            # Split cuboid up based on first overlapping cuboid and add splits to stack.
            overlapping = next(
                filter(
                    lambda cuboid: not ReactorCore._no_overlap(insert_cuboid, cuboid),
                    self.cuboids,
                )
            )

            new_cuboids = ReactorCore._split_cubes(insert_cuboid, overlapping)

            stack = stack + new_cuboids

        return

    def _set_off(self, x: Range, y: Range, z: Range) -> None:
        # Take out overlapping cubes, split them and add the non-overlapping splits.
        removal_cuboid = Cuboid(x, y, z)

        overlapping_cuboids = list(
            filter(
                lambda cuboid: not ReactorCore._no_overlap(removal_cuboid, cuboid),
                self.cuboids,
            )
        )

        self.cuboids = [
            cuboid for cuboid in self.cuboids if cuboid not in overlapping_cuboids
        ]

        for overlapping_cuboid in overlapping_cuboids:
            potential_cuboids = ReactorCore._split_cubes(
                overlapping_cuboid, removal_cuboid
            )

            non_overlapping = list(
                filter(
                    lambda x: not ReactorCore._fully_contained(x, removal_cuboid),
                    potential_cuboids,
                )
            )

            self.cuboids = self.cuboids + non_overlapping

        return

    def set(self, x: Range, y: Range, z: Range, value) -> None:
        if value == 1:
            self._set_on(x, y, z)
        else:
            self._set_off(x, y, z)

    @staticmethod
    def _is_in(coordinate, cuboid):
        return (
            (cuboid.x.min <= coordinate[0] < cuboid.x.max)
            and (cuboid.y.min <= coordinate[1] < cuboid.y.max)
            and (cuboid.z.min <= coordinate[2] < cuboid.z.max)
        )

    def has(self, coordinate, value) -> bool:
        coordinate_exists = any(
            [ReactorCore._is_in(coordinate, cuboid) for cuboid in self.cuboids]
        )

        if value == 1:
            return coordinate_exists
        else:
            return not coordinate_exists

    @staticmethod
    def _get_range_dist(range: Range):
        return range.max - range.min

    def count_on(self) -> int:
        return sum(
            [
                ReactorCore._get_range_dist(cuboid.x)
                * ReactorCore._get_range_dist(cuboid.y)
                * ReactorCore._get_range_dist(cuboid.z)
                for cuboid in self.cuboids
            ]
        )


def load_range(range: str) -> Range:
    min_str, max_str = re.search(r"[x|y|z]=(-?\d+)..(-?\d+)", range).groups()
    return Range(int(min_str), int(max_str) + 1)


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


def execute_step(
    core: ReactorCore, step: RebootStep, is_initialization=False
) -> ReactorCore:
    x, y, z = step.x, step.y, step.z

    if is_initialization:
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
