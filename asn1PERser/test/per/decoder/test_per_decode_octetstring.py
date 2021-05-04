import pytest
from asn1PERser.codec.per.decoder import decode as per_decoder
from asn1PERser.test.per.encoder.test_per_encode_octetstring import SCHEMA_constrained_ext_octetstring, \
    SCHEMA_constrained_octetstring, SCHEMA_no_constrain_octetstring, DATA_octetstring


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_no_constrain_octetstring(), '0180', DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='1')),
    (SCHEMA_no_constrain_octetstring(), '0100', DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='0')),
    (SCHEMA_no_constrain_octetstring(), '0140', DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='01')),
    (SCHEMA_no_constrain_octetstring(), '0180', DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='10')),
    (SCHEMA_no_constrain_octetstring(), '01F0', DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='1111')),
    (SCHEMA_no_constrain_octetstring(), '01F0', DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='111100')),
    (SCHEMA_no_constrain_octetstring(), '02F0F0', DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='1111000011110')),
    (SCHEMA_no_constrain_octetstring(), '020C33', DATA_octetstring(SCHEMA_no_constrain_octetstring(), bin_val='0000110000110011')),
    (SCHEMA_no_constrain_octetstring(), '075CB35B6E395CA8', DATA_octetstring(SCHEMA_no_constrain_octetstring(),
                                                                             bin_val='01011100101100110101101101101110001110010101110010101')),
])
def test_no_constrain_octetstring_as_binary_value_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_no_constrain_octetstring(), '0100', DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='0')),
    (SCHEMA_no_constrain_octetstring(), '0110', DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='1')),
    (SCHEMA_no_constrain_octetstring(), '0101', DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='01')),
    (SCHEMA_no_constrain_octetstring(), '0110', DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='10')),
    (SCHEMA_no_constrain_octetstring(), '0200A0', DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='00A')),
    (SCHEMA_no_constrain_octetstring(), '02AA00', DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='AA0')),
    (SCHEMA_no_constrain_octetstring(), '04ABCDEFA0', DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='ABCDEFA')),
    (SCHEMA_no_constrain_octetstring(), '080123ABCDEFA01230', DATA_octetstring(SCHEMA_no_constrain_octetstring(), hex_val='0123ABCDEFA0123')),
])
def test_no_constrain_octetstring_as_hex_value_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    # (SCHEMA_constrained_octetstring(lb=0, ub=0), '00', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=0), bin_val='')),    # does not work
    (SCHEMA_constrained_octetstring(lb=0, ub=0), '00', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=0), hex_val='')),
])
def test_constrained_octetstring_of_zero_length_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_octetstring(lb=1, ub=1), '80', DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), bin_val='1')),
    (SCHEMA_constrained_octetstring(lb=1, ub=1), '70', DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), bin_val='01110')),
    (SCHEMA_constrained_octetstring(lb=1, ub=1), '0F', DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), bin_val='00001111')),
    (SCHEMA_constrained_octetstring(lb=1, ub=1), 'C0', DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), hex_val='C')),
    (SCHEMA_constrained_octetstring(lb=1, ub=1), 'CF', DATA_octetstring(SCHEMA_constrained_octetstring(lb=1, ub=1), hex_val='CF')),
    (SCHEMA_constrained_octetstring(lb=2, ub=2), 'FF00', DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), bin_val='111111110')),
    (SCHEMA_constrained_octetstring(lb=2, ub=2), '0F08', DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), bin_val='0000111100001')),
    (SCHEMA_constrained_octetstring(lb=2, ub=2), 'CCCC', DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), bin_val='1100110011001100')),
    (SCHEMA_constrained_octetstring(lb=2, ub=2), 'ABC0', DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), hex_val='ABC')),
    (SCHEMA_constrained_octetstring(lb=2, ub=2), '0000', DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), hex_val='000')),
    (SCHEMA_constrained_octetstring(lb=2, ub=2), '0000', DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), hex_val='0000')),
    (SCHEMA_constrained_octetstring(lb=2, ub=2), 'FFFF', DATA_octetstring(SCHEMA_constrained_octetstring(lb=2, ub=2), hex_val='FFFF')),
])
def test_constrained_same_len_octetstring_with_len_le_2_octetes_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_octetstring(lb=3, ub=3), '010101', DATA_octetstring(SCHEMA_constrained_octetstring(lb=3, ub=3), bin_val='000000010000000100000001')),
    (SCHEMA_constrained_octetstring(lb=3, ub=3), 'ABCDEF', DATA_octetstring(SCHEMA_constrained_octetstring(lb=3, ub=3), hex_val='ABCDEF')),
    (SCHEMA_constrained_octetstring(lb=4, ub=4), '7FFFFF00', DATA_octetstring(SCHEMA_constrained_octetstring(lb=4, ub=4), bin_val='01111111111111111111111100000000')),
    (SCHEMA_constrained_octetstring(lb=4, ub=4), 'ABCDEF01', DATA_octetstring(SCHEMA_constrained_octetstring(lb=4, ub=4), hex_val='ABCDEF01')),
    (SCHEMA_constrained_octetstring(lb=17, ub=17), '11223344556677889900AABBCCDDEEFF11', DATA_octetstring(SCHEMA_constrained_octetstring(lb=17, ub=17),
                                                                                                          hex_val='11223344556677889900AABBCCDDEEFF11')),
])
def test_constrained_same_len_octetstring_with_len_gt_2_and_lt_64K_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_octetstring(lb=0, ub=15), '00', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=15), hex_val='')),
    (SCHEMA_constrained_octetstring(lb=0, ub=15), '10A0', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=15), hex_val='A')),
    (SCHEMA_constrained_octetstring(lb=0, ub=15), '10A0', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=15), hex_val='A0')),
    (SCHEMA_constrained_octetstring(lb=0, ub=15), 'F0112233445566778899001122334455', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=15),
                                                                                                       hex_val='112233445566778899001122334455')),
    (SCHEMA_constrained_octetstring(lb=0, ub=22), '08A0', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=22), hex_val='A')),
    (SCHEMA_constrained_octetstring(lb=0, ub=22), '08A0', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=22), hex_val='A0')),
    (SCHEMA_constrained_octetstring(lb=0, ub=22), '78112233445566778899001122334455', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=22),
                                                                                                       hex_val='112233445566778899001122334455')),
    (SCHEMA_constrained_octetstring(lb=0, ub=22), 'B011223344556677889900112233445566778899001122', DATA_octetstring(SCHEMA_constrained_octetstring(lb=0, ub=22),
                                                                                                                     hex_val='11223344556677889900112233445566778899001122')),
    (SCHEMA_constrained_octetstring(lb=10, ub=15), '00112233445566778899AA', DATA_octetstring(SCHEMA_constrained_octetstring(lb=10, ub=15),
                                                                                              hex_val='112233445566778899AA')),
    (SCHEMA_constrained_octetstring(lb=10, ub=15), 'A0112233445566778899AABBCCDDEEFF', DATA_octetstring(SCHEMA_constrained_octetstring(lb=10, ub=15),
                                                                                                        hex_val='112233445566778899AABBCCDDEEFF')),
    (SCHEMA_constrained_octetstring(lb=10, ub=22), '00112233445566778899AA', DATA_octetstring(SCHEMA_constrained_octetstring(lb=10, ub=22),
                                                                                              hex_val='112233445566778899AA')),
    (SCHEMA_constrained_octetstring(lb=10, ub=22), 'B0112233445566778899AABBCCDDEEFF001122334455', DATA_octetstring(SCHEMA_constrained_octetstring(lb=10, ub=22),
                                                                                                                    hex_val='112233445566778899AABBCCDDEEFF001122334455')),
])
def test_constrained_different_len_octet_string_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=0), '00', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=0), hex_val='')),
    (SCHEMA_constrained_ext_octetstring(lb=1, ub=1), '5000', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=1, ub=1), hex_val='A')),
    (SCHEMA_constrained_ext_octetstring(lb=1, ub=1), '5580', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=1, ub=1), hex_val='AB')),
    (SCHEMA_constrained_ext_octetstring(lb=5, ub=5), '001122334450', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=5, ub=5), hex_val='112233445')),
    (SCHEMA_constrained_ext_octetstring(lb=5, ub=5), '001122334455', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=5, ub=5), hex_val='1122334455')),
    (SCHEMA_constrained_ext_octetstring(lb=15, ub=15), '00112233445566778899001122334455', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=15, ub=15),
                                                                                                            hex_val='112233445566778899001122334455')),
    (SCHEMA_constrained_ext_octetstring(lb=22, ub=22), '0011223344556677889900112233445566778899001122', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=22, ub=22),
                                                                                                                          hex_val='11223344556677889900112233445566778899001122')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=2), '00', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val='')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=2), '20A0', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val='A')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=2), '20AB', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val='AB')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=2), '40ABC0', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val='ABC')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=2), '40ABCD', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=2), hex_val='ABCD')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=15), '08A0', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=15), hex_val='A')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=15), '08AB', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=15), hex_val='AB')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=15), '48112233445566778899', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=15),
                                                                                               hex_val='112233445566778899')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=15), '78112233445566778899AABBCCDDEEFF', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=15),
                                                                                                           hex_val='112233445566778899AABBCCDDEEFF')),
])
def test_constrained_with_extension_when_len_is_within_extension_root_octetstring_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=0), '8001A0', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=0), hex_val='A')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=0), '8001AB', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=0), hex_val='AB')),
    (SCHEMA_constrained_ext_octetstring(lb=0, ub=0), '80051122334455', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=0, ub=0), hex_val='1122334455')),
    (SCHEMA_constrained_ext_octetstring(lb=2, ub=2), '8000', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val='')),
    (SCHEMA_constrained_ext_octetstring(lb=2, ub=2), '8001A0', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val='A')),
    (SCHEMA_constrained_ext_octetstring(lb=2, ub=2), '8001AB', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val='AB')),
    (SCHEMA_constrained_ext_octetstring(lb=2, ub=2), '8003112233', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val='112233')),
    (SCHEMA_constrained_ext_octetstring(lb=2, ub=2), '80051122334455', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=2, ub=2), hex_val='1122334455')),
    (SCHEMA_constrained_ext_octetstring(lb=3, ub=4), '8000', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='')),
    (SCHEMA_constrained_ext_octetstring(lb=3, ub=4), '8001A0', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='A')),
    (SCHEMA_constrained_ext_octetstring(lb=3, ub=4), '8001AB', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='AB')),
    (SCHEMA_constrained_ext_octetstring(lb=3, ub=4), '80021122', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='1122')),
    (SCHEMA_constrained_ext_octetstring(lb=3, ub=4), '80051122334455', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='1122334455')),
    (SCHEMA_constrained_ext_octetstring(lb=3, ub=4), '800711223344556677', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=3, ub=4), hex_val='11223344556677')),
    (SCHEMA_constrained_ext_octetstring(lb=10, ub=22), '8009112233445566778899', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=10, ub=22), hex_val='112233445566778899')),
    (SCHEMA_constrained_ext_octetstring(lb=10, ub=22), '80171122334455667788990011223344556677889900112233', DATA_octetstring(SCHEMA_constrained_ext_octetstring(lb=10, ub=22),
                                                                                                                              hex_val='1122334455667788990011223344556677889900112233')),
])
def test_constrained_with_extension_when_len_is_NOT_within_extension_root_octetstring_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value
