from dataclasses import dataclass
import sys

HEX_MAP = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

MINIMUM_PACKET_SIZE = 6

MINIMUM_LITERAL_VALUE_PACKET_SIZE = 11

MINIMUL_OPERATOR_PACKET_SIZE = 17 + MINIMUM_LITERAL_VALUE_PACKET_SIZE


@dataclass
class Packet:
    version: int
    type_id: int


@dataclass
class LiteralValuePacket(Packet):
    value: int


@dataclass
class OperatorPacket(Packet):
    length_type_id: int
    subpackets: list[Packet]


def sum_versions(packet):
    if isinstance(packet, LiteralValuePacket):
        return packet.version

    if isinstance(packet, OperatorPacket):
        return packet.version + sum(map(sum_versions, packet.subpackets))


def pop_n(list, n):
    return "".join([list.pop(0) for _ in range(n)])


def parse_packet(binary_packet):
    version = int(pop_n(binary_packet, 3), 2)
    type_id = int(pop_n(binary_packet, 3), 2)

    if type_id == 4:
        group_prefix = 1
        binary_value = []

        while group_prefix == 1:
            group_prefix = int(binary_packet.pop(0))
            binary_value.append(pop_n(binary_packet, 4))

        value = int("".join(binary_value), 2)

        return LiteralValuePacket(version, type_id, value), binary_packet
    else:
        length_type_id = int(binary_packet.pop(0))

        is_total_length = length_type_id == 0
        if is_total_length:
            num_bits = 15
        else:
            num_bits = 11

        subpackets = []

        limit_value = 0
        limit = int(pop_n(binary_packet, num_bits), 2)

        while limit_value < limit:
            input_length = len(binary_packet)
            packet, binary_packet = parse_packet(binary_packet)
            output_length = len(binary_packet)

            subpackets.append(packet)
            if is_total_length:
                limit_value = limit_value + (input_length - output_length)
            else:
                limit_value = len(subpackets)

        return (
            OperatorPacket(version, type_id, length_type_id, subpackets),
            binary_packet,
        )


def convert_hex(hex):
    return list("".join(map(lambda c: HEX_MAP[c], hex)))


if __name__ == "__main__":
    with open(sys.argv[1], "r") as input_file:
        input = input_file.read()

    binary_packet = convert_hex(input.split("\n")[0])
    packet, binary_string = parse_packet(binary_packet)

    print(sum_versions(packet))
