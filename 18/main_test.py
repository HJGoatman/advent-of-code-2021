from main import (
    explode,
    load_snailfish_numbers,
    get_exploded_value,
    RegularNumber,
    has_regular_number,
    split,
    add,
)

numbers_1 = load_snailfish_numbers([[[[[9, 8], 1], 2], 3], 4])


def test_get_exploded_right():
    assert get_exploded_value(numbers_1, is_right=True) == RegularNumber(8)


def test_get_exploded_left():
    assert get_exploded_value(numbers_1, is_right=False) == RegularNumber(9)


def test_has_right_number_1():
    assert has_regular_number(load_snailfish_numbers([0, 1]), 2, is_right=True) == True


def test_has_right_number_2():
    assert (
        has_regular_number(load_snailfish_numbers([6, [5, [7, 0]]]), 2, is_right=True)
        == False
    )


def test_explode_1():
    assert explode(numbers_1) == load_snailfish_numbers([[[[0, 9], 2], 3], 4])


def test_explode_2():
    assert explode(
        load_snailfish_numbers([7, [6, [5, [4, [3, 2]]]]])
    ) == load_snailfish_numbers([7, [6, [5, [7, 0]]]])


def test_explode_3():
    assert explode(
        load_snailfish_numbers([[6, [5, [4, [3, 2]]]], 1])
    ) == load_snailfish_numbers([[6, [5, [7, 0]]], 3])


def test_explode_4():
    assert explode(
        load_snailfish_numbers([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    ) == load_snailfish_numbers([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])


def test_explode_5():
    assert explode(
        load_snailfish_numbers([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    ) == load_snailfish_numbers(
        [
            [3, [2, [8, 0]]],
            [9, [5, [7, 0]]],
        ]
    )


def test_explode_6():
    assert explode(
        load_snailfish_numbers([[6, [5, [4, [3, 2]]]], [1, 2]])
    ) == load_snailfish_numbers([[6, [5, [7, 0]]], [3, 2]])


# def test_split():
#     assert split(
#         load_snailfish_numbers([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]), 0
#     ) == load_snailfish_numbers([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]])


# def test_add():
#     assert add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]) == load_snailfish_numbers(
#         [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
#     )
