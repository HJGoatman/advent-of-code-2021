from main import (
    parse_packet,
    sum_versions,
    convert_hex,
    OperatorPacket,
    evaluate_packet,
)


def test_1():
    packet, _ = parse_packet(convert_hex("D2FE28"))
    assert packet.value == 2021


def test_2():
    packet, _ = parse_packet(convert_hex("38006F45291200"))
    assert packet.version == 1
    assert packet.type_id == 6
    assert isinstance(packet, OperatorPacket)
    assert len(packet.subpackets) == 2
    assert packet.subpackets[0].value == 10
    assert packet.subpackets[1].value == 20


def test_3():
    packet, _ = parse_packet(convert_hex("EE00D40C823060"))
    assert packet.version == 7
    assert packet.type_id == 3
    assert isinstance(packet, OperatorPacket)
    assert len(packet.subpackets) == 3
    assert packet.subpackets[0].value == 1
    assert packet.subpackets[1].value == 2
    assert packet.subpackets[2].value == 3


def test_4():
    packet, _ = parse_packet(convert_hex("8A004A801A8002F478"))
    assert sum_versions(packet) == 16


def test_5():
    packet, _ = parse_packet(convert_hex("620080001611562C8802118E34"))
    assert sum_versions(packet) == 12


def test_6():
    packet, _ = parse_packet(convert_hex("C0015000016115A2E0802F182340"))
    assert sum_versions(packet) == 23


def test_7():
    packet, _ = parse_packet(convert_hex("A0016C880162017C3686B18A3D4780"))
    assert sum_versions(packet) == 31


def eval_hex(hex):
    packet, _ = parse_packet(convert_hex(hex))
    return evaluate_packet(packet)


def test_sum_eval():
    assert eval_hex("C200B40A82") == 3


def test_product_eval():
    assert eval_hex("04005AC33890") == 54


def test_minimum_eval():
    assert eval_hex("880086C3E88112") == 7


def test_maximum_eval():
    assert eval_hex("CE00C43D881120") == 9


def test_less_than_eval():
    assert eval_hex("D8005AC2A8F0") == 1


def test_greater_than_eval():
    assert eval_hex("F600BC2D8F") == 0


def test_not_equal_eval():
    assert eval_hex("9C005AC2F8F0") == 0


def test_multi_eval():
    assert eval_hex("9C0141080250320F1802104A08") == 1
