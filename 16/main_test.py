from main import parse_packet, sum_versions, convert_hex, OperatorPacket


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
