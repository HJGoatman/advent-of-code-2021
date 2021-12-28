from __future__ import annotations
import sys
import re
from dataclasses import dataclass
from itertools import cycle, repeat, product
from functools import reduce
from collections import Counter
from typing import Tuple


@dataclass
class Player:
    id: int
    position: int
    score: int


@dataclass
class GameTree:
    pass


@dataclass
class Node(GameTree):
    # players: list[Player]
    # player_id: int
    # position: int
    # score: int
    # move: int
    subnodes: list[Node]


@dataclass
class Winner(GameTree):
    id: int
    repeats: int


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


def create_game_tree(
    active_player: Player,
    other_player: Player,
    move: int,
    winning_score: int,
    repeats: int,
    possible_moves,
    is_first: bool,
) -> Tuple[int, int]:
    if not is_first:
        position = ((active_player.position + move - 1) % 10) + 1
        score = active_player.score + position
    else:
        position = active_player.position
        score = active_player.score

    if score >= winning_score:
        if active_player.id == 1:
            return (repeats, 0)
        else:
            return (0, repeats)

    results = []
    for move, repeat in possible_moves:
        result = create_game_tree(
            active_player=other_player,
            other_player=Player(active_player.id, position, score),
            move=move,
            winning_score=winning_score,
            repeats=repeats * repeat,
            possible_moves=possible_moves,
            is_first=False,
        )

        results.append(result)

    return reduce(
        lambda pair1, pair2: (pair1[0] + pair2[0], pair1[1] + pair2[1]), results
    )


# def sum_winners(tree: GameTree) -> Tuple[int, int]:
#     if isinstance(tree, Winner):


def play_dirac(player1, player2):
    possible_moves = list(Counter(map(sum, product(*repeat([1, 2, 3], 3)))).items())

    game_tree = create_game_tree(
        player2, player1, 0, 21, 1, possible_moves=possible_moves, is_first=True
    )

    return max(game_tree)


if __name__ == "__main__":
    with open(sys.argv[1]) as input_file:
        input_str = input_file.read()

    players = load_input(input_str)
    print(play_game(*players))

    players = load_input(input_str)
    print(play_dirac(*players))
