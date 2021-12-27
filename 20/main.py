from dataclasses import dataclass
from typing import Tuple
from functools import reduce
import numpy as np
import sys


@dataclass
class ImageEnhancementAlgorithm:
    algorithm: list[bool]


@dataclass
class Image:
    pixels: list[(int, int)]

    def __eq__(self, other):
        return np.all(self.pixels == other.pixels)

    def __repr__(self) -> str:
        min_y, max_y, min_x, max_x = get_image_range(self)
        min_y_diff = 0 - min_y
        min_x_diff = 0 - min_x

        matrix = np.full((max_y + min_y_diff + 1, max_x + min_x_diff + 1), ".")
        for pixel in self.pixels:
            matrix[pixel[0] + min_y_diff, pixel[1] + min_x_diff] = "#"

        matrix = "\n".join(map(lambda x: "".join(x), matrix.tolist()))
        return str(matrix)


def load_algorithm(algorithm: str) -> ImageEnhancementAlgorithm:
    return ImageEnhancementAlgorithm([char == "#" for char in list(algorithm)])


def load_image(image: str, offset=(0, 0)) -> Image:
    # print(image)
    image_array = np.asarray(
        [
            [char == "#" for char in list(line)]
            for line in image.split("\n")
            if line != ""
        ]
    )
    pixels = list(zip(*np.where(image_array)))
    pixels = [(y - offset[0], x - offset[1]) for y, x in pixels]
    return Image(pixels=pixels)


def load_input(input_str: str) -> Tuple[ImageEnhancementAlgorithm, Image]:
    algorithm_str, image_str = input_str.split("\n\n")

    return load_algorithm(algorithm_str), load_image(image_str)


def subpixels_to_decimal(pixels: list[bool]) -> int:
    return int("".join(map(str, map(int, pixels))), 2)


def get_surrounding_coordinates(coordinate) -> set((int, int)):
    y, x = coordinate
    return [(i + y, j + x) for i in range(-1, 2) for j in range(-1, 2)]


def _is_light(coordinate, pixels, image_range, fill_value):
    min_y, max_y, min_x, max_x = image_range

    if (
        coordinate[0] < min_y
        or coordinate[0] > max_y
        or coordinate[1] < min_x
        or coordinate[1] > max_x
    ):
        return fill_value
    return coordinate in pixels


def is_light(pixel, pixels, algorithm, image_range, fill_value):
    return algorithm.algorithm[
        subpixels_to_decimal(
            map(
                lambda x: _is_light(x, pixels, image_range, fill_value),
                get_surrounding_coordinates(pixel),
            )
        )
    ]


def get_image_range(image: Image) -> Tuple[int, int, int, int]:
    ys = [pixel[0] for pixel in image.pixels]
    xs = [pixel[1] for pixel in image.pixels]

    return min(ys), max(ys), min(xs), max(xs)


def enhance_image(
    image: Image,
    algorithm: ImageEnhancementAlgorithm,
    fill_value: bool = False,
    increase_bounds: int = 10,
) -> Image:
    image_range = get_image_range(image)
    min_y, max_y, min_x, max_x = image_range

    min_y = min_y - increase_bounds
    max_y = max_y + increase_bounds

    min_x = min_x - increase_bounds
    max_x = max_x + increase_bounds

    pixel_space = [
        (y, x) for y in range(min_y, max_y + 1) for x in range(min_x, max_x + 1)
    ]

    return Image(
        list(
            filter(
                lambda pixel: is_light(
                    pixel, image.pixels, algorithm, image_range, fill_value
                ),
                pixel_space,
            )
        )
    )


def enhance_image_n(
    image: Image,
    algorithm: ImageEnhancementAlgorithm,
    n: int,
    fill_value: bool = False,
    increase_bounds: int = 10,
) -> Image:
    for _ in range(n):
        image = enhance_image(
            image, algorithm, fill_value=fill_value, increase_bounds=increase_bounds
        )

        if algorithm.algorithm[0]:
            fill_value = not fill_value
    return image


if __name__ == "__main__":
    with open(sys.argv[1]) as input_file:
        input_str = input_file.read()

    # algorithm, image = load_input(input_str)

    # image = enhance_image(image, algorithm, increase_bounds=10)
    # print(image)
    # image = enhance_image(image, algorithm, increase_bounds=10, fill_value=True)
    # print(image)

    # print(len(set(image.pixels)))

    algorithm, image = load_input(input_str)
    image = enhance_image_n(image, algorithm, 50, increase_bounds=1)

    print()
    print(image)
    print(len(set(image.pixels)))
