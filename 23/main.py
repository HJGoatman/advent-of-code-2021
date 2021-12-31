from dataclasses import dataclass
import re


@dataclass
class Amphipod:
    energy: int


@dataclass
class Amber(Amphipod):
    energy: int = 1


@dataclass
class Bronze(Amphipod):
    energy: int = 10


@dataclass
class Copper(Amphipod):
    energy: int = 100


@dataclass
class Desert(Amphipod):
    energy: int = 1000


@dataclass
class Room:
    type: type
    number: int
    occupants: list[Amphipod]


@dataclass
class Hallway:
    hallway: list[Amphipod]


@dataclass
class Burrow:
    hallway: Hallway
    rooms: list[Room]


@dataclass
class State:
    burrow: Burrow
    total_energy: int = 0


def load_hallway(hallway: str) -> Hallway:
    return Hallway(
        [load_space(char) for char in re.search(r"#(\.+)#", hallway).group(1)]
    )


def load_space(char: str) -> Amphipod | None:
    if char == "A":
        return Amber()
    elif char == "B":
        return Bronze()
    elif char == "C":
        return Copper()
    elif char == "D":
        return Desert()
    else:
        return None


def load_rooms(rooms: str) -> Room:
    rooms = list(map(lambda room: room.ljust(len(rooms[0]), " "), rooms))
    rooms = list(map(lambda room: list(room[1:-1]), rooms))

    rooms = [
        (i, list(map(lambda room: room[i], rooms)))
        for i, char in enumerate(list(rooms[0]))
        if char != "#"
    ]

    room_types = iter([Amber, Bronze, Copper, Desert])

    return [Room(next(room_types), i, list(map(load_space, room))) for i, room in rooms]


def load_input(input: str) -> State:
    lines = [line for line in input.split("\n") if line != ""]
    hallway = load_hallway(lines[1])
    rooms = load_rooms(lines[2:-1])

    return State(Burrow(hallway, rooms))
