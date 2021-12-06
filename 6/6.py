from os import stat
import sys

def state_to_string(state):
    state = [str(laternfish) for laternfish in state]
    return ",".join(state)


with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

initial_state = [int(val) for val in input.split(',')]
# print(f'Initial state: {state_to_string(initial_state)}')

state = initial_state.copy()
for day in range(1, int(sys.argv[2]) + 1):
    ready_to_born_idx = [i for i, x in enumerate(state) if x == 0]
    for i in ready_to_born_idx:
        state.append(9)
        state[i] = 7

    state = list(map(lambda laternfish: laternfish - 1, state))
    # print(f"After {day} day: {state_to_string(state)}")
    
    
print(f"Total Fish after day {day}: {len(state)}")