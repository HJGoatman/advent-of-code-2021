from main import Player, load_input, play_round, play_game

with open("tests/test1.txt") as test_file:
    test_str = test_file.read()


def test_load_input():
    assert load_input(test_str) == [
        Player(1, 4, 0),
        Player(2, 8, 0),
    ]


def test_play_round():
    die = iter(range(1, 101))
    board = list(range(1, 11))
    player1, player2 = load_input(test_str)

    play_round(die, board, player1)
    assert player1.score == 10
    play_round(die, board, player2)
    assert player2.score == 3
    play_round(die, board, player1)
    assert player1.score == 14
    play_round(die, board, player2)
    assert player2.score == 9
    play_round(die, board, player1)
    assert player1.score == 20
    play_round(die, board, player2)
    assert player2.score == 16
    play_round(die, board, player1)
    assert player1.score == 26
    play_round(die, board, player2)
    assert player2.score == 22


def test_play_game():
    player1, player2 = load_input(test_str)
    rounds = play_game(player1, player2)
    print(rounds)

    assert rounds * min(player1.score, player2.score) == 739785
