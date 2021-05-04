import pytest
from asn1PERser.codec.per.decoder import decode as per_decoder
from asn1PERser.classes.data.builtin.IntegerType import IntegerType
from asn1PERser.classes.types.constraint import ValueRange, MIN, MAX


def SCHEMA_not_constrained_integer():
    class MyInt(IntegerType):
        '''
        MyInt ::= INTEGER
        '''
        pass
    return MyInt


def SCHEMA_constrained_integer(lowerEndpoint_value, upperEndpoint_value, extensionMarker_value=False):
    class MyInt(IntegerType):
        '''
        MyInt ::= INTEGER (lowerEndpoint..upperEndpoint, extensionMarker)
        '''
        subtypeSpec = ValueRange(lowerEndpoint_value, upperEndpoint_value, extensionMarker=extensionMarker_value)
    return MyInt


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_not_constrained_integer(), '0100', 0),
    (SCHEMA_not_constrained_integer(), '0101', 1),
    (SCHEMA_not_constrained_integer(), '0108', 8),
    (SCHEMA_not_constrained_integer(), '010F', 15),
    (SCHEMA_not_constrained_integer(), '0110', 16),
    (SCHEMA_not_constrained_integer(), '0140', 64),
    (SCHEMA_not_constrained_integer(), '017F', 127),
    (SCHEMA_not_constrained_integer(), '020080', 128),
    (SCHEMA_not_constrained_integer(), '020081', 129),
    (SCHEMA_not_constrained_integer(), '020FA0', 4000),
    (SCHEMA_not_constrained_integer(), '027FFF', 32767),
    (SCHEMA_not_constrained_integer(), '03008000', 32768),
    (SCHEMA_not_constrained_integer(), '037FFFFF', 8388607),
    (SCHEMA_not_constrained_integer(), '0400800000', 8388608),
    (SCHEMA_not_constrained_integer(), '0401803E6F', 25181807),
])
def test_unconstrained_greater_or_equal_zero_integers_are_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_not_constrained_integer(), '04FE7FC191', -25181807),
    (SCHEMA_not_constrained_integer(), '03800000', -8388608),
    (SCHEMA_not_constrained_integer(), '03800001', -8388607),
    (SCHEMA_not_constrained_integer(), '028000', -32768),
    (SCHEMA_not_constrained_integer(), '028001', -32767),
    (SCHEMA_not_constrained_integer(), '02F060', -4000),
    (SCHEMA_not_constrained_integer(), '02FF7F', -129),
    (SCHEMA_not_constrained_integer(), '0180', -128),
    (SCHEMA_not_constrained_integer(), '0181', -127),
    (SCHEMA_not_constrained_integer(), '01C0', -64),
    (SCHEMA_not_constrained_integer(), '01F0', -16),
    (SCHEMA_not_constrained_integer(), '01F1', -15),
    (SCHEMA_not_constrained_integer(), '01F8', -8),
    (SCHEMA_not_constrained_integer(), '01FF', -1),
])
def test_unconstrained_lower_than_zero_integers_are_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-8388607, upperEndpoint_value=-8388607), '00', -8388607),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1864, upperEndpoint_value=-1864), '00', -1864),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-56, upperEndpoint_value=-56), '00', -56),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-3, upperEndpoint_value=-3), '00', -3),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=0), '00', 0),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1, upperEndpoint_value=1), '00', 1),
    (SCHEMA_constrained_integer(lowerEndpoint_value=8, upperEndpoint_value=8), '00', 8),
    (SCHEMA_constrained_integer(lowerEndpoint_value=15, upperEndpoint_value=15), '00', 15),
    (SCHEMA_constrained_integer(lowerEndpoint_value=16, upperEndpoint_value=16), '00', 16),
    (SCHEMA_constrained_integer(lowerEndpoint_value=64, upperEndpoint_value=64), '00', 64),
    (SCHEMA_constrained_integer(lowerEndpoint_value=127, upperEndpoint_value=127), '00', 127),
    (SCHEMA_constrained_integer(lowerEndpoint_value=128, upperEndpoint_value=128), '00', 128),
    (SCHEMA_constrained_integer(lowerEndpoint_value=129, upperEndpoint_value=129), '00', 129),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4000), '00', 4000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=32767, upperEndpoint_value=32767), '00', 32767),
    (SCHEMA_constrained_integer(lowerEndpoint_value=32768, upperEndpoint_value=32768), '00', 32768),
    (SCHEMA_constrained_integer(lowerEndpoint_value=8388607, upperEndpoint_value=8388607), '00', 8388607),
    (SCHEMA_constrained_integer(lowerEndpoint_value=8388608, upperEndpoint_value=8388608), '00', 8388608),
    (SCHEMA_constrained_integer(lowerEndpoint_value=25181807, upperEndpoint_value=25181807, ), '00', 25181807),
])
def test_constrained_integer_range_has_the_value_1_so_decoding_shall_be_empty(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-8388607, upperEndpoint_value=-8388606), '00', -8388607),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-8388607, upperEndpoint_value=-8388606), '80', -8388606),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1864, upperEndpoint_value=-1863), '00', -1864),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1864, upperEndpoint_value=-1863), '80', -1863),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-56, upperEndpoint_value=-55), '00', -56),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-56, upperEndpoint_value=-55), '80', -55),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-3, upperEndpoint_value=-2), '00', -3),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-3, upperEndpoint_value=-2), '80', -2),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1, upperEndpoint_value=0), '00', -1),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1, upperEndpoint_value=0), '80', 0),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1, upperEndpoint_value=2), '00', 1),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1, upperEndpoint_value=2), '80', 2),
    (SCHEMA_constrained_integer(lowerEndpoint_value=8, upperEndpoint_value=9), '00', 8),
    (SCHEMA_constrained_integer(lowerEndpoint_value=8, upperEndpoint_value=9), '80', 9),
    (SCHEMA_constrained_integer(lowerEndpoint_value=15, upperEndpoint_value=16), '00', 15),
    (SCHEMA_constrained_integer(lowerEndpoint_value=15, upperEndpoint_value=16), '80', 16),
    (SCHEMA_constrained_integer(lowerEndpoint_value=16, upperEndpoint_value=17), '00', 16),
    (SCHEMA_constrained_integer(lowerEndpoint_value=16, upperEndpoint_value=17), '80', 17),
    (SCHEMA_constrained_integer(lowerEndpoint_value=64, upperEndpoint_value=65), '00', 64),
    (SCHEMA_constrained_integer(lowerEndpoint_value=64, upperEndpoint_value=65), '80', 65),
    (SCHEMA_constrained_integer(lowerEndpoint_value=127, upperEndpoint_value=128), '00', 127),
    (SCHEMA_constrained_integer(lowerEndpoint_value=127, upperEndpoint_value=128), '80', 128),
    (SCHEMA_constrained_integer(lowerEndpoint_value=128, upperEndpoint_value=129), '00', 128),
    (SCHEMA_constrained_integer(lowerEndpoint_value=128, upperEndpoint_value=129), '80', 129),
    (SCHEMA_constrained_integer(lowerEndpoint_value=129, upperEndpoint_value=130), '00', 129),
    (SCHEMA_constrained_integer(lowerEndpoint_value=129, upperEndpoint_value=130), '80', 130),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4001), '00', 4000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4001), '80', 4001),
    (SCHEMA_constrained_integer(lowerEndpoint_value=32767, upperEndpoint_value=32768), '00', 32767),
    (SCHEMA_constrained_integer(lowerEndpoint_value=32767, upperEndpoint_value=32768), '80', 32768),
    (SCHEMA_constrained_integer(lowerEndpoint_value=32768, upperEndpoint_value=32769), '00', 32768),
    (SCHEMA_constrained_integer(lowerEndpoint_value=32768, upperEndpoint_value=32769), '80', 32769),
    (SCHEMA_constrained_integer(lowerEndpoint_value=8388607, upperEndpoint_value=8388608), '00', 8388607),
    (SCHEMA_constrained_integer(lowerEndpoint_value=8388607, upperEndpoint_value=8388608), '80', 8388608),
    (SCHEMA_constrained_integer(lowerEndpoint_value=8388608, upperEndpoint_value=8388609), '00', 8388608),
    (SCHEMA_constrained_integer(lowerEndpoint_value=8388608, upperEndpoint_value=8388609), '80', 8388609),
    (SCHEMA_constrained_integer(lowerEndpoint_value=25181807, upperEndpoint_value=25181808, ), '00', 25181807),
    (SCHEMA_constrained_integer(lowerEndpoint_value=25181807, upperEndpoint_value=25181808, ), '80', 25181808),
])
def test_constrained_integer_range_has_value_2_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-8388610, upperEndpoint_value=-8388608), '00', -8388610),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-8388610, upperEndpoint_value=-8388608), '40', -8388609),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-8388610, upperEndpoint_value=-8388608), '80', -8388608),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1, upperEndpoint_value=1), '00', -1),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1, upperEndpoint_value=1), '40', 0),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1, upperEndpoint_value=1), '80', 1),
    (SCHEMA_constrained_integer(lowerEndpoint_value=25181807, upperEndpoint_value=25181809, ), '00', 25181807),
    (SCHEMA_constrained_integer(lowerEndpoint_value=25181807, upperEndpoint_value=25181809, ), '40', 25181808),
    (SCHEMA_constrained_integer(lowerEndpoint_value=25181807, upperEndpoint_value=25181809, ), '80', 25181809),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-56, upperEndpoint_value=-53), '00', -56),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-56, upperEndpoint_value=-53), '40', -55),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-56, upperEndpoint_value=-53), '80', -54),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-56, upperEndpoint_value=-53), 'C0', -53),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4003), '00', 4000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4003), '40', 4001),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4003), '80', 4002),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4003), 'C0', 4003),
])
def test_constrained_integer_range_has_value_3_4_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-2, upperEndpoint_value=2), '00', -2),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-2, upperEndpoint_value=2), '20', -1),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-2, upperEndpoint_value=2), '40', 0),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-2, upperEndpoint_value=2), '60', 1),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-2, upperEndpoint_value=2), '80', 2),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-2, upperEndpoint_value=3), 'A0', 3),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-2, upperEndpoint_value=4), 'C0', 4),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-2, upperEndpoint_value=5), 'E0', 5),
])
def test_constrained_integer_range_has_value_5_6_7_8_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '00', -100000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '10', -99999),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '20', -99998),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '30', -99997),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '40', -99996),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '50', -99995),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '60', -99994),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '70', -99993),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '80', -99992),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99991), '90', -99991),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99990), 'A0', -99990),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99989), 'B0', -99989),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99988), 'C0', -99988),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99987), 'D0', -99987),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99986), 'E0', -99986),
    (SCHEMA_constrained_integer(lowerEndpoint_value=-100000, upperEndpoint_value=-99985), 'F0', -99985),
])
def test_constrained_integer_range_has_value_9_to_16_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-4016, upperEndpoint_value=-4000), '78', -4001),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4016), '08', 4001),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4016), '18', 4003),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4016), '28', 4005),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4016), '50', 4010),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4016), '70', 4014),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4016), '80', 4016),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4017), '88', 4017),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4020), 'A0', 4020),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4024), 'C0', 4024),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4028), 'E0', 4028),
    (SCHEMA_constrained_integer(lowerEndpoint_value=4000, upperEndpoint_value=4031), 'F8', 4031),
])
def test_constrained_integer_range_has_value_17_to_32_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1000032, upperEndpoint_value=-1000000), '7C', -1000001),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '04', 1000001),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '14', 1000005),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '24', 1000009),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '40', 1000016),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '58', 1000022),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '5C', 1000023),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '60', 1000024),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '70', 1000028),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '80', 1000032),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000040), '94', 1000037),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000045), 'B4', 1000045),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000056), 'DC', 1000055),
    (SCHEMA_constrained_integer(lowerEndpoint_value=1000000, upperEndpoint_value=1000063), 'FC', 1000063),
])
def test_constrained_integer_range_has_value_33_to_64_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-64, upperEndpoint_value=0), '72', -7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=64), '0E', 7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=64), '32', 25),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=64), '58', 44),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=64), '7A', 61),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=70), '8A', 69),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=77), '9A', 77),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=85), 'AA', 85),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=98), 'C4', 98),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=111), 'DE', 111),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=120), 'EE', 119),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=127), 'FE', 127),
])
def test_constrained_integer_range_has_value_65_to_128_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-128, upperEndpoint_value=0), '79', -7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '07', 7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '19', 25),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '2C', 44),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '3D', 61),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '45', 69),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '4D', 77),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '55', 85),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '62', 98),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '6F', 111),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '77', 119),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '7F', 127),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=128), '80', 128),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=140), '8C', 140),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=161), 'A1', 161),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=182), 'B6', 182),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=230), 'E6', 230),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=253), 'FD', 253),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=254), 'FE', 254),
])
def test_constrained_integer_range_has_value_129_to_255_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-255, upperEndpoint_value=0), 'F8', -7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '07', 7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '19', 25),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '2C', 44),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '3D', 61),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '45', 69),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '4D', 77),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '55', 85),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '62', 98),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '6F', 111),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '77', 119),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '7F', 127),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '80', 128),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), '8C', 140),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), 'A1', 161),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), 'B6', 182),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), 'E6', 230),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), 'FD', 253),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), 'FE', 254),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255), 'FF', 255),
])
def test_constrained_integer_range_has_value_256_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-256, upperEndpoint_value=0), '00F9', -7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '0007', 7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '0019', 25),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '002C', 44),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '003D', 61),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '0045', 69),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '004D', 77),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '0055', 85),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '0062', 98),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '006F', 111),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '0077', 119),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '007F', 127),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '0080', 128),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '008C', 140),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '00A1', 161),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '00B6', 182),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '00E6', 230),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '00FD', 253),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '00FE', 254),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '00FF', 255),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=256), '0100', 256),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=511), '01FF', 511),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=512), '0200', 512),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1023), '03FF', 1023),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1024), '0400', 1024),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1024), '0400', 1024),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=8191), '1FFF', 8191),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=8192), '2000', 8192),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=32768), '7FFE', 32766),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=32768), '7FFF', 32767),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=32768), '8000', 32768),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=44321), 'AD21', 44321),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=60000), 'D903', 55555),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=65535), 'EA60', 60000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=65535), 'FFFE', 65534),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=65535), 'FFFF', 65535),
])
def test_constrained_integer_range_has_value_257_to_65536_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=-1234567, upperEndpoint_value=0), '80114FE7', -100000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '0007', 7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '0019', 25),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '002C', 44),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '003D', 61),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '0045', 69),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '004D', 77),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '0055', 85),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '0062', 98),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '006F', 111),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '0077', 119),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '007F', 127),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '0080', 128),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '008C', 140),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '00A1', 161),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '00B6', 182),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '00E6', 230),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '00FD', 253),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '00FE', 254),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '00FF', 255),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '400100', 256),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '4001FF', 511),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '400200', 512),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '4003FF', 1023),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '400400', 1024),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '400400', 1024),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '401FFF', 8191),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '402000', 8192),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '407FFE', 32766),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '407FFF', 32767),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '408000', 32768),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '40AD21', 44321),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '40D903', 55555),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '40EA60', 60000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '40FFFE', 65534),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '40FFFF', 65535),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '80010000', 65536),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1234567), '800186A0', 100000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=256, upperEndpoint_value=1234567), '0000', 256),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=4294967295), '0064', 100),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=4294967295), '00FF', 255),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=4294967295), '400100', 256),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=4294967295), '800186A0', 100000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=4294967295), 'C005F5E100', 100000000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=4294967295), 'C0FFFFFFFE', 4294967294),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=4294967295), 'C0FFFFFFFF', 4294967295),
])
def test_constrained_integer_range_has_value_greater_than_65536_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '0107', 7),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '0119', 25),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '012C', 44),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '013D', 61),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '0145', 69),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '014D', 77),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '0155', 85),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '0162', 98),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '016F', 111),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '0177', 119),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '017F', 127),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '0180', 128),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '018C', 140),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '01A1', 161),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '01B6', 182),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '01E6', 230),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '01FD', 253),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '01FE', 254),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '01FF', 255),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '020100', 256),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '0201FF', 511),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '020200', 512),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '0203FF', 1023),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '020400', 1024),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '020400', 1024),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '021FFF', 8191),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '022000', 8192),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '027FFE', 32766),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '027FFF', 32767),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '028000', 32768),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '02AD21', 44321),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '02D903', 55555),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '02EA60', 60000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '02FFFE', 65534),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '02FFFF', 65535),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '03010000', 65536),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=MAX), '030186A0', 100000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=256, upperEndpoint_value=MAX), '0100', 256)
])
def test_semi_constrained_integer_is_encoded_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '60', 3),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=120, extensionMarker_value=True), '03', 3),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255, extensionMarker_value=True), '0003', 3),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=10000, extensionMarker_value=True), '000003', 3),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=100000, extensionMarker_value=True), '0003', 3),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=255, extensionMarker_value=True), '00FE', 254),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=10000, extensionMarker_value=True), '0000FE', 254),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=100000, extensionMarker_value=True), '00FE', 254),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=10000, extensionMarker_value=True), '0003FF', 1023),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=100000, extensionMarker_value=True), '2003FF', 1023),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=100000, extensionMarker_value=True), '207FFE', 32766),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1000000, extensionMarker_value=True), '20FFFF', 65535),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=1000000, extensionMarker_value=True), '400186A0', 100000),
])
def test_extension_marker_is_present_and_value_is_within_extension_root_integer_is_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '800104', 4),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '80030186A0', 100000),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '8001FC', -4),
    (SCHEMA_constrained_integer(lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '8003FE7960', -100000),
])
def test_extension_marker_is_present_and_values_in_not_within_extension_root_integer_is_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value
