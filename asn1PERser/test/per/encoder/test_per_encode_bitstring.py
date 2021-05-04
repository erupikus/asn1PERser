import pytest
from asn1PERser.codec.per.encoder import encode as per_encoder
from asn1PERser.classes.data.builtin.BitStringType import BitStringType
from asn1PERser.classes.types.constraint import ValueSize


def SCHEMA_no_constrain_bitstring():
    class MyBitString(BitStringType):
        '''
        MyBitString ::= BIT STRING
        '''
        pass
    return MyBitString


def SCHEMA_constrained_bitstring(lb, ub):
    class MyBitString(BitStringType):
        '''
        MyBitString ::= BIT STRING (SIZE(lowerEndpoint..upperEndpoint))
        '''
        subtypeSpec = ValueSize(lb, ub)
    return MyBitString


def SCHEMA_constrained_ext_bitstring(lb, ub):
    class MyBitString(BitStringType):
        '''
        MyBitString ::= BIT STRING (SIZE(lowerEndpoint..upperEndpoint, ...))
        '''
        subtypeSpec = ValueSize(lb, ub, extensionMarker=True)
    return MyBitString


def DATA_bitstring(schema, bin_val=None, hex_val=None):
    if bin_val is not None:
        bitstring = schema(binValue=bin_val)
    elif hex_val is not None:
        bitstring = schema(hexValue=hex_val)
    return bitstring


@pytest.mark.parametrize("bitstring, encoded", [
    # (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val=''), '00'),    # Does not work
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='0'), '0100'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='1'), '0180'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='01'), '0240'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='10'), '0280'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='11'), '02C0'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='011'), '0360'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='1010'), '04A0'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='1111'), '04F0'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='111111111111111'), '0FFFFE'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='111111111111111111111111'), '18FFFFFF'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='100000000000000000000001'), '18800001'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='000000000000000000000001'), '18000001'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='0000111000000000010000001111110000000000000001'),
     '2E0E0040FC0004'),
])
def test_no_constrain_bitstring_as_binary_value_can_be_encoded(bitstring, encoded):
    assert per_encoder(bitstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("bitstring, encoded", [
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='0'), '0400'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='1'), '0410'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='10'), '0810'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='01'), '0801'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='A'), '04A0'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='0A'), '080A'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='00000ABCDEF'), '2C00000ABCDEF0'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='ABCDEFABCDEF'), '30ABCDEFABCDEF'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='ABCDEFABCDEF0'), '34ABCDEFABCDEF00'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='ABCDEFABCDEF0123456789'), '58ABCDEFABCDEF0123456789'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='ABCDEFABCDEF0123456789ABCDEFABC'),
     '7CABCDEFABCDEF0123456789ABCDEFABC0'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='ABCDEFABCDEF0123456789ABCDEFABC0'),
     '8080ABCDEFABCDEF0123456789ABCDEFABC0'),
    (DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789'),
     '80B0ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789'),
])
def test_no_constrain_bitstring_as_hex_value_can_be_encoded(bitstring, encoded):
    assert per_encoder(bitstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("bitstring, encoded", [
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=0), bin_val=''), '00'),
    # (DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=0), hex_val=''), '00'),    # Does not work
])
def test_constrained_bitstring_of_zero_length_can_be_encoded(bitstring, encoded):
    assert per_encoder(bitstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("bitstring, encoded", [
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=1, ub=1), bin_val='1'), '80'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=1, ub=1), bin_val='0'), '00'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=2, ub=2), bin_val='10'), '80'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=2, ub=2), bin_val='11'), 'C0'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=4, ub=4), bin_val='1010'), 'A0'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=4, ub=4), bin_val='0101'), '50'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=7, ub=7), bin_val='1010101'), 'AA'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=7, ub=7), bin_val='0101010'), '54'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=15, ub=15), bin_val='110011001100110'), 'CCCC'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=15, ub=15), bin_val='001100110011001'), '3332'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=16, ub=16), bin_val='1100110011001100'), 'CCCC'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=16, ub=16), bin_val='0011001100110011'), '3333'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=4, ub=4), hex_val='A'), 'A0'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=8, ub=8), hex_val='BB'), 'BB'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=12, ub=12), hex_val='111'), '1110'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=16, ub=16), hex_val='2222'), '2222'),
])
def test_constrained_bitstring_same_length_gt_zero_and_le_16_can_be_encoded(bitstring, encoded):
    assert per_encoder(bitstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("bitstring, encoded", [
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=17, ub=17), bin_val='00110011001100111'), '333380'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=18, ub=18), bin_val='001100110011001101'), '333340'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=19, ub=19), bin_val='0011001100110011001'), '333320'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=20, ub=20), bin_val='00110011001100110011'), '333330'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=21, ub=21), bin_val='001100110011001100111'), '333338'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=22, ub=22), bin_val='0011001100110011001101'), '333334'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=23, ub=23), bin_val='00110011001100110011001'), '333332'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=24, ub=24), bin_val='001100110011001100110011'), '333333'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=25, ub=25), bin_val='0011001100110011001100111'), '33333380'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=128, ub=128), hex_val='ABCDEFABCDEF0123456789ABCDEFABC0'),
     'ABCDEFABCDEF0123456789ABCDEFABC0'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=176, ub=176), hex_val='ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789'),
     'ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789'),

])
def test_constrained_bitstring_same_length_gt_16_and_lt_64K_can_be_encoded(bitstring, encoded):
    assert per_encoder(bitstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("bitstring, encoded", [
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=1), bin_val='1'), '8080'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=15), bin_val='1'), '1080'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=15), bin_val='111000111000111'), 'F0E38E'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=14, ub=15), bin_val='111000111000111'), '80E38E'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=127), bin_val='111000111000111'), '1EE38E'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=1000), bin_val='111000111000111'), '000FE38E'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=10000), bin_val='111000111000111'), '000FE38E'),
    (DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=65535), bin_val='111000111000111'), '000FE38E'),
])
def test_constrained_bitstring_with_ub_less_then_64K_can_be_encoded(bitstring, encoded):
    assert per_encoder(bitstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("bitstring, encoded", [
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=1, ub=1), bin_val='1'), '40'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=1, ub=1), bin_val='0111111'), '80077E'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=2, ub=2), bin_val='10'), '40'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=2, ub=2), bin_val='101'), '8003A0'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=7, ub=7), bin_val='01010101'), '800855'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=15, ub=15), bin_val='11001100110011011'), '8011CCCD80'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=16, ub=16), bin_val='00110011001100110001'), '8014333310'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=25, ub=25), bin_val='0011001100110011001100111111'), '801C333333F0'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=128, ub=128), hex_val='ABCDEFABCDEF0123456789ABCDEFABC0'),
     '00ABCDEFABCDEF0123456789ABCDEFABC0'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=176, ub=176), hex_val='ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789'),
     '00ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=0, ub=1), bin_val='1'), '4080'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=0, ub=15), bin_val='1'), '0880'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=0, ub=15), bin_val='111100001111000'), '78F0F0'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=0, ub=15), bin_val='0111100001111000'), '80107878'),
    (DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=0, ub=128), hex_val='ABCDEFABCDEF0123456789ABCDEFABC0'),
     '4000ABCDEFABCDEF0123456789ABCDEFABC0'),
])
def test_constrained_bitstring_with_extension_marker_can_be_encoded(bitstring, encoded):
    assert per_encoder(bitstring) == bytearray.fromhex(encoded)
