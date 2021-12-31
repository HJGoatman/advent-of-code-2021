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
class Burrow:
    hallway: list[Amphipod]
    rooms: list[Room]


@dataclass
class State:
    burrow: Burrow
    total_energy: int = 0


def load_hallway(hallway: str) -> list[Amphipod]:
    return [load_space(char) for char in re.search(r"#(\.+)#", hallway).group(1)]


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


def get_range_of_movement(hallway: list[Amphipod], room_number: int):
    blocks = [i for i, _ in filter(lambda space: space[1] != None, enumerate(hallway))]
    upper_bound = next(filter(lambda i: i > room_number, blocks), len(hallway))
    lower_bound = next(filter(lambda i: i < room_number, blocks), 0)

    return range(lower_bound, upper_bound)


def get_hallway_spaces(
    hallway: list[Amphipod], room_number: int, room_numbers: list[int]
) -> list[int]:

    return list(
        filter(
            lambda i: i not in room_numbers, get_range_of_movement(hallway, room_number)
        )
    )


def get_moves(state: State) -> list[State]:
    states = []

    burrow = state.burrow
    # Moves from Hallway into correct Room
    for i, amphipod in filter(lambda x: x[1] != None, enumerate(burrow.hallway)):
        # Is Amphipod room available?
        target_room = next(
            filter(lambda room: isinstance(amphipod, room.type), burrow.rooms)
        )

        is_room_avaliable = all(
            map(
                lambda occupant: occupant == None
                or isinstance(occupant, target_room.target),
                target_room.occupants,
            )
        )

        # Can amphipod reach their room?
        is_room_reachable = target_room.number in get_range_of_movement(
            burrow.hallway, i
        )

        if is_room_avaliable and is_room_reachable:
            space_index, _ = next(
                filter(
                    lambda space: space == None,
                    reversed(enumerate(target_room.occupants)),
                )
            )

            new_room = Room(
                target_room.type,
                target_room.number,
                occupants=[
                    amphipod if i == space_index else occupant
                    for i, occupant in enumerate(target_room.occupants)
                ],
            )
            new_burrow = Burrow(
                hallway=[
                    None if i == j else val for j, val in enumerate(burrow.hallway)
                ],
                rooms=[
                    new_room if room == target_room else room for room in burrow.rooms
                ],
            )

            energy = (space_index + 1 + abs(i - target_room.number)) * amphipod.energy
            states.append(State(new_burrow, state.total_energy + energy))

    room_numbers = [room.number for room in burrow.rooms]

    # Moves from Room to Hallway.
    for room in burrow.rooms:
        steps, moving_occupant = next(
            filter(lambda occupant: occupant[1] != None, enumerate(room.occupants))
        )

        new_room = Room(
            room.type,
            room.number,
            [None if i == steps else val for i, val in enumerate(room.occupants)],
        )

        # Get spaces occupant can move to.

        for hallway_space in get_hallway_spaces(
            burrow.hallway, room.number, room_numbers
        ):
            new_hallway = [
                moving_occupant if i == hallway_space else val
                for i, val in enumerate(burrow.hallway)
            ]
            energy = (
                steps + 1 + abs(room.number - hallway_space)
            ) * moving_occupant.energy

            states.append(
                State(
                    Burrow(
                        new_hallway,
                        [
                            new_room if new_room.number == room.number else room
                            for room in burrow.rooms
                        ],
                    ),
                    state.total_energy + energy,
                )
            )

    return states
