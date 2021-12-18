from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor


@dataclass
class SnailFishNumbers:
    pass


@dataclass
class Pair(SnailFishNumbers):
    left: SnailFishNumbers
    right: SnailFishNumbers
    depth: int


@dataclass
class RegularNumber(SnailFishNumbers):
    value: int


def load_snailfish_numbers(snailfish_numbers_list, depth=0) -> SnailFishNumbers:
    if isinstance(snailfish_numbers_list, int):
        return RegularNumber(value=snailfish_numbers_list)
    else:
        return Pair(
            left=load_snailfish_numbers(snailfish_numbers_list[0], depth=depth + 1),
            right=load_snailfish_numbers(snailfish_numbers_list[1], depth=depth + 1),
            depth=depth,
        )


def get_exploded_value(numbers: SnailFishNumbers, is_right: bool) -> RegularNumber:
    if isinstance(numbers, Pair) and numbers.depth == 4:
        if is_right:
            return numbers.right
        else:
            return numbers.left

    if isinstance(numbers, RegularNumber):
        return None

    for pair in [numbers.left, numbers.right]:
        value = get_exploded_value(pair, is_right=is_right)
        if value is not None:
            return value

    return None


def has_regular_number(
    numbers: SnailFishNumbers, max_depth: int, is_right: bool
) -> bool:
    if isinstance(numbers, RegularNumber):
        return False

    if is_right:
        search_side = numbers.right
        other_side = numbers.left
    else:
        search_side = numbers.left
        other_side = numbers.right

    if isinstance(search_side, RegularNumber) and numbers.depth < max_depth:
        return True
    else:
        return has_regular_number(
            other_side, max_depth - 1, is_right
        ) or has_regular_number(other_side, max_depth - 1, is_right)


def explode(numbers: SnailFishNumbers) -> SnailFishNumbers:
    if isinstance(numbers, RegularNumber):
        return numbers

    if numbers.depth == 4:
        return RegularNumber(0)

    exploded_right_value = get_exploded_value(numbers, is_right=True)
    exploded_left_value = get_exploded_value(numbers, is_right=False)

    if exploded_right_value is None or exploded_left_value is None:
        return numbers

    if isinstance(numbers.right, RegularNumber) and not has_regular_number(
        numbers.left, 4, is_right=True
    ):
        return Pair(
            left=explode(numbers.left),
            right=RegularNumber(
                numbers.right.value + exploded_right_value.value,
            ),
            depth=numbers.depth,
        )

    if isinstance(numbers.left, RegularNumber) and not has_regular_number(
        numbers.right, 4, is_right=False
    ):
        return Pair(
            left=RegularNumber(
                numbers.left.value + exploded_left_value.value,
            ),
            right=explode(numbers.right),
            depth=numbers.depth,
        )

    return Pair(
        left=explode(numbers.left),
        right=explode(numbers.right),
        depth=numbers.depth,
    )


def split(numbers: SnailFishNumbers, depth: int) -> SnailFishNumbers:
    if isinstance(numbers, RegularNumber):
        if numbers.value > 10:
            split_value = numbers.value / 2
            return Pair(
                left=RegularNumber(floor(split_value)),
                right=RegularNumber(ceil(split_value)),
                depth=depth,
            )

        return numbers

    return Pair(
        left=explode_split(numbers.left, numbers.depth + 1),
        right=explode_split(numbers.right, numbers.depth + 1),
        depth=numbers.depth,
    )


def explode_split(numbers: SnailFishNumbers, depth) -> SnailFishNumbers:
    return split(explode(numbers), depth)


def add(list1, list2):
    return explode_split(load_snailfish_numbers(list1 + list2), 0)
