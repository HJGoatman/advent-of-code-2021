import sys
from collections import Counter
from itertools import chain


# Method created by @andreasf6
def get_numbers(letters):
    one = list("".join(filter(lambda l: len(l) == 2, letters)))
    seven = list("".join(filter(lambda l: len(l) == 3, letters)))
    four = list("".join(filter(lambda l: len(l) == 4, letters)))
    eight = list("".join(filter(lambda l: len(l) == 7, letters)))
    two_three_five = list((filter(lambda l: len(l) == 5, letters)))
    zero_six_nine = list((filter(lambda l: len(l) == 6, letters)))

    a = set(seven) - set(one)
    d_g = set.intersection(*map(set, two_three_five)) - set(a)
    d = d_g.intersection(set(four))
    g = d_g - set(four) - d

    e_b = set(
        [k for k, v in Counter(chain(*map(list, two_three_five))).items() if v == 1]
    )
    b = set(four) - d - set(one)
    e = e_b - b

    zero = set([x for x in zero_six_nine if str(x).find(("".join(d))) == -1])
    six_nine = set(zero_six_nine) - zero
    f = set().union(
        *[
            letter.intersection(set(one))
            for letter in (map(set, six_nine))
            if len(letter.intersection(set(one))) == 1
        ]
    )
    c = set(one) - f

    # zero = (''.join(zero))

    def get_matching_letter(number, letters):
        return filter(lambda letter: set(list(letter)) == set(number), letters)[0]

    zero = "".join(sorted(get_matching_letter(list(zero)[0], letters)))
    one = "".join(sorted(get_matching_letter(one, letters)))
    two = "".join(sorted(get_matching_letter(list(chain(a, c, d, e, g)), letters)))
    three = "".join(sorted(get_matching_letter(list(chain(a, c, d, f, g)), letters)))
    four = "".join(sorted(get_matching_letter(four, letters)))
    five = "".join(sorted(get_matching_letter(list(chain(a, b, d, f, g)), letters)))
    six = "".join(sorted(get_matching_letter(list(chain(a, b, d, e, f, g)), letters)))
    seven = "".join(sorted(get_matching_letter(seven, letters)))
    eight = "".join(sorted(get_matching_letter(eight, letters)))
    nine = "".join(sorted(get_matching_letter(list(chain(a, b, c, d, f, g)), letters)))

    return {
        zero: 0,
        one: 1,
        two: 2,
        three: 3,
        four: 4,
        five: 5,
        six: 6,
        seven: 7,
        eight: 8,
        nine: 9,
    }


with open(sys.argv[1], "r") as input_file:
    input = input_file.read()

values = [new_line.split(" | ") for new_line in input.split("\n") if new_line != ""]
values = [(input_str.split(), output_str.split()) for input_str, output_str in values]

outputs = []
for input_values, output_values in values:
    number_map = get_numbers(input_values)
    
    outputs.append(
        int(
            "".join(
                list(map(lambda x: str(number_map["".join(sorted(x))]), output_values))
            )
        )
    )

print(sum(outputs))