import sys
import re
from dataclasses import dataclass
from itertools import cycle


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


def play_round(die, board, player):
    move = next(die) + next(die) + next(die)
    player.position = player.position + move

    player.score = player.score + board[(player.position - 1) % 10]


def play_game(player1, player2):
    die = cycle(range(1, 101))
    board = list(range(1, 11))

    counter = 0
    player1_turn = True
    while player1.score < 1000 and player2.score < 1000:
        if player1_turn:
            play_round(die, board, player1)
        else:
            play_round(die, board, player2)

        player1_turn = not player1_turn

        counter = counter + 3

    return counter * min(player1.score, player2.score)


if __name__ == "__main__":
    with open(sys.argv[1]) as input_file:
        input_str = input_file.read()

    players = load_input(input_str)
    print(play_game(*players))
