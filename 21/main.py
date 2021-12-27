import sys
import re
from dataclasses import dataclass


@dataclass
class Player:
    id: int
    position: int
    score: int


def load_input(input: str) -> list[Player]:
    return [
        Player(
            *map(
                int, re.search(r"Player (\d)+ starting position: (\d)+", line).groups()
            ),
            0
        )
        for line in input.split("\n")
        if line != ""
    ]


if __name__ == "__main__":
    with open(sys.argv[1]) as input_file:
        input_str = input_file.read()

    players = load_input(input_str)
