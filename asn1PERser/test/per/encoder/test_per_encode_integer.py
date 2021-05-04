import pytest
from asn1PERser.codec.per.encoder import encode as per_encoder
from asn1PERser.classes.data.builtin.IntegerType import IntegerType
from asn1PERser.classes.types.constraint import ValueRange, MIN, MAX


def SCHEMA_not_contrained_integer(value):
    class MyInt(IntegerType):
        pass
    return MyInt(value)


def SCHEMA_constrained_integer(value, lowerEndpoint_value, upperEndpoint_value, extensionMarker_value=False):
    class MyInt(IntegerType):
        subtypeSpec = ValueRange(lowerEndpoint_value, upperEndpoint_value, extensionMarker=extensionMarker_value)
    return MyInt(value)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_not_contrained_integer(0), '0100'),
    (SCHEMA_not_contrained_integer(1), '0101'),
    (SCHEMA_not_contrained_integer(8), '0108'),
    (SCHEMA_not_contrained_integer(15), '010F'),
    (SCHEMA_not_contrained_integer(16), '0110'),
    (SCHEMA_not_contrained_integer(64), '0140'),
    (SCHEMA_not_contrained_integer(127), '017F'),
    (SCHEMA_not_contrained_integer(128), '020080'),
    (SCHEMA_not_contrained_integer(129), '020081'),
    (SCHEMA_not_contrained_integer(4000), '020FA0'),
    (SCHEMA_not_contrained_integer(32767), '027FFF'),
    (SCHEMA_not_contrained_integer(32768), '03008000'),
    (SCHEMA_not_contrained_integer(8388607), '037FFFFF'),
    (SCHEMA_not_contrained_integer(8388608), '0400800000'),
    (SCHEMA_not_contrained_integer(25181807), '0401803E6F'),
])
def test_unconstrained_greater_or_equal_zero_integers_are_encoded(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_not_contrained_integer(-25181807), '04FE7FC191'),
    (SCHEMA_not_contrained_integer(-8388608), '03800000'),
    (SCHEMA_not_contrained_integer(-8388607), '03800001'),
    (SCHEMA_not_contrained_integer(-32768), '028000'),
    (SCHEMA_not_contrained_integer(-32767), '028001'),
    (SCHEMA_not_contrained_integer(-4000), '02F060'),
    (SCHEMA_not_contrained_integer(-129), '02FF7F'),
    (SCHEMA_not_contrained_integer(-128), '0180'),
    (SCHEMA_not_contrained_integer(-127), '0181'),
    (SCHEMA_not_contrained_integer(-64), '01C0'),
    (SCHEMA_not_contrained_integer(-16), '01F0'),
    (SCHEMA_not_contrained_integer(-15), '01F1'),
    (SCHEMA_not_contrained_integer(-8), '01F8'),
    (SCHEMA_not_contrained_integer(-1), '01FF'),
])
def test_unconstrained_lower_than_zero_integers_are_encoded(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-8388607, lowerEndpoint_value=-8388607, upperEndpoint_value=-8388607), '00'),
    (SCHEMA_constrained_integer(-1864, lowerEndpoint_value=-1864, upperEndpoint_value=-1864), '00'),
    (SCHEMA_constrained_integer(-56, lowerEndpoint_value=-56, upperEndpoint_value=-56), '00'),
    (SCHEMA_constrained_integer(-3, lowerEndpoint_value=-3, upperEndpoint_value=-3), '00'),
    (SCHEMA_constrained_integer(0, lowerEndpoint_value=0, upperEndpoint_value=0), '00'),
    (SCHEMA_constrained_integer(1, lowerEndpoint_value=1, upperEndpoint_value=1), '00'),
    (SCHEMA_constrained_integer(8, lowerEndpoint_value=8, upperEndpoint_value=8), '00'),
    (SCHEMA_constrained_integer(15, lowerEndpoint_value=15, upperEndpoint_value=15), '00'),
    (SCHEMA_constrained_integer(16, lowerEndpoint_value=16, upperEndpoint_value=16), '00'),
    (SCHEMA_constrained_integer(64, lowerEndpoint_value=64, upperEndpoint_value=64), '00'),
    (SCHEMA_constrained_integer(127, lowerEndpoint_value=127, upperEndpoint_value=127), '00'),
    (SCHEMA_constrained_integer(128, lowerEndpoint_value=128, upperEndpoint_value=128), '00'),
    (SCHEMA_constrained_integer(129, lowerEndpoint_value=129, upperEndpoint_value=129), '00'),
    (SCHEMA_constrained_integer(4000, lowerEndpoint_value=4000, upperEndpoint_value=4000), '00'),
    (SCHEMA_constrained_integer(32767, lowerEndpoint_value=32767, upperEndpoint_value=32767), '00'),
    (SCHEMA_constrained_integer(32768, lowerEndpoint_value=32768, upperEndpoint_value=32768), '00'),
    (SCHEMA_constrained_integer(8388607, lowerEndpoint_value=8388607, upperEndpoint_value=8388607), '00'),
    (SCHEMA_constrained_integer(8388608, lowerEndpoint_value=8388608, upperEndpoint_value=8388608), '00'),
    (SCHEMA_constrained_integer(25181807, lowerEndpoint_value=25181807, upperEndpoint_value=25181807, ), '00'),
])
def test_constrained_integer_range_has_the_value_1_so_encoding_bit_field_shall_be_empty(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-8388607, lowerEndpoint_value=-8388607, upperEndpoint_value=-8388606), '00'),
    (SCHEMA_constrained_integer(-8388606, lowerEndpoint_value=-8388607, upperEndpoint_value=-8388606), '80'),
    (SCHEMA_constrained_integer(-1864, lowerEndpoint_value=-1864, upperEndpoint_value=-1863), '00'),
    (SCHEMA_constrained_integer(-1863, lowerEndpoint_value=-1864, upperEndpoint_value=-1863), '80'),
    (SCHEMA_constrained_integer(-56, lowerEndpoint_value=-56, upperEndpoint_value=-55), '00'),
    (SCHEMA_constrained_integer(-55, lowerEndpoint_value=-56, upperEndpoint_value=-55), '80'),
    (SCHEMA_constrained_integer(-3, lowerEndpoint_value=-3, upperEndpoint_value=-2), '00'),
    (SCHEMA_constrained_integer(-2, lowerEndpoint_value=-3, upperEndpoint_value=-2), '80'),
    (SCHEMA_constrained_integer(-1, lowerEndpoint_value=-1, upperEndpoint_value=0), '00'),
    (SCHEMA_constrained_integer(0, lowerEndpoint_value=-1, upperEndpoint_value=0), '80'),
    (SCHEMA_constrained_integer(1, lowerEndpoint_value=1, upperEndpoint_value=2), '00'),
    (SCHEMA_constrained_integer(2, lowerEndpoint_value=1, upperEndpoint_value=2), '80'),
    (SCHEMA_constrained_integer(8, lowerEndpoint_value=8, upperEndpoint_value=9), '00'),
    (SCHEMA_constrained_integer(9, lowerEndpoint_value=8, upperEndpoint_value=9), '80'),
    (SCHEMA_constrained_integer(15, lowerEndpoint_value=15, upperEndpoint_value=16), '00'),
    (SCHEMA_constrained_integer(16, lowerEndpoint_value=15, upperEndpoint_value=16), '80'),
    (SCHEMA_constrained_integer(16, lowerEndpoint_value=16, upperEndpoint_value=17), '00'),
    (SCHEMA_constrained_integer(17, lowerEndpoint_value=16, upperEndpoint_value=17), '80'),
    (SCHEMA_constrained_integer(64, lowerEndpoint_value=64, upperEndpoint_value=65), '00'),
    (SCHEMA_constrained_integer(65, lowerEndpoint_value=64, upperEndpoint_value=65), '80'),
    (SCHEMA_constrained_integer(127, lowerEndpoint_value=127, upperEndpoint_value=128), '00'),
    (SCHEMA_constrained_integer(128, lowerEndpoint_value=127, upperEndpoint_value=128), '80'),
    (SCHEMA_constrained_integer(128, lowerEndpoint_value=128, upperEndpoint_value=129), '00'),
    (SCHEMA_constrained_integer(129, lowerEndpoint_value=128, upperEndpoint_value=129), '80'),
    (SCHEMA_constrained_integer(129, lowerEndpoint_value=129, upperEndpoint_value=130), '00'),
    (SCHEMA_constrained_integer(130, lowerEndpoint_value=129, upperEndpoint_value=130), '80'),
    (SCHEMA_constrained_integer(4000, lowerEndpoint_value=4000, upperEndpoint_value=4001), '00'),
    (SCHEMA_constrained_integer(4001, lowerEndpoint_value=4000, upperEndpoint_value=4001), '80'),
    (SCHEMA_constrained_integer(32767, lowerEndpoint_value=32767, upperEndpoint_value=32768), '00'),
    (SCHEMA_constrained_integer(32768, lowerEndpoint_value=32767, upperEndpoint_value=32768), '80'),
    (SCHEMA_constrained_integer(32768, lowerEndpoint_value=32768, upperEndpoint_value=32769), '00'),
    (SCHEMA_constrained_integer(32769, lowerEndpoint_value=32768, upperEndpoint_value=32769), '80'),
    (SCHEMA_constrained_integer(8388607, lowerEndpoint_value=8388607, upperEndpoint_value=8388608), '00'),
    (SCHEMA_constrained_integer(8388608, lowerEndpoint_value=8388607, upperEndpoint_value=8388608), '80'),
    (SCHEMA_constrained_integer(8388608, lowerEndpoint_value=8388608, upperEndpoint_value=8388609), '00'),
    (SCHEMA_constrained_integer(8388609, lowerEndpoint_value=8388608, upperEndpoint_value=8388609), '80'),
    (SCHEMA_constrained_integer(25181807, lowerEndpoint_value=25181807, upperEndpoint_value=25181808, ), '00'),
    (SCHEMA_constrained_integer(25181808, lowerEndpoint_value=25181807, upperEndpoint_value=25181808, ), '80'),
])
def test_constrained_integer_range_has_value_2(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-8388610, lowerEndpoint_value=-8388610, upperEndpoint_value=-8388608), '00'),
    (SCHEMA_constrained_integer(-8388609, lowerEndpoint_value=-8388610, upperEndpoint_value=-8388608), '40'),
    (SCHEMA_constrained_integer(-8388608, lowerEndpoint_value=-8388610, upperEndpoint_value=-8388608), '80'),
    (SCHEMA_constrained_integer(-1, lowerEndpoint_value=-1, upperEndpoint_value=1), '00'),
    (SCHEMA_constrained_integer(0, lowerEndpoint_value=-1, upperEndpoint_value=1), '40'),
    (SCHEMA_constrained_integer(1, lowerEndpoint_value=-1, upperEndpoint_value=1), '80'),
    (SCHEMA_constrained_integer(25181807, lowerEndpoint_value=25181807, upperEndpoint_value=25181809, ), '00'),
    (SCHEMA_constrained_integer(25181808, lowerEndpoint_value=25181807, upperEndpoint_value=25181809, ), '40'),
    (SCHEMA_constrained_integer(25181809, lowerEndpoint_value=25181807, upperEndpoint_value=25181809, ), '80'),
    (SCHEMA_constrained_integer(-56, lowerEndpoint_value=-56, upperEndpoint_value=-53), '00'),
    (SCHEMA_constrained_integer(-55, lowerEndpoint_value=-56, upperEndpoint_value=-53), '40'),
    (SCHEMA_constrained_integer(-54, lowerEndpoint_value=-56, upperEndpoint_value=-53), '80'),
    (SCHEMA_constrained_integer(-53, lowerEndpoint_value=-56, upperEndpoint_value=-53), 'C0'),
    (SCHEMA_constrained_integer(4000, lowerEndpoint_value=4000, upperEndpoint_value=4003), '00'),
    (SCHEMA_constrained_integer(4001, lowerEndpoint_value=4000, upperEndpoint_value=4003), '40'),
    (SCHEMA_constrained_integer(4002, lowerEndpoint_value=4000, upperEndpoint_value=4003), '80'),
    (SCHEMA_constrained_integer(4003, lowerEndpoint_value=4000, upperEndpoint_value=4003), 'C0'),
])
def test_constrained_integer_range_has_value_3_4(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-2, lowerEndpoint_value=-2, upperEndpoint_value=2), '00'),
    (SCHEMA_constrained_integer(-1, lowerEndpoint_value=-2, upperEndpoint_value=2), '20'),
    (SCHEMA_constrained_integer(0, lowerEndpoint_value=-2, upperEndpoint_value=2), '40'),
    (SCHEMA_constrained_integer(1, lowerEndpoint_value=-2, upperEndpoint_value=2), '60'),
    (SCHEMA_constrained_integer(2, lowerEndpoint_value=-2, upperEndpoint_value=2), '80'),
    (SCHEMA_constrained_integer(3, lowerEndpoint_value=-2, upperEndpoint_value=3), 'A0'),
    (SCHEMA_constrained_integer(4, lowerEndpoint_value=-2, upperEndpoint_value=4), 'C0'),
    (SCHEMA_constrained_integer(5, lowerEndpoint_value=-2, upperEndpoint_value=5), 'E0'),
])
def test_constrained_integer_range_has_value_5_6_7_8(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-100000, lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '00'),
    (SCHEMA_constrained_integer(-99999, lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '10'),
    (SCHEMA_constrained_integer(-99998, lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '20'),
    (SCHEMA_constrained_integer(-99997, lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '30'),
    (SCHEMA_constrained_integer(-99996, lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '40'),
    (SCHEMA_constrained_integer(-99995, lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '50'),
    (SCHEMA_constrained_integer(-99994, lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '60'),
    (SCHEMA_constrained_integer(-99993, lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '70'),
    (SCHEMA_constrained_integer(-99992, lowerEndpoint_value=-100000, upperEndpoint_value=-99992), '80'),
    (SCHEMA_constrained_integer(-99991, lowerEndpoint_value=-100000, upperEndpoint_value=-99991), '90'),
    (SCHEMA_constrained_integer(-99990, lowerEndpoint_value=-100000, upperEndpoint_value=-99990), 'A0'),
    (SCHEMA_constrained_integer(-99989, lowerEndpoint_value=-100000, upperEndpoint_value=-99989), 'B0'),
    (SCHEMA_constrained_integer(-99988, lowerEndpoint_value=-100000, upperEndpoint_value=-99988), 'C0'),
    (SCHEMA_constrained_integer(-99987, lowerEndpoint_value=-100000, upperEndpoint_value=-99987), 'D0'),
    (SCHEMA_constrained_integer(-99986, lowerEndpoint_value=-100000, upperEndpoint_value=-99986), 'E0'),
    (SCHEMA_constrained_integer(-99985, lowerEndpoint_value=-100000, upperEndpoint_value=-99985), 'F0'),
])
def test_constrained_integer_range_has_value_9_to_16(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-4001, lowerEndpoint_value=-4016, upperEndpoint_value=-4000), '78'),
    (SCHEMA_constrained_integer(4001, lowerEndpoint_value=4000, upperEndpoint_value=4016), '08'),
    (SCHEMA_constrained_integer(4003, lowerEndpoint_value=4000, upperEndpoint_value=4016), '18'),
    (SCHEMA_constrained_integer(4005, lowerEndpoint_value=4000, upperEndpoint_value=4016), '28'),
    (SCHEMA_constrained_integer(4010, lowerEndpoint_value=4000, upperEndpoint_value=4016), '50'),
    (SCHEMA_constrained_integer(4014, lowerEndpoint_value=4000, upperEndpoint_value=4016), '70'),
    (SCHEMA_constrained_integer(4016, lowerEndpoint_value=4000, upperEndpoint_value=4016), '80'),
    (SCHEMA_constrained_integer(4017, lowerEndpoint_value=4000, upperEndpoint_value=4017), '88'),
    (SCHEMA_constrained_integer(4020, lowerEndpoint_value=4000, upperEndpoint_value=4020), 'A0'),
    (SCHEMA_constrained_integer(4024, lowerEndpoint_value=4000, upperEndpoint_value=4024), 'C0'),
    (SCHEMA_constrained_integer(4028, lowerEndpoint_value=4000, upperEndpoint_value=4028), 'E0'),
    (SCHEMA_constrained_integer(4031, lowerEndpoint_value=4000, upperEndpoint_value=4031), 'F8'),
])
def test_constrained_integer_range_has_value_17_to_32(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-1000001, lowerEndpoint_value=-1000032, upperEndpoint_value=-1000000), '7C'),
    (SCHEMA_constrained_integer(1000001, lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '04'),
    (SCHEMA_constrained_integer(1000005, lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '14'),
    (SCHEMA_constrained_integer(1000009, lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '24'),
    (SCHEMA_constrained_integer(1000016, lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '40'),
    (SCHEMA_constrained_integer(1000022, lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '58'),
    (SCHEMA_constrained_integer(1000023, lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '5C'),
    (SCHEMA_constrained_integer(1000024, lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '60'),
    (SCHEMA_constrained_integer(1000028, lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '70'),
    (SCHEMA_constrained_integer(1000032, lowerEndpoint_value=1000000, upperEndpoint_value=1000032), '80'),
    (SCHEMA_constrained_integer(1000037, lowerEndpoint_value=1000000, upperEndpoint_value=1000040), '94'),
    (SCHEMA_constrained_integer(1000045, lowerEndpoint_value=1000000, upperEndpoint_value=1000045), 'B4'),
    (SCHEMA_constrained_integer(1000055, lowerEndpoint_value=1000000, upperEndpoint_value=1000056), 'DC'),
    (SCHEMA_constrained_integer(1000063, lowerEndpoint_value=1000000, upperEndpoint_value=1000063), 'FC'),
])
def test_constrained_integer_range_has_value_33_to_64(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-7, lowerEndpoint_value=-64, upperEndpoint_value=0), '72'),
    (SCHEMA_constrained_integer(7, lowerEndpoint_value=0, upperEndpoint_value=64), '0E'),
    (SCHEMA_constrained_integer(25, lowerEndpoint_value=0, upperEndpoint_value=64), '32'),
    (SCHEMA_constrained_integer(44, lowerEndpoint_value=0, upperEndpoint_value=64), '58'),
    (SCHEMA_constrained_integer(61, lowerEndpoint_value=0, upperEndpoint_value=64), '7A'),
    (SCHEMA_constrained_integer(69, lowerEndpoint_value=0, upperEndpoint_value=70), '8A'),
    (SCHEMA_constrained_integer(77, lowerEndpoint_value=0, upperEndpoint_value=77), '9A'),
    (SCHEMA_constrained_integer(85, lowerEndpoint_value=0, upperEndpoint_value=85), 'AA'),
    (SCHEMA_constrained_integer(98, lowerEndpoint_value=0, upperEndpoint_value=98), 'C4'),
    (SCHEMA_constrained_integer(111, lowerEndpoint_value=0, upperEndpoint_value=111), 'DE'),
    (SCHEMA_constrained_integer(119, lowerEndpoint_value=0, upperEndpoint_value=120), 'EE'),
    (SCHEMA_constrained_integer(127, lowerEndpoint_value=0, upperEndpoint_value=127), 'FE'),
])
def test_constrained_integer_range_has_value_65_to_128(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-7, lowerEndpoint_value=-128, upperEndpoint_value=0), '79'),
    (SCHEMA_constrained_integer(7, lowerEndpoint_value=0, upperEndpoint_value=128), '07'),
    (SCHEMA_constrained_integer(25, lowerEndpoint_value=0, upperEndpoint_value=128), '19'),
    (SCHEMA_constrained_integer(44, lowerEndpoint_value=0, upperEndpoint_value=128), '2C'),
    (SCHEMA_constrained_integer(61, lowerEndpoint_value=0, upperEndpoint_value=128), '3D'),
    (SCHEMA_constrained_integer(69, lowerEndpoint_value=0, upperEndpoint_value=128), '45'),
    (SCHEMA_constrained_integer(77, lowerEndpoint_value=0, upperEndpoint_value=128), '4D'),
    (SCHEMA_constrained_integer(85, lowerEndpoint_value=0, upperEndpoint_value=128), '55'),
    (SCHEMA_constrained_integer(98, lowerEndpoint_value=0, upperEndpoint_value=128), '62'),
    (SCHEMA_constrained_integer(111, lowerEndpoint_value=0, upperEndpoint_value=128), '6F'),
    (SCHEMA_constrained_integer(119, lowerEndpoint_value=0, upperEndpoint_value=128), '77'),
    (SCHEMA_constrained_integer(127, lowerEndpoint_value=0, upperEndpoint_value=128), '7F'),
    (SCHEMA_constrained_integer(128, lowerEndpoint_value=0, upperEndpoint_value=128), '80'),
    (SCHEMA_constrained_integer(140, lowerEndpoint_value=0, upperEndpoint_value=140), '8C'),
    (SCHEMA_constrained_integer(161, lowerEndpoint_value=0, upperEndpoint_value=161), 'A1'),
    (SCHEMA_constrained_integer(182, lowerEndpoint_value=0, upperEndpoint_value=182), 'B6'),
    (SCHEMA_constrained_integer(230, lowerEndpoint_value=0, upperEndpoint_value=230), 'E6'),
    (SCHEMA_constrained_integer(253, lowerEndpoint_value=0, upperEndpoint_value=253), 'FD'),
    (SCHEMA_constrained_integer(254, lowerEndpoint_value=0, upperEndpoint_value=254), 'FE'),
])
def test_constrained_integer_range_has_value_129_to_255(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-7, lowerEndpoint_value=-255, upperEndpoint_value=0), 'F8'),
    (SCHEMA_constrained_integer(7, lowerEndpoint_value=0, upperEndpoint_value=255), '07'),
    (SCHEMA_constrained_integer(25, lowerEndpoint_value=0, upperEndpoint_value=255), '19'),
    (SCHEMA_constrained_integer(44, lowerEndpoint_value=0, upperEndpoint_value=255), '2C'),
    (SCHEMA_constrained_integer(61, lowerEndpoint_value=0, upperEndpoint_value=255), '3D'),
    (SCHEMA_constrained_integer(69, lowerEndpoint_value=0, upperEndpoint_value=255), '45'),
    (SCHEMA_constrained_integer(77, lowerEndpoint_value=0, upperEndpoint_value=255), '4D'),
    (SCHEMA_constrained_integer(85, lowerEndpoint_value=0, upperEndpoint_value=255), '55'),
    (SCHEMA_constrained_integer(98, lowerEndpoint_value=0, upperEndpoint_value=255), '62'),
    (SCHEMA_constrained_integer(111, lowerEndpoint_value=0, upperEndpoint_value=255), '6F'),
    (SCHEMA_constrained_integer(119, lowerEndpoint_value=0, upperEndpoint_value=255), '77'),
    (SCHEMA_constrained_integer(127, lowerEndpoint_value=0, upperEndpoint_value=255), '7F'),
    (SCHEMA_constrained_integer(128, lowerEndpoint_value=0, upperEndpoint_value=255), '80'),
    (SCHEMA_constrained_integer(140, lowerEndpoint_value=0, upperEndpoint_value=255), '8C'),
    (SCHEMA_constrained_integer(161, lowerEndpoint_value=0, upperEndpoint_value=255), 'A1'),
    (SCHEMA_constrained_integer(182, lowerEndpoint_value=0, upperEndpoint_value=255), 'B6'),
    (SCHEMA_constrained_integer(230, lowerEndpoint_value=0, upperEndpoint_value=255), 'E6'),
    (SCHEMA_constrained_integer(253, lowerEndpoint_value=0, upperEndpoint_value=255), 'FD'),
    (SCHEMA_constrained_integer(254, lowerEndpoint_value=0, upperEndpoint_value=255), 'FE'),
    (SCHEMA_constrained_integer(255, lowerEndpoint_value=0, upperEndpoint_value=255), 'FF'),
])
def test_constrained_integer_range_has_value_256(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-7, lowerEndpoint_value=-256, upperEndpoint_value=0), '00F9'),
    (SCHEMA_constrained_integer(7, lowerEndpoint_value=0, upperEndpoint_value=256), '0007'),
    (SCHEMA_constrained_integer(25, lowerEndpoint_value=0, upperEndpoint_value=256), '0019'),
    (SCHEMA_constrained_integer(44, lowerEndpoint_value=0, upperEndpoint_value=256), '002C'),
    (SCHEMA_constrained_integer(61, lowerEndpoint_value=0, upperEndpoint_value=256), '003D'),
    (SCHEMA_constrained_integer(69, lowerEndpoint_value=0, upperEndpoint_value=256), '0045'),
    (SCHEMA_constrained_integer(77, lowerEndpoint_value=0, upperEndpoint_value=256), '004D'),
    (SCHEMA_constrained_integer(85, lowerEndpoint_value=0, upperEndpoint_value=256), '0055'),
    (SCHEMA_constrained_integer(98, lowerEndpoint_value=0, upperEndpoint_value=256), '0062'),
    (SCHEMA_constrained_integer(111, lowerEndpoint_value=0, upperEndpoint_value=256), '006F'),
    (SCHEMA_constrained_integer(119, lowerEndpoint_value=0, upperEndpoint_value=256), '0077'),
    (SCHEMA_constrained_integer(127, lowerEndpoint_value=0, upperEndpoint_value=256), '007F'),
    (SCHEMA_constrained_integer(128, lowerEndpoint_value=0, upperEndpoint_value=256), '0080'),
    (SCHEMA_constrained_integer(140, lowerEndpoint_value=0, upperEndpoint_value=256), '008C'),
    (SCHEMA_constrained_integer(161, lowerEndpoint_value=0, upperEndpoint_value=256), '00A1'),
    (SCHEMA_constrained_integer(182, lowerEndpoint_value=0, upperEndpoint_value=256), '00B6'),
    (SCHEMA_constrained_integer(230, lowerEndpoint_value=0, upperEndpoint_value=256), '00E6'),
    (SCHEMA_constrained_integer(253, lowerEndpoint_value=0, upperEndpoint_value=256), '00FD'),
    (SCHEMA_constrained_integer(254, lowerEndpoint_value=0, upperEndpoint_value=256), '00FE'),
    (SCHEMA_constrained_integer(255, lowerEndpoint_value=0, upperEndpoint_value=256), '00FF'),
    (SCHEMA_constrained_integer(256, lowerEndpoint_value=0, upperEndpoint_value=256), '0100'),
    (SCHEMA_constrained_integer(511, lowerEndpoint_value=0, upperEndpoint_value=511), '01FF'),
    (SCHEMA_constrained_integer(512, lowerEndpoint_value=0, upperEndpoint_value=512), '0200'),
    (SCHEMA_constrained_integer(1023, lowerEndpoint_value=0, upperEndpoint_value=1023), '03FF'),
    (SCHEMA_constrained_integer(1024, lowerEndpoint_value=0, upperEndpoint_value=1024), '0400'),
    (SCHEMA_constrained_integer(1024, lowerEndpoint_value=0, upperEndpoint_value=1024), '0400'),
    (SCHEMA_constrained_integer(8191, lowerEndpoint_value=0, upperEndpoint_value=8191), '1FFF'),
    (SCHEMA_constrained_integer(8192, lowerEndpoint_value=0, upperEndpoint_value=8192), '2000'),
    (SCHEMA_constrained_integer(32766, lowerEndpoint_value=0, upperEndpoint_value=32768), '7FFE'),
    (SCHEMA_constrained_integer(32767, lowerEndpoint_value=0, upperEndpoint_value=32768), '7FFF'),
    (SCHEMA_constrained_integer(32768, lowerEndpoint_value=0, upperEndpoint_value=32768), '8000'),
    (SCHEMA_constrained_integer(44321, lowerEndpoint_value=0, upperEndpoint_value=44321), 'AD21'),
    (SCHEMA_constrained_integer(55555, lowerEndpoint_value=0, upperEndpoint_value=60000), 'D903'),
    (SCHEMA_constrained_integer(60000, lowerEndpoint_value=0, upperEndpoint_value=65535), 'EA60'),
    (SCHEMA_constrained_integer(65534, lowerEndpoint_value=0, upperEndpoint_value=65535), 'FFFE'),
    (SCHEMA_constrained_integer(65535, lowerEndpoint_value=0, upperEndpoint_value=65535), 'FFFF'),
])
def test_constrained_integer_range_has_value_257_to_65536(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(-100000, lowerEndpoint_value=-1234567, upperEndpoint_value=0), '80114FE7'),
    (SCHEMA_constrained_integer(7, lowerEndpoint_value=0, upperEndpoint_value=1234567), '0007'),
    (SCHEMA_constrained_integer(25, lowerEndpoint_value=0, upperEndpoint_value=1234567), '0019'),
    (SCHEMA_constrained_integer(44, lowerEndpoint_value=0, upperEndpoint_value=1234567), '002C'),
    (SCHEMA_constrained_integer(61, lowerEndpoint_value=0, upperEndpoint_value=1234567), '003D'),
    (SCHEMA_constrained_integer(69, lowerEndpoint_value=0, upperEndpoint_value=1234567), '0045'),
    (SCHEMA_constrained_integer(77, lowerEndpoint_value=0, upperEndpoint_value=1234567), '004D'),
    (SCHEMA_constrained_integer(85, lowerEndpoint_value=0, upperEndpoint_value=1234567), '0055'),
    (SCHEMA_constrained_integer(98, lowerEndpoint_value=0, upperEndpoint_value=1234567), '0062'),
    (SCHEMA_constrained_integer(111, lowerEndpoint_value=0, upperEndpoint_value=1234567), '006F'),
    (SCHEMA_constrained_integer(119, lowerEndpoint_value=0, upperEndpoint_value=1234567), '0077'),
    (SCHEMA_constrained_integer(127, lowerEndpoint_value=0, upperEndpoint_value=1234567), '007F'),
    (SCHEMA_constrained_integer(128, lowerEndpoint_value=0, upperEndpoint_value=1234567), '0080'),
    (SCHEMA_constrained_integer(140, lowerEndpoint_value=0, upperEndpoint_value=1234567), '008C'),
    (SCHEMA_constrained_integer(161, lowerEndpoint_value=0, upperEndpoint_value=1234567), '00A1'),
    (SCHEMA_constrained_integer(182, lowerEndpoint_value=0, upperEndpoint_value=1234567), '00B6'),
    (SCHEMA_constrained_integer(230, lowerEndpoint_value=0, upperEndpoint_value=1234567), '00E6'),
    (SCHEMA_constrained_integer(253, lowerEndpoint_value=0, upperEndpoint_value=1234567), '00FD'),
    (SCHEMA_constrained_integer(254, lowerEndpoint_value=0, upperEndpoint_value=1234567), '00FE'),
    (SCHEMA_constrained_integer(255, lowerEndpoint_value=0, upperEndpoint_value=1234567), '00FF'),
    (SCHEMA_constrained_integer(256, lowerEndpoint_value=0, upperEndpoint_value=1234567), '400100'),
    (SCHEMA_constrained_integer(511, lowerEndpoint_value=0, upperEndpoint_value=1234567), '4001FF'),
    (SCHEMA_constrained_integer(512, lowerEndpoint_value=0, upperEndpoint_value=1234567), '400200'),
    (SCHEMA_constrained_integer(1023, lowerEndpoint_value=0, upperEndpoint_value=1234567), '4003FF'),
    (SCHEMA_constrained_integer(1024, lowerEndpoint_value=0, upperEndpoint_value=1234567), '400400'),
    (SCHEMA_constrained_integer(1024, lowerEndpoint_value=0, upperEndpoint_value=1234567), '400400'),
    (SCHEMA_constrained_integer(8191, lowerEndpoint_value=0, upperEndpoint_value=1234567), '401FFF'),
    (SCHEMA_constrained_integer(8192, lowerEndpoint_value=0, upperEndpoint_value=1234567), '402000'),
    (SCHEMA_constrained_integer(32766, lowerEndpoint_value=0, upperEndpoint_value=1234567), '407FFE'),
    (SCHEMA_constrained_integer(32767, lowerEndpoint_value=0, upperEndpoint_value=1234567), '407FFF'),
    (SCHEMA_constrained_integer(32768, lowerEndpoint_value=0, upperEndpoint_value=1234567), '408000'),
    (SCHEMA_constrained_integer(44321, lowerEndpoint_value=0, upperEndpoint_value=1234567), '40AD21'),
    (SCHEMA_constrained_integer(55555, lowerEndpoint_value=0, upperEndpoint_value=1234567), '40D903'),
    (SCHEMA_constrained_integer(60000, lowerEndpoint_value=0, upperEndpoint_value=1234567), '40EA60'),
    (SCHEMA_constrained_integer(65534, lowerEndpoint_value=0, upperEndpoint_value=1234567), '40FFFE'),
    (SCHEMA_constrained_integer(65535, lowerEndpoint_value=0, upperEndpoint_value=1234567), '40FFFF'),
    (SCHEMA_constrained_integer(65536, lowerEndpoint_value=0, upperEndpoint_value=1234567), '80010000'),
    (SCHEMA_constrained_integer(100000, lowerEndpoint_value=0, upperEndpoint_value=1234567), '800186A0'),
    (SCHEMA_constrained_integer(256, lowerEndpoint_value=256, upperEndpoint_value=1234567), '0000'),
    (SCHEMA_constrained_integer(100, lowerEndpoint_value=0, upperEndpoint_value=4294967295), '0064'),
    (SCHEMA_constrained_integer(255, lowerEndpoint_value=0, upperEndpoint_value=4294967295), '00FF'),
    (SCHEMA_constrained_integer(256, lowerEndpoint_value=0, upperEndpoint_value=4294967295), '400100'),
    (SCHEMA_constrained_integer(100000, lowerEndpoint_value=0, upperEndpoint_value=4294967295), '800186A0'),
    (SCHEMA_constrained_integer(100000000, lowerEndpoint_value=0, upperEndpoint_value=4294967295), 'C005F5E100'),
    (SCHEMA_constrained_integer(4294967294, lowerEndpoint_value=0, upperEndpoint_value=4294967295), 'C0FFFFFFFE'),
    (SCHEMA_constrained_integer(4294967295, lowerEndpoint_value=0, upperEndpoint_value=4294967295), 'C0FFFFFFFF'),
])
def test_constrained_integer_range_has_value_greater_than_65536(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(7, lowerEndpoint_value=0, upperEndpoint_value=MAX), '0107'),
    (SCHEMA_constrained_integer(25, lowerEndpoint_value=0, upperEndpoint_value=MAX), '0119'),
    (SCHEMA_constrained_integer(44, lowerEndpoint_value=0, upperEndpoint_value=MAX), '012C'),
    (SCHEMA_constrained_integer(61, lowerEndpoint_value=0, upperEndpoint_value=MAX), '013D'),
    (SCHEMA_constrained_integer(69, lowerEndpoint_value=0, upperEndpoint_value=MAX), '0145'),
    (SCHEMA_constrained_integer(77, lowerEndpoint_value=0, upperEndpoint_value=MAX), '014D'),
    (SCHEMA_constrained_integer(85, lowerEndpoint_value=0, upperEndpoint_value=MAX), '0155'),
    (SCHEMA_constrained_integer(98, lowerEndpoint_value=0, upperEndpoint_value=MAX), '0162'),
    (SCHEMA_constrained_integer(111, lowerEndpoint_value=0, upperEndpoint_value=MAX), '016F'),
    (SCHEMA_constrained_integer(119, lowerEndpoint_value=0, upperEndpoint_value=MAX), '0177'),
    (SCHEMA_constrained_integer(127, lowerEndpoint_value=0, upperEndpoint_value=MAX), '017F'),
    (SCHEMA_constrained_integer(128, lowerEndpoint_value=0, upperEndpoint_value=MAX), '0180'),
    (SCHEMA_constrained_integer(140, lowerEndpoint_value=0, upperEndpoint_value=MAX), '018C'),
    (SCHEMA_constrained_integer(161, lowerEndpoint_value=0, upperEndpoint_value=MAX), '01A1'),
    (SCHEMA_constrained_integer(182, lowerEndpoint_value=0, upperEndpoint_value=MAX), '01B6'),
    (SCHEMA_constrained_integer(230, lowerEndpoint_value=0, upperEndpoint_value=MAX), '01E6'),
    (SCHEMA_constrained_integer(253, lowerEndpoint_value=0, upperEndpoint_value=MAX), '01FD'),
    (SCHEMA_constrained_integer(254, lowerEndpoint_value=0, upperEndpoint_value=MAX), '01FE'),
    (SCHEMA_constrained_integer(255, lowerEndpoint_value=0, upperEndpoint_value=MAX), '01FF'),
    (SCHEMA_constrained_integer(256, lowerEndpoint_value=0, upperEndpoint_value=MAX), '020100'),
    (SCHEMA_constrained_integer(511, lowerEndpoint_value=0, upperEndpoint_value=MAX), '0201FF'),
    (SCHEMA_constrained_integer(512, lowerEndpoint_value=0, upperEndpoint_value=MAX), '020200'),
    (SCHEMA_constrained_integer(1023, lowerEndpoint_value=0, upperEndpoint_value=MAX), '0203FF'),
    (SCHEMA_constrained_integer(1024, lowerEndpoint_value=0, upperEndpoint_value=MAX), '020400'),
    (SCHEMA_constrained_integer(1024, lowerEndpoint_value=0, upperEndpoint_value=MAX), '020400'),
    (SCHEMA_constrained_integer(8191, lowerEndpoint_value=0, upperEndpoint_value=MAX), '021FFF'),
    (SCHEMA_constrained_integer(8192, lowerEndpoint_value=0, upperEndpoint_value=MAX), '022000'),
    (SCHEMA_constrained_integer(32766, lowerEndpoint_value=0, upperEndpoint_value=MAX), '027FFE'),
    (SCHEMA_constrained_integer(32767, lowerEndpoint_value=0, upperEndpoint_value=MAX), '027FFF'),
    (SCHEMA_constrained_integer(32768, lowerEndpoint_value=0, upperEndpoint_value=MAX), '028000'),
    (SCHEMA_constrained_integer(44321, lowerEndpoint_value=0, upperEndpoint_value=MAX), '02AD21'),
    (SCHEMA_constrained_integer(55555, lowerEndpoint_value=0, upperEndpoint_value=MAX), '02D903'),
    (SCHEMA_constrained_integer(60000, lowerEndpoint_value=0, upperEndpoint_value=MAX), '02EA60'),
    (SCHEMA_constrained_integer(65534, lowerEndpoint_value=0, upperEndpoint_value=MAX), '02FFFE'),
    (SCHEMA_constrained_integer(65535, lowerEndpoint_value=0, upperEndpoint_value=MAX), '02FFFF'),
    (SCHEMA_constrained_integer(65536, lowerEndpoint_value=0, upperEndpoint_value=MAX), '03010000'),
    (SCHEMA_constrained_integer(100000, lowerEndpoint_value=0, upperEndpoint_value=MAX), '030186A0'),
    (SCHEMA_constrained_integer(256, lowerEndpoint_value=256, upperEndpoint_value=MAX), '0100')
])
def test_semi_constrained_integer_is_encoded(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(3, lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '60'),
    (SCHEMA_constrained_integer(3, lowerEndpoint_value=0, upperEndpoint_value=120, extensionMarker_value=True), '03'),
    (SCHEMA_constrained_integer(3, lowerEndpoint_value=0, upperEndpoint_value=255, extensionMarker_value=True), '0003'),
    (SCHEMA_constrained_integer(3, lowerEndpoint_value=0, upperEndpoint_value=10000, extensionMarker_value=True), '000003'),
    (SCHEMA_constrained_integer(3, lowerEndpoint_value=0, upperEndpoint_value=100000, extensionMarker_value=True), '0003'),
    (SCHEMA_constrained_integer(254, lowerEndpoint_value=0, upperEndpoint_value=255, extensionMarker_value=True), '00FE'),
    (SCHEMA_constrained_integer(254, lowerEndpoint_value=0, upperEndpoint_value=10000, extensionMarker_value=True), '0000FE'),
    (SCHEMA_constrained_integer(254, lowerEndpoint_value=0, upperEndpoint_value=100000, extensionMarker_value=True), '00FE'),
    (SCHEMA_constrained_integer(1023, lowerEndpoint_value=0, upperEndpoint_value=10000, extensionMarker_value=True), '0003FF'),
    (SCHEMA_constrained_integer(1023, lowerEndpoint_value=0, upperEndpoint_value=100000, extensionMarker_value=True), '2003FF'),
    (SCHEMA_constrained_integer(32766, lowerEndpoint_value=0, upperEndpoint_value=100000, extensionMarker_value=True), '207FFE'),
    (SCHEMA_constrained_integer(65535, lowerEndpoint_value=0, upperEndpoint_value=1000000, extensionMarker_value=True), '20FFFF'),
    (SCHEMA_constrained_integer(100000, lowerEndpoint_value=0, upperEndpoint_value=1000000, extensionMarker_value=True), '400186A0'),
])
def test_extension_marker_is_present_and_value_is_within_extension_root_integer_is_encoded(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("integer, encoded", [
    (SCHEMA_constrained_integer(4, lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '800104'),
    (SCHEMA_constrained_integer(100000, lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '80030186A0'),
    (SCHEMA_constrained_integer(-4, lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '8001FC'),
    (SCHEMA_constrained_integer(-100000, lowerEndpoint_value=0, upperEndpoint_value=3, extensionMarker_value=True), '8003FE7960'),
])
def test_extension_marker_is_present_and_values_in_not_within_extension_root_integer_is_encoded(integer, encoded):
    assert per_encoder(integer) == bytearray.fromhex(encoded)
