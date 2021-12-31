from main import State, Burrow, Room, Amber, Bronze, Copper, Desert

possible_moves_1 = [
    State(
        Burrow(
            [Bronze(), None, None, None, None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[None, Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=30,
    ),
    State(
        Burrow(
            [None, Bronze(), None, None, None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[None, Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=20,
    ),
    State(
        Burrow(
            [None, None, None, Bronze(), None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[None, Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=20,
    ),
    State(
        Burrow(
            [None, None, None, None, None, Bronze(), None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[None, Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=40,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, Bronze(), None, None, None],
            [
                Room(type=Amber, number=2, occupants=[None, Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=60,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, None, None, Bronze(), None],
            [
                Room(type=Amber, number=2, occupants=[None, Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=80,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, None, None, None, Bronze()],
            [
                Room(type=Amber, number=2, occupants=[None, Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=90,
    ),
    State(
        Burrow(
            [Copper(), None, None, None, None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[None, Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=500,
    ),
    State(
        Burrow(
            [None, Copper(), None, None, None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[None, Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=400,
    ),
    State(
        Burrow(
            [None, None, None, Copper(), None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[None, Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=200,
    ),
    State(
        Burrow(
            [None, None, None, None, None, Copper(), None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[None, Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=200,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, Copper(), None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[None, Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=400,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, None, None, Copper(), None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[None, Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=600,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, None, None, None, Copper()],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[None, Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=700,
    ),
    State(
        Burrow(
            [Bronze(), None, None, None, None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[None, Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=70,
    ),
    State(
        Burrow(
            [None, Bronze(), None, None, None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[None, Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=60,
    ),
    State(
        Burrow(
            [None, None, None, Bronze(), None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[None, Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=40,
    ),
    State(
        Burrow(
            [None, None, None, None, None, Bronze(), None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[None, Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=20,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, Bronze(), None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[None, Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=20,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, None, None, Bronze(), None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[None, Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=40,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, None, None, None, Bronze()],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[None, Copper()]),
                Room(type=Desert, number=8, occupants=[Desert(), Amber()]),
            ],
        ),
        total_energy=50,
    ),
    State(
        Burrow(
            [Desert(), None, None, None, None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[None, Amber()]),
            ],
        ),
        total_energy=9000,
    ),
    State(
        Burrow(
            [None, Desert(), None, None, None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[None, Amber()]),
            ],
        ),
        total_energy=8000,
    ),
    State(
        Burrow(
            [None, None, None, Desert(), None, None, None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[None, Amber()]),
            ],
        ),
        total_energy=6000,
    ),
    State(
        Burrow(
            [None, None, None, None, None, Desert(), None, None, None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[None, Amber()]),
            ],
        ),
        total_energy=4000,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, Desert(), None, None, None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[None, Amber()]),
            ],
        ),
        total_energy=2000,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, None, None, Desert(), None],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[None, Amber()]),
            ],
        ),
        total_energy=2000,
    ),
    State(
        Burrow(
            [None, None, None, None, None, None, None, None, None, None, Desert()],
            [
                Room(type=Amber, number=2, occupants=[Bronze(), Amber()]),
                Room(type=Bronze, number=4, occupants=[Copper(), Desert()]),
                Room(type=Copper, number=6, occupants=[Bronze(), Copper()]),
                Room(type=Desert, number=8, occupants=[None, Amber()]),
            ],
        ),
        total_energy=3000,
    ),
]

