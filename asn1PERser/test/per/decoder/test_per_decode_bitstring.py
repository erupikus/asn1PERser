import pytest
from asn1PERser.codec.per.decoder import decode as per_decoder
from asn1PERser.test.per.encoder.test_per_encode_bitstring import SCHEMA_constrained_bitstring, \
    SCHEMA_no_constrain_bitstring, SCHEMA_constrained_ext_bitstring, DATA_bitstring


@pytest.mark.parametrize("schema, encoded, value", [
    # (DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val=''), '00'),    # Does not work
    (SCHEMA_no_constrain_bitstring(), '0100', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='0')),
    (SCHEMA_no_constrain_bitstring(), '0180', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='1')),
    (SCHEMA_no_constrain_bitstring(), '0240', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='01')),
    (SCHEMA_no_constrain_bitstring(), '0280', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='10')),
    (SCHEMA_no_constrain_bitstring(), '02C0', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='11')),
    (SCHEMA_no_constrain_bitstring(), '0360', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='011')),
    (SCHEMA_no_constrain_bitstring(), '04A0', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='1010')),
    (SCHEMA_no_constrain_bitstring(), '04F0', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='1111')),
    (SCHEMA_no_constrain_bitstring(), '0FFFFE', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='111111111111111')),
    (SCHEMA_no_constrain_bitstring(), '18FFFFFF', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='111111111111111111111111')),
    (SCHEMA_no_constrain_bitstring(), '18800001', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='100000000000000000000001')),
    (SCHEMA_no_constrain_bitstring(), '18000001', DATA_bitstring(SCHEMA_no_constrain_bitstring(), bin_val='000000000000000000000001')),
    (SCHEMA_no_constrain_bitstring(), '2E0E0040FC0004', DATA_bitstring(SCHEMA_no_constrain_bitstring(),
                                                                       bin_val='0000111000000000010000001111110000000000000001')),
])
def test_no_constrain_bitstring_as_binary_value_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_no_constrain_bitstring(), '0400', DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='0')),
    (SCHEMA_no_constrain_bitstring(), '0410', DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='1')),
    (SCHEMA_no_constrain_bitstring(), '0810', DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='10')),
    (SCHEMA_no_constrain_bitstring(), '0801', DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='01')),
    (SCHEMA_no_constrain_bitstring(), '04A0', DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='A')),
    (SCHEMA_no_constrain_bitstring(), '080A', DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='0A')),
    (SCHEMA_no_constrain_bitstring(), '2C00000ABCDEF0', DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='00000ABCDEF')),
    (SCHEMA_no_constrain_bitstring(), '30ABCDEFABCDEF', DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='ABCDEFABCDEF')),
    (SCHEMA_no_constrain_bitstring(), '34ABCDEFABCDEF00', DATA_bitstring(SCHEMA_no_constrain_bitstring(), hex_val='ABCDEFABCDEF0')),
    (SCHEMA_no_constrain_bitstring(), '58ABCDEFABCDEF0123456789', DATA_bitstring(SCHEMA_no_constrain_bitstring(),
                                                                                 hex_val='ABCDEFABCDEF0123456789')),
    (SCHEMA_no_constrain_bitstring(), '7CABCDEFABCDEF0123456789ABCDEFABC0', DATA_bitstring(SCHEMA_no_constrain_bitstring(),
                                                                                           hex_val='ABCDEFABCDEF0123456789ABCDEFABC')),
    (SCHEMA_no_constrain_bitstring(), '8080ABCDEFABCDEF0123456789ABCDEFABC0', DATA_bitstring(SCHEMA_no_constrain_bitstring(),
                                                                                             hex_val='ABCDEFABCDEF0123456789ABCDEFABC0')),
    (SCHEMA_no_constrain_bitstring(), '80B0ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789', DATA_bitstring(SCHEMA_no_constrain_bitstring(),
                                                                                                         hex_val='ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789')),

])
def test_no_constrain_bitstring_as_hex_value_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_bitstring(lb=0, ub=0), '00', DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=0), bin_val='')),
])
def test_constrained_bitstring_of_zero_length_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_bitstring(lb=1, ub=1), '80', DATA_bitstring(SCHEMA_constrained_bitstring(lb=1, ub=1), bin_val='1')),
    (SCHEMA_constrained_bitstring(lb=1, ub=1), '00', DATA_bitstring(SCHEMA_constrained_bitstring(lb=1, ub=1), bin_val='0')),
    (SCHEMA_constrained_bitstring(lb=2, ub=2), '80', DATA_bitstring(SCHEMA_constrained_bitstring(lb=2, ub=2), bin_val='10')),
    (SCHEMA_constrained_bitstring(lb=2, ub=2), 'C0', DATA_bitstring(SCHEMA_constrained_bitstring(lb=2, ub=2), bin_val='11')),
    (SCHEMA_constrained_bitstring(lb=4, ub=4), 'A0', DATA_bitstring(SCHEMA_constrained_bitstring(lb=4, ub=4), bin_val='1010')),
    (SCHEMA_constrained_bitstring(lb=4, ub=4), '50', DATA_bitstring(SCHEMA_constrained_bitstring(lb=4, ub=4), bin_val='0101')),
    (SCHEMA_constrained_bitstring(lb=7, ub=7), 'AA', DATA_bitstring(SCHEMA_constrained_bitstring(lb=7, ub=7), bin_val='1010101')),
    (SCHEMA_constrained_bitstring(lb=7, ub=7), '54', DATA_bitstring(SCHEMA_constrained_bitstring(lb=7, ub=7), bin_val='0101010')),
    (SCHEMA_constrained_bitstring(lb=15, ub=15), 'CCCC', DATA_bitstring(SCHEMA_constrained_bitstring(lb=15, ub=15), bin_val='110011001100110')),
    (SCHEMA_constrained_bitstring(lb=15, ub=15), '3332', DATA_bitstring(SCHEMA_constrained_bitstring(lb=15, ub=15), bin_val='001100110011001')),
    (SCHEMA_constrained_bitstring(lb=16, ub=16), 'CCCC', DATA_bitstring(SCHEMA_constrained_bitstring(lb=16, ub=16), bin_val='1100110011001100')),
    (SCHEMA_constrained_bitstring(lb=16, ub=16), '3333', DATA_bitstring(SCHEMA_constrained_bitstring(lb=16, ub=16), bin_val='0011001100110011')),
    (SCHEMA_constrained_bitstring(lb=4, ub=4), 'A0', DATA_bitstring(SCHEMA_constrained_bitstring(lb=4, ub=4), hex_val='A')),
    (SCHEMA_constrained_bitstring(lb=8, ub=8), 'BB', DATA_bitstring(SCHEMA_constrained_bitstring(lb=8, ub=8), hex_val='BB')),
    (SCHEMA_constrained_bitstring(lb=12, ub=12), '1110', DATA_bitstring(SCHEMA_constrained_bitstring(lb=12, ub=12), hex_val='111')),
    (SCHEMA_constrained_bitstring(lb=16, ub=16), '2222', DATA_bitstring(SCHEMA_constrained_bitstring(lb=16, ub=16), hex_val='2222')),
])
def test_constrained_bitstring_same_length_gt_zero_and_le_16_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_bitstring(lb=17, ub=17), '333380', DATA_bitstring(SCHEMA_constrained_bitstring(lb=17, ub=17), bin_val='00110011001100111')),
    (SCHEMA_constrained_bitstring(lb=18, ub=18), '333340', DATA_bitstring(SCHEMA_constrained_bitstring(lb=18, ub=18), bin_val='001100110011001101')),
    (SCHEMA_constrained_bitstring(lb=19, ub=19), '333320', DATA_bitstring(SCHEMA_constrained_bitstring(lb=19, ub=19), bin_val='0011001100110011001')),
    (SCHEMA_constrained_bitstring(lb=20, ub=20), '333330', DATA_bitstring(SCHEMA_constrained_bitstring(lb=20, ub=20), bin_val='00110011001100110011')),
    (SCHEMA_constrained_bitstring(lb=21, ub=21), '333338', DATA_bitstring(SCHEMA_constrained_bitstring(lb=21, ub=21), bin_val='001100110011001100111')),
    (SCHEMA_constrained_bitstring(lb=22, ub=22), '333334', DATA_bitstring(SCHEMA_constrained_bitstring(lb=22, ub=22), bin_val='0011001100110011001101')),
    (SCHEMA_constrained_bitstring(lb=23, ub=23), '333332', DATA_bitstring(SCHEMA_constrained_bitstring(lb=23, ub=23), bin_val='00110011001100110011001')),
    (SCHEMA_constrained_bitstring(lb=24, ub=24), '333333', DATA_bitstring(SCHEMA_constrained_bitstring(lb=24, ub=24), bin_val='001100110011001100110011')),
    (SCHEMA_constrained_bitstring(lb=25, ub=25), '33333380', DATA_bitstring(SCHEMA_constrained_bitstring(lb=25, ub=25), bin_val='0011001100110011001100111')),
    (SCHEMA_constrained_bitstring(lb=128, ub=128), 'ABCDEFABCDEF0123456789ABCDEFABC0', DATA_bitstring(SCHEMA_constrained_bitstring(lb=128, ub=128),
                                                                                                      hex_val='ABCDEFABCDEF0123456789ABCDEFABC0')),
    (SCHEMA_constrained_bitstring(lb=176, ub=176), 'ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789', DATA_bitstring(SCHEMA_constrained_bitstring(lb=176, ub=176),
                                                                                                                  hex_val='ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789')),
])
def test_constrained_bitstring_same_length_gt_16_and_lt_64K_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_bitstring(lb=0, ub=1), '8080', DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=1), bin_val='1')),
    (SCHEMA_constrained_bitstring(lb=0, ub=15), '1080', DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=15), bin_val='1')),
    (SCHEMA_constrained_bitstring(lb=0, ub=15), 'F0E38E', DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=15), bin_val='111000111000111')),
    (SCHEMA_constrained_bitstring(lb=14, ub=15), '80E38E', DATA_bitstring(SCHEMA_constrained_bitstring(lb=14, ub=15), bin_val='111000111000111')),
    (SCHEMA_constrained_bitstring(lb=0, ub=127), '1EE38E', DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=127), bin_val='111000111000111')),
    (SCHEMA_constrained_bitstring(lb=0, ub=1000), '000FE38E', DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=1000), bin_val='111000111000111')),
    (SCHEMA_constrained_bitstring(lb=0, ub=10000), '000FE38E', DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=10000), bin_val='111000111000111')),
    (SCHEMA_constrained_bitstring(lb=0, ub=65535), '000FE38E', DATA_bitstring(SCHEMA_constrained_bitstring(lb=0, ub=65535), bin_val='111000111000111')),
])
def test_constrained_bitstring_with_ub_less_then_64K_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_ext_bitstring(lb=1, ub=1), '40', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=1, ub=1), bin_val='1')),
    (SCHEMA_constrained_ext_bitstring(lb=1, ub=1), '80077E', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=1, ub=1), bin_val='0111111')),
    (SCHEMA_constrained_ext_bitstring(lb=2, ub=2), '40', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=2, ub=2), bin_val='10')),
    (SCHEMA_constrained_ext_bitstring(lb=2, ub=2), '8003A0', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=2, ub=2), bin_val='101')),
    (SCHEMA_constrained_ext_bitstring(lb=7, ub=7), '800855', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=7, ub=7), bin_val='01010101')),
    (SCHEMA_constrained_ext_bitstring(lb=15, ub=15), '8011CCCD80', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=15, ub=15), bin_val='11001100110011011')),
    (SCHEMA_constrained_ext_bitstring(lb=16, ub=16), '8014333310', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=16, ub=16), bin_val='00110011001100110001')),
    (SCHEMA_constrained_ext_bitstring(lb=25, ub=25), '801C333333F0', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=25, ub=25), bin_val='0011001100110011001100111111')),
    (SCHEMA_constrained_ext_bitstring(lb=128, ub=128), '00ABCDEFABCDEF0123456789ABCDEFABC0', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=128, ub=128),
                                                                                                            hex_val='ABCDEFABCDEF0123456789ABCDEFABC0')),
    (SCHEMA_constrained_ext_bitstring(lb=176, ub=176), '00ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=176, ub=176),
                                                                                                                        hex_val='ABCDEFABCDEF0123456789ABCDEFABCDEF0123456789')),
    (SCHEMA_constrained_ext_bitstring(lb=0, ub=1), '4080', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=0, ub=1), bin_val='1')),
    (SCHEMA_constrained_ext_bitstring(lb=0, ub=15), '0880', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=0, ub=15), bin_val='1')),
    (SCHEMA_constrained_ext_bitstring(lb=0, ub=15), '78F0F0', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=0, ub=15), bin_val='111100001111000')),
    (SCHEMA_constrained_ext_bitstring(lb=0, ub=128), '4000ABCDEFABCDEF0123456789ABCDEFABC0', DATA_bitstring(SCHEMA_constrained_ext_bitstring(lb=0, ub=128),
                                                                                                            hex_val='ABCDEFABCDEF0123456789ABCDEFABC0')),
])
def test_constrained_bitstring_with_extension_marker_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value
