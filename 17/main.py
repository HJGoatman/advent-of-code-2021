import sys
from dataclasses import dataclass
from math import sqrt, ceil


@dataclass
class TargetArea:
    x1: int
    x2: int
    y1: int
    y2: int


def will_hit(x_current, y_current, x_v, y_v):
    if x_v < 0:
        x_v = 0

    if (x_current > max_x_target) or (y_current < min_y_target):
        return False
    if (
        (x_current >= min_x_target)
        and (y_current <= max_y_target)
        and (x_current <= max_x_target)
        and (y_current >= min_y_target)
    ):
        return True

    return will_hit(x_current + x_v, y_current + y_v, x_v - 1, y_v - 1)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as input_file:
        input = input_file.read()

    target_area_values = list(
        map(
            lambda x: list(map(int, x[2:].split(".."))),
            input.split("\n")[0][13:].split(", "),
        )
    )

    target_area_values = target_area_values[0] + target_area_values[1]

    target_area = TargetArea(*target_area_values)

    print(target_area)
    print()

    min_x_target = min(target_area.x1, target_area.x2)
    max_x_target = max(target_area.x1, target_area.x2)

    min_y_target = min(target_area.y1, target_area.y2)
    max_y_target = max(target_area.y1, target_area.y2)

    n = abs(min_y_target + 1)
    max_height = int((n * (n + 1)) / 2)
    print("Maximum Height:", max_height)

    c = -2 * min_x_target

    min_x_v = ceil((-1 + sqrt(1 - 4 * c)) / 2)
    max_x_v = max_x_target

    min_y_v = min_y_target
    max_y_v = abs(min_y_v)

    print(
        "Number of successful probes:",
        len(
            [
                (x_v, y_v)
                for x_v in range(min_x_v, max_x_v + 1)
                for y_v in range(min_y_v, max_y_v)
                if will_hit(0, 0, x_v, y_v)
            ]
        ),
    )
