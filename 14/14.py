import sys
from functools import reduce
from collections import Counter

with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

steps = int(sys.argv[2])

template, insertion_rules_str = input.split("\n\n")

insertion_rules = {
    match: insert
    for match, insert in [
        tuple(rule_str.split(" -> "))
        for rule_str in insertion_rules_str.split("\n")
        if rule_str != ""
    ]
}


for i in range(steps):
    pairs = [template[j : j + 2] for j in range(len(template) - 1)]

    triples = list(map(lambda pair: pair[0] + insertion_rules[pair] + pair[1], pairs))

    template = reduce(lambda x, y: x + y[:2], triples, "") + triples[-1][-1]


count_values = Counter(template).values()

print(max(count_values) - min(count_values))
