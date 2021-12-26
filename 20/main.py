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


def load_algorithm(algorithm: str) -> ImageEnhancementAlgorithm:
    return ImageEnhancementAlgorithm([char == "#" for char in list(algorithm)])


def load_image(image: str) -> Image:
    # print(image)
    image_array = np.asarray(
        [
            [char == "#" for char in list(line)]
            for line in image.split("\n")
            if line != ""
        ]
    )
    return Image(pixels=set(zip(*np.where(image_array))))


def load_input(input_str: str) -> Tuple[ImageEnhancementAlgorithm, Image]:
    algorithm_str, image_str = input_str.split("\n\n")

    return load_algorithm(algorithm_str), load_image(image_str)


def subpixels_to_decimal(pixels: list[bool]) -> int:
    return int("".join(map(str, map(int, pixels))), 2)


def get_surrounding_coordinates(coordinate) -> set((int, int)):
    y, x = coordinate
    return [(i + y, j + x) for i in range(-1, 2) for j in range(-1, 2)]


def is_light(pixel, pixels, algorithm):
    return algorithm.algorithm[
        subpixels_to_decimal(
            map(lambda x: x in pixels, get_surrounding_coordinates(pixel))
        )
    ]


def enhance_image(image: Image, algorithm: ImageEnhancementAlgorithm) -> Image:
    ys = [pixel[0] for pixel in image.pixels]
    min_y = min(ys) - 1
    max_y = max(ys) + 1

    xs = [pixel[1] for pixel in image.pixels]
    min_x = min(xs) - 1
    max_x = max(xs) + 1

    pixel_space = [
        (y, x) for y in range(min_y, max_y + 1) for x in range(min_x, max_x + 1)
    ]

    return Image(
        list(
            filter(lambda pixel: is_light(pixel, image.pixels, algorithm), pixel_space)
        )
    )


if __name__ == "__main__":
    with open(sys.argv[1]) as input_file:
        input_str = input_file.read()

    print(load_image(input_str))
