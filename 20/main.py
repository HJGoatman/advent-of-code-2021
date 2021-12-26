from dataclasses import dataclass
from typing import Tuple
import numpy as np
import sys


@dataclass
class ImageEnhancementAlgorithm:
    algorithm: list[bool]


@dataclass
class Image:
    pixels: np.ndarray

    def __eq__(self, other):
        return np.all(self.pixels == other.pixels)


def load_algorithm(algorithm: str) -> ImageEnhancementAlgorithm:
    return ImageEnhancementAlgorithm([char == "#" for char in list(algorithm)])


def load_image(image: str) -> Image:
    # print(image)
    return Image(
        pixels=np.asarray(
            [
                [char == "#" for char in list(line)]
                for line in image.split("\n")
                if line != ""
            ]
        )
    )


def load_input(input_str: str) -> Tuple[ImageEnhancementAlgorithm, Image]:
    algorithm_str, image_str = input_str.split("\n\n")

    return load_algorithm(algorithm_str), load_image(image_str)


if __name__ == "__main__":
    with open(sys.argv[1]) as input_file:
        input_str = input_file.read()

    print(load_image(input_str))
