from main import (
    load_input,
    ImageEnhancementAlgorithm,
    Image,
    subpixels_to_decimal,
    get_surrounding_coordinates,
    enhance_image,
    load_image,
    enhance_image_n,
)
import numpy as np


def test_load_image():
    with open("tests/test1.txt") as input_file:
        input_str = input_file.read()

    image_enhancement_algorithm, image = load_input(input_str)

    assert image_enhancement_algorithm == ImageEnhancementAlgorithm(
        algorithm=[
            False,
            False,
            True,
            False,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            False,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            True,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            False,
            False,
            True,
            False,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            True,
            False,
            False,
            True,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            False,
            False,
            True,
            False,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            True,
            False,
            False,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            True,
        ]
    )

    assert image == Image(
        pixels=[
            (0, 0),
            (0, 3),
            (1, 0),
            (2, 0),
            (2, 1),
            (2, 4),
            (3, 2),
            (4, 2),
            (4, 3),
            (4, 4),
        ]
    )


def test_subpixels_to_decimal():
    assert (
        subpixels_to_decimal(
            [False, False, False, True, False, False, False, True, False]
        )
        == 34
    )


def test_get_surrounding_coordinates():
    assert get_surrounding_coordinates((5, 10)) == [
        (4, 9),
        (4, 10),
        (4, 11),
        (5, 9),
        (5, 10),
        (5, 11),
        (6, 9),
        (6, 10),
        (6, 11),
    ]


def test_enhance_image():
    with open("tests/test1.txt") as input_file:
        input_str = input_file.read()

    image_enhancement_algorithm, image = load_input(input_str)

    with open("tests/test3.txt") as test_file:
        test_str = test_file.read()

    assert enhance_image(image, image_enhancement_algorithm) == load_image(
        test_str, offset=(5, 5)
    )


def test_two_enhancements():
    with open("tests/test1.txt") as input_file:
        input_str = input_file.read()

    image_enhancement_algorithm, image = load_input(input_str)

    image = enhance_image(image, image_enhancement_algorithm)

    image = enhance_image(image, image_enhancement_algorithm)

    with open("tests/test4.txt") as test_file:
        test_str = test_file.read()

    assert image == load_image(test_str, offset=(5, 5))
    assert len(image.pixels) == 35


def test_enhance_50():
    with open("tests/test1.txt") as input_file:
        input_str = input_file.read()

    image_enhancement_algorithm, image = load_input(input_str)

    assert (
        len(
            enhance_image_n(
                image, image_enhancement_algorithm, 50, increase_bounds=1
            ).pixels
        )
        == 3351
    )
