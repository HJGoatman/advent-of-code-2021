import sys
import numpy as np

def to_board(board_str):
    values = np.asarray([[int(num) for num in row.strip().split()] for row in board_str.split("\n")])
    marked = np.zeros_like(values).astype(bool)

    return [values, marked]


with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

parts = input.split("\n\n")
numbers = [int(number) for number in parts[0].split(",")]
boards = list(map(to_board, parts[1:]))

scores = []

for number in numbers:
    # Mark off matching number for each board.
    for i, board in enumerate(boards):
        boards[i][1] = board[1] | (board[0] == number)

    # Check if any rows or columns are all true.
    for i, (values, marked) in enumerate(boards):
        if np.any(np.all(marked, axis=0)) or np.any(np.all(marked, axis=1)):
            # print(number, values, marked)
            score = np.sum(values[~marked]) * number
            scores.append(score)
            boards.pop(i)

print(scores[-1])        
