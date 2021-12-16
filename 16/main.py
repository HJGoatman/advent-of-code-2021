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


class Packet:
    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id

    @staticmethod
    def from_str(packet_str):
        binary_packet = "".join(map(lambda c: HEX_MAP[c], packet_str))
        return Packet.from_binary(binary_packet)

    @staticmethod
    def from_binary(binary_packet):
        if len(binary_packet) < MINIMUM_PACKET_SIZE:
            raise IncompletePacketError

        version = int(binary_packet[:3], 2)
        type_id = int(binary_packet[3:6], 2)

        if type_id == 4:
            if len(binary_packet) < MINIMUM_LITERAL_VALUE_PACKET_SIZE:
                raise IncompletePacketError

            return LiteralValuePacket(
                version, type_id, LiteralValuePacket.get_value(binary_packet[6:])
            )
        else:
            if len(binary_packet) < MINIMUL_OPERATOR_PACKET_SIZE:
                raise IncompletePacketError
            length_type_id = OperatorPacket.read_length_type_id(binary_packet[6])
            return OperatorPacket(
                version,
                type_id,
                length_type_id,
                OperatorPacket.read_subpackets(length_type_id, binary_packet[7:]),
            )


class IncompletePacketError(Exception):
    pass


class LiteralValuePacket(Packet):
    def __init__(self, version, type_id, value):
        super().__init__(version, type_id)
        self.value = value

    def get_value(packet_binary):
        # while (len(packet_binary) % 5) != 0:
        #     packet_binary = "0" + packet_binary

        group_prefix = 1
        binary_value = []
        i = 0

        while group_prefix == 1:
            if i + 5 > len(packet_binary):
                raise IncompletePacketError

            group_prefix = int(packet_binary[i])
            binary_value.append(packet_binary[i + 1 : i + 5])

            i = i + 5

        return int("".join(binary_value), 2)

    def __repr__(self) -> str:
        return f"LiteralValuePacket({self.value})"


class OperatorPacket(Packet):
    def __init__(self, version, type_id, length_type_id, subpackets):
        super().__init__(version, type_id)
        self.length_type_id = length_type_id
        self.subpackets = subpackets

    @staticmethod
    def read_subpackets(length_type_id, packet_str):
        cursor = 0

        is_total_length = length_type_id == 0
        if is_total_length:
            cursor = 15
        else:
            cursor = 11

        subpackets = []

        limit_value = 0
        limit = int(packet_str[:cursor], 2)
        potential_packet_size = 0

        while limit_value <= limit:
            if (cursor + potential_packet_size) > len(packet_str):
                raise IncompletePacketError

            try:
                packet = Packet.from_binary(
                    packet_str[cursor : cursor + potential_packet_size]
                )
            except IncompletePacketError:
                potential_packet_size = potential_packet_size + 1
                continue

            subpackets.append(packet)
            if is_total_length:
                limit_value = cursor + potential_packet_size
            else:
                limit_value = len(subpackets) + 1

            cursor = cursor + potential_packet_size
            potential_packet_size = 0

        return subpackets

    @staticmethod
    def read_length_type_id(length_type_id_str):
        return int(length_type_id_str)

    def __repr__(self) -> str:
        return f"OperatorPacket({self.subpackets})"


def sum_versions(packet):
    if isinstance(packet, LiteralValuePacket):
        return packet.version

    if isinstance(packet, OperatorPacket):
        return packet.version + sum(map(sum_versions, packet.subpackets))


if __name__ == "__main__":
    with open(sys.argv[1], "r") as input_file:
        input = input_file.read()

    packet = Packet.from_str(input.split("\n")[0])

    print(packet)
