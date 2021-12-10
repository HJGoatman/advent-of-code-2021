import sys

with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

lines = [line for line in input.split("\n") if line != '']

get_match = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>'
}

class SyntaxError(Exception):
    def __init__(self, got, expected, *args: object) -> None:
        super().__init__(*args)
        self.got = got
        self.expected = expected
        
class MissingError(Exception):
    def __init__(self, input, end, *args: object) -> None:
        super().__init__(*args)
        self.end = end
        self.input = input


def is_correct_syntax(input_str):
    stack = []

    for char in input_str:
        if char in ['(', '{', '<', '[']:
            stack.append(char)
        else:
            match = stack.pop()
            if match == '(' and char == ')':
                continue
            elif match == '{' and char == '}':
                continue
            elif match == '<' and char == '>':
                continue
            elif match == '[' and char == ']':
                continue
            else:
                raise SyntaxError(char, match)

    if len(stack) == 0:
        return True
    else:

        raise MissingError(input_str, [get_match[val] for val in reversed(stack)])
    
scoring = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

autocomplete_scoring = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

points = 0
autocomplete_scores = []
for line in lines:
    

    try:
        is_correct_syntax(line)
    except SyntaxError as e:
        points = points + scoring[e.got]
    except MissingError as e:
        autocomplete_score = 0

        # print(e.input)
        # print(e.end)
        for char in e.end:
            
            autocomplete_score = autocomplete_score * 5 + autocomplete_scoring[char]
            # print(autocomplete_score)

        autocomplete_scores.append(autocomplete_score)

print(points)
print(sorted(autocomplete_scores)[int((len(autocomplete_scores) - 1) / 2)])