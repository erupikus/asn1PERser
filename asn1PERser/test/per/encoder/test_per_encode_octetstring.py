import pytest
from pyasn1.type.namedtype import NamedType, NamedTypes, DefaultedNamedType, OptionalNamedType
from asn1PERser.codec.per.encoder import encode as per_encoder
from asn1PERser.classes.data.builtin.OctetStringType import OctetStringType
from asn1PERser.classes.types.constraint import ValueSize


def SCHEMA_no_constrain_octetstring():
    class MyOctetString(OctetStringType):
        '''
        MyBitString ::= OCTET STRING
        '''
        pass
    return MyOctetString


def SCHEMA_constrained_octetstring(lb, ub):
    class MyOctetString(OctetStringType):
        '''
        MyBitString ::= OCTET STRING (SIZE(lowerEndpoint..upperEndpoint))
        '''
        subtypeSpec = ValueSize(lb, ub)
    return MyOctetString


def SCHEMA_constrained_ext_octetstring(lb, ub):
    class MyOctetString(OctetStringType):
        '''
        MyBitString ::= OCTET STRING (SIZE(lowerEndpoint..upperEndpoint, ...))
        '''
        subtypeSpec = ValueSize(lb, ub, extensionMarker=True)
    return MyOctetString


def DATA_octetstring(schema, bin_val=None, hex_val=None):
    if bin_val is not None:
        octetstring = schema(binValue=bin_val)
    elif hex_val is not None:
        octetstring = schema(hexValue=hex_val)
    return octetstring


@pytest.mark.parametrize("octetstring, encoded", [
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='1'), '0180'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='0'), '0100'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='01'), '0140'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='10'), '0180'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='1111'), '01F0'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='111100'), '01F0'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='1111000011110'), '02F0F0'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='0000110000110011'), '020C33'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='01011100101100110101101101101110001110010101110010101'),
     '075CB35B6E395CA8'),
])
def test_no_constrain_octetstring_as_binary_value_can_be_encoded(octetstring, encoded):
    assert per_encoder(octetstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("octetstring, encoded", [
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='0'), '0100'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='1'), '0110'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='01'), '0101'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='10'), '0110'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='00A'), '0200A0'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='AA0'), '02AA00'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='ABCDEFA'), '04ABCDEFA0'),
    (DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='0123ABCDEFA0123'), '080123ABCDEFA01230'),
])
def test_no_constrain_octetstring_as_hex_value_can_be_encoded(octetstring, encoded):
    assert per_encoder(octetstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("octetstring, encoded", [
    # (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=0), bin_val=''), '00'),    # does not work
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=0), hex_val=''), '00'),
])
def test_constrained_octetstring_of_zero_length_can_be_encoded(octetstring, encoded):
    assert per_encoder(octetstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("octetstring, encoded", [
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), bin_val='1'), '80'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), bin_val='01110'), '70'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), bin_val='00001111'), '0F'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), hex_val='C'), 'C0'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), hex_val='CF'), 'CF'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), bin_val='111111110'), 'FF00'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), bin_val='0000111100001'), '0F08'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), bin_val='1100110011001100'), 'CCCC'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), hex_val='ABC'), 'ABC0'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), hex_val='000'), '0000'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), hex_val='0000'), '0000'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), hex_val='FFFF'), 'FFFF'),
])
def test_constrained_same_len_octetstring_with_len_le_2_octetes_can_be_encoded(octetstring, encoded):
    assert per_encoder(octetstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("octetstring, encoded", [
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=3, ub=3), bin_val='000000010000000100000001'), '010101'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=3, ub=3), hex_val='ABCDEF'), 'ABCDEF'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=4, ub=4), bin_val='01111111111111111111111100000000'), '7FFFFF00'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=4, ub=4), hex_val='ABCDEF01'), 'ABCDEF01'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=17, ub=17), hex_val='11223344556677889900AABBCCDDEEFF11'),
     '11223344556677889900AABBCCDDEEFF11'),
])
def test_constrained_same_len_octetstring_with_len_gt_2_and_lt_64K_can_be_encoded(octetstring, encoded):
    assert per_encoder(octetstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("octetstring, encoded", [
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=15), hex_val=''), '00'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=15), hex_val='A'), '10A0'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=15), hex_val='A0'), '10A0'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=15), hex_val='112233445566778899001122334455'),
     'F0112233445566778899001122334455'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=22), hex_val='A'), '08A0'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=22), hex_val='A0'), '08A0'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=22), hex_val='112233445566778899001122334455'),
     '78112233445566778899001122334455'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=22), hex_val='11223344556677889900112233445566778899001122'),
     'B011223344556677889900112233445566778899001122'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=10, ub=15), hex_val='112233445566778899AA'),
     '00112233445566778899AA'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=10, ub=15), hex_val='112233445566778899AABBCCDDEEFF'),
    'A0112233445566778899AABBCCDDEEFF'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=10, ub=22), hex_val='112233445566778899AA'),
     '00112233445566778899AA'),
    (DATA_octetstring(SCHEMA_constrained_octetstring(lb=10, ub=22), hex_val='112233445566778899AABBCCDDEEFF001122334455'),
    'B0112233445566778899AABBCCDDEEFF001122334455'),
])
def test_constrained_different_len_octet_string_can_be_encoded(octetstring, encoded):
    assert per_encoder(octetstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("octetstring, encoded", [
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=0), hex_val=''), '00'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=1, ub=1), hex_val='A'), '5000'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=1, ub=1), hex_val='AB'), '5580'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=5, ub=5), hex_val='112233445'), '001122334450'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=5, ub=5), hex_val='1122334455'), '001122334455'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=15, ub=15), hex_val='112233445566778899001122334455'),
     '00112233445566778899001122334455'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=22, ub=22), hex_val='11223344556677889900112233445566778899001122'),
     '0011223344556677889900112233445566778899001122'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val=''), '00'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val='A'), '20A0'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val='AB'), '20AB'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val='ABC'), '40ABC0'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val='ABCD'), '40ABCD'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=15), hex_val='A'), '08A0'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=15), hex_val='AB'), '08AB'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=15), hex_val='112233445566778899'), '48112233445566778899'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=15), hex_val='112233445566778899AABBCCDDEEFF'),
     '78112233445566778899AABBCCDDEEFF'),
])
def test_constrained_with_extension_when_len_is_within_extension_root_octetstring_can_be_encoded(octetstring, encoded):
    assert per_encoder(octetstring) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("octetstring, encoded", [
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=0), hex_val='A'), '8001A0'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=0), hex_val='AB'), '8001AB'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=0), hex_val='1122334455'), '80051122334455'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val=''), '8000'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val='A'), '8001A0'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val='AB'), '8001AB'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val='112233'), '8003112233'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val='1122334455'), '80051122334455'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val=''), '8000'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='A'), '8001A0'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='AB'), '8001AB'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='1122'), '80021122'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='1122334455'), '80051122334455'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='11223344556677'), '800711223344556677'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=10, ub=22), hex_val='112233445566778899'), '8009112233445566778899'),
    (DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=10, ub=22), hex_val='1122334455667788990011223344556677889900112233'),
     '80171122334455667788990011223344556677889900112233'),
])
def test_constrained_with_extension_when_len_is_NOT_within_extension_root_octetstring_can_be_encoded(octetstring, encoded):
    assert per_encoder(octetstring) == bytearray.fromhex(encoded)
