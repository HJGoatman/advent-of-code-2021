from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor

from functools import reduce

import sys


@dataclass
class SnailFishNumbers:
    depth: int


@dataclass
class Pair(SnailFishNumbers):
    left: SnailFishNumbers
    right: SnailFishNumbers


@dataclass
class RegularNumber(SnailFishNumbers):
    value: int


def load_snailfish_numbers(snailfish_numbers_list, depth=0) -> SnailFishNumbers:
    if isinstance(snailfish_numbers_list, int):
        return RegularNumber(depth=depth, value=snailfish_numbers_list)
    else:
        return Pair(
            left=load_snailfish_numbers(snailfish_numbers_list[0], depth=depth + 1),
            right=load_snailfish_numbers(snailfish_numbers_list[1], depth=depth + 1),
            depth=depth,
        )


def get_leaves(snailfish: SnailFishNumbers) -> list[RegularNumber]:
    if isinstance(snailfish, RegularNumber):
        return [snailfish]

    return get_leaves(snailfish.left) + get_leaves(snailfish.right)


def explode(leaves: list[RegularNumber]) -> list[RegularNumber]:
    i = next(i for i, x in enumerate(leaves) if x.depth > 4)
    j = i + 1

    if i - 1 >= 0:
        leaves[i - 1].value = leaves[i - 1].value + leaves[i].value

    if j + 1 < len(leaves):
        leaves[j + 1].value = leaves[j + 1].value + leaves[j].value

    return leaves[:i] + [RegularNumber(leaves[i].depth - 1, 0)] + leaves[j + 1 :]


def split(leaves: list[RegularNumber]) -> list[RegularNumber]:
    i, x = next((i, x) for i, x in enumerate(leaves) if x.value >= 10)

    return (
        leaves[:i]
        + [
            RegularNumber(x.depth + 1, floor(x.value / 2)),
            RegularNumber(x.depth + 1, ceil(x.value / 2)),
        ]
        + leaves[i + 1 :]
    )


def add(leaves1, leaves2):
    leaves = [RegularNumber(leaf.depth + 1, leaf.value) for leaf in leaves1] + [
        RegularNumber(leaf.depth + 1, leaf.value) for leaf in leaves2
    ]

    while any([leaf.depth > 4 for leaf in leaves]) or any(
        [leaf.value >= 10 for leaf in leaves]
    ):
        if any([leaf.depth > 4 for leaf in leaves]):
            leaves = explode(leaves)
            continue
        if any([leaf.value >= 10 for leaf in leaves]):
            leaves = split(leaves)
            continue

    return leaves


def add_file(input_str):
    snailfish_numbers_list = [
        load_snailfish_numbers(eval(line))
        for line in input_str.split("\n")
        if line != ""
    ]

    leaves_list = [
        get_leaves(snailfish_numbers) for snailfish_numbers in snailfish_numbers_list
    ]

    return reduce(add, leaves_list)


def get_magnitude(pair):
    if isinstance(pair, RegularNumber):
        return pair.value

    return 3 * get_magnitude(pair.left) + 2 * get_magnitude(pair.right)


def leaves_to_tree(leaves: list[RegularNumber]) -> SnailFishNumbers:
    stack = []

    while len(stack) != 1 or len(leaves) != 0:
        if len(stack) < 2:
            stack.append(leaves.pop(0))
            continue

        right = stack.pop()
        left = stack.pop()

        if left.depth == right.depth:
            stack.append(Pair(right.depth - 1, left, right))
        else:
            stack.append(left)
            stack.append(right)
            stack.append(leaves.pop(0))

    return stack[0]


if __name__ == "__main__":
    with open(sys.argv[1], "r") as input_file:
        input = input_file.read()

    print(get_magnitude(leaves_to_tree(add_file(input))))
