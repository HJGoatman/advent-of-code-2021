from main import (
    explode,
    load_snailfish_numbers,
    get_leaves,
    RegularNumber,
    split,
    add,
    add_file,
    get_magnitude,
    Pair,
    leaves_to_tree,
)

numbers_1 = load_snailfish_numbers([[[[[9, 8], 1], 2], 3], 4])


def test_get_leaves():
    assert get_leaves(numbers_1) == [
        RegularNumber(5, 9),
        RegularNumber(5, 8),
        RegularNumber(4, 1),
        RegularNumber(3, 2),
        RegularNumber(2, 3),
        RegularNumber(1, 4),
    ]


# def test_get_exploded_left():
#     assert get_exploded_value(numbers_1, is_right=False) == RegularNumber(9)


# def test_has_right_number_1():
#     assert has_regular_number(load_snailfish_numbers([0, 1]), 2, is_right=True) == True


# def test_has_right_number_2():
#     assert (
#         has_regular_number(load_snailfish_numbers([6, [5, [7, 0]]]), 2, is_right=True)
#         == False
#     )


def test_explode_1():
    assert explode(get_leaves(numbers_1)) == get_leaves(
        load_snailfish_numbers([[[[0, 9], 2], 3], 4])
    )


def test_explode_2():
    assert explode(
        get_leaves(load_snailfish_numbers([7, [6, [5, [4, [3, 2]]]]]))
    ) == get_leaves(load_snailfish_numbers([7, [6, [5, [7, 0]]]]))


def test_explode_3():
    assert explode(
        get_leaves(load_snailfish_numbers([[6, [5, [4, [3, 2]]]], 1]))
    ) == get_leaves(load_snailfish_numbers([[6, [5, [7, 0]]], 3]))


def test_explode_4():
    assert explode(
        get_leaves(
            load_snailfish_numbers([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
        )
    ) == get_leaves(load_snailfish_numbers([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]))


def test_explode_5():
    assert explode(
        get_leaves(load_snailfish_numbers([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]))
    ) == get_leaves(
        load_snailfish_numbers(
            [
                [3, [2, [8, 0]]],
                [9, [5, [7, 0]]],
            ]
        )
    )


def test_explode_6():
    assert explode(
        get_leaves(load_snailfish_numbers([[6, [5, [4, [3, 2]]]], [1, 2]]))
    ) == get_leaves(load_snailfish_numbers([[6, [5, [7, 0]]], [3, 2]]))


def test_split_1():
    assert split([RegularNumber(0, 10)]) == [RegularNumber(1, 5), RegularNumber(1, 5)]


def test_split_2():
    assert split([RegularNumber(0, 11)]) == [RegularNumber(1, 5), RegularNumber(1, 6)]


def test_split_3():
    assert split([RegularNumber(0, 12)]) == [RegularNumber(1, 6), RegularNumber(1, 6)]


def test_add():
    assert (
        add(
            get_leaves(load_snailfish_numbers([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])),
            get_leaves(load_snailfish_numbers([1, 1])),
        )
        == get_leaves(load_snailfish_numbers([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]))
    )


def test_reduce_1():
    input_str = "[1,1]\n[2,2]\n[3,3]\n[4,4]\n"

    assert add_file(input_str) == get_leaves(
        load_snailfish_numbers([[[[1, 1], [2, 2]], [3, 3]], [4, 4]])
    )


def test_reduce_2():
    input_str = "[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n"
    assert add_file(input_str) == get_leaves(
        load_snailfish_numbers([[[[3, 0], [5, 3]], [4, 4]], [5, 5]])
    )


def test_reduce_3():
    input_str = "[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]\n"
    assert add_file(input_str) == get_leaves(
        load_snailfish_numbers([[[[5, 0], [7, 4]], [5, 5]], [6, 6]])
    )


def test_large_input():
    with open("test.txt") as input_file:
        input = input_file.read()

    assert add_file(input) == get_leaves(
        load_snailfish_numbers(
            [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
        )
    )


def test_magnitude_1():
    assert get_magnitude(Pair(0, RegularNumber(0, 9), RegularNumber(0, 1))) == 29


def test_magnitude_2():
    assert get_magnitude(Pair(0, RegularNumber(0, 1), RegularNumber(0, 9))) == 21


def test_magnitude_3():
    assert get_magnitude(load_snailfish_numbers([[1, 2], [[3, 4], 5]])) == 143


def test_magnitude_4():
    assert (
        get_magnitude(load_snailfish_numbers([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]))
        == 1384
    )


def test_magnitude_5():
    assert (
        get_magnitude(load_snailfish_numbers([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]))
        == 445
    )


def test_magnitude_6():
    assert (
        get_magnitude(load_snailfish_numbers([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]))
        == 791
    )


def test_magnitude_7():
    assert (
        get_magnitude(load_snailfish_numbers([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]))
        == 1137
    )


def test_magnitude_8():
    assert (
        get_magnitude(
            load_snailfish_numbers(
                [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
            )
        )
        == 3488
    )


def test_leaves_to_tree_1():
    tree = load_snailfish_numbers(
        [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]
    )
    assert leaves_to_tree(get_leaves(tree)) == tree


def test_leaves_to_tree_2():
    tree = load_snailfish_numbers([[6, [5, [4, [3, 2]]]], [1, 2]])
    assert leaves_to_tree(get_leaves(tree)) == tree


def test_integration():
    with open("test2.txt") as input_file:
        input = input_file.read()

    file_add_out = add_file(input)
    assert file_add_out == get_leaves(
        load_snailfish_numbers(
            [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]
        )
    )

    assert get_magnitude(leaves_to_tree(file_add_out)) == 4140
