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

pair_counter = {match: 0 for match in insertion_rules.keys()}
pairs = [template[j : j + 2] for j in range(len(template) - 1)]
for pair in pairs:
    pair_counter[pair] = pair_counter[pair] + 1


def get_new_pairs(pair, amount):
    new_value = insertion_rules[pair]
    return {pair[0] + new_value: amount, new_value + pair[1]: amount}


def combine_dicts(dict1, dict2):
    return Counter(dict1) + Counter(dict2)


for i in range(steps):
    pair_counter = reduce(
        combine_dicts,
        map(lambda x: get_new_pairs(*x), list(pair_counter.items())),
    )


letter_count = reduce(
    combine_dicts,
    [{key[1]: amount} for key, amount in pair_counter.items()],
)

letter_count[template[0]] = letter_count[template[0]] + 1

count_values = letter_count.values()

print(max(count_values) - min(count_values))
