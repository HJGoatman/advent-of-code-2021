from os import stat
import sys

def state_to_string(state):
    state = [str(laternfish) for laternfish in state]
    return ",".join(state)


with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

initial_state = [int(val) for val in input.split(',')]

state = [len(list(filter(lambda x: x == i, initial_state))) for i in range(0,9)]

for day in range(1, int(sys.argv[2]) + 1):
    number_of_births = state.pop(0)
    state[6] = state[6] + number_of_births
    state.append(number_of_births)

print(sum(state))