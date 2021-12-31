from dataclasses import dataclass
import re


@dataclass
class Amphipod:
    id: int
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
    return Hallway([None for _ in range(len(re.search(r"#(\.+)#", hallway).group(1)))])


def load_rooms(rooms: str) -> Room:
    rooms = list(map(lambda room: room.ljust(len(rooms[0]), " "), rooms))
    rooms = list(map(lambda room: list(room[1:-1]), rooms))

    rooms = [
        (i, list(map(lambda room: room[i], rooms)))
        for i, char in enumerate(list(rooms[0]))
        if char != "#"
    ]

    rooms_out = list()

    room_types = iter([Amber, Bronze, Copper, Desert])

    id_counter = 1
    for i, room in rooms:
        occupants = []
        for amphipod_str in room:
            if amphipod_str == "A":
                occupants.append(Amber(id_counter))
            elif amphipod_str == "B":
                occupants.append(Bronze(id_counter))
            elif amphipod_str == "C":
                occupants.append(Copper(id_counter))
            else:
                occupants.append(Desert(id_counter))

            id_counter = id_counter + 1

        rooms_out.append(Room(next(room_types), i, occupants))

    return rooms_out


def load_input(input: str) -> State:
    lines = [line for line in input.split("\n") if line != ""]
    hallway = load_hallway(lines[1])
    rooms = load_rooms(lines[2:-1])

    return State(Burrow(hallway, rooms))
