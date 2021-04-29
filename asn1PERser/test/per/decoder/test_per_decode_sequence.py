import pytest
from asn1PERser.codec.per.decoder import decode as per_decoder
from asn1PERser.test.per.encoder.test_per_encode_sequence import  \
    DATA_simple_seq, DATA_bool_seq, SCHEMA_two_elem_seq_with_extension_marker_present_or_not, \
    SCHEMA_seq_with_only_extension_marker_present_or_not, SCHEMA_seq_with_elements_in_extension_addition, \
    SCHEMA_seq_with_some_optional_elements_in_root, SCHEMA_seq_with_only_optional_elements_in_root, \
    SCHEMA_seq_with_default_elements_in_root, SCHEMA_sequence_of_boolean, DATA_octet_seq, SCHEMA_sequence_of_octetstring, \
    SCHEMA_sequence_of_bitstring, DATA_bitstring_seq, DATA_enumerated_seq, SCHEMA_sequence_of_enumerated, \
    SCHEMA_sequence_with_extension_addition_groups_1, SCHEMA_sequence_with_extension_addition_groups_2, \
    SCHEMA_sequence_with_extension_addition_groups_3, DATA_extension_addition_groups_seq


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_two_elem_seq_with_extension_marker_present_or_not(extensionMarker_value=False), '0300870702FCB3',
        DATA_simple_seq(SCHEMA_two_elem_seq_with_extension_marker_present_or_not, i0_is=True,
                        i1_is=True, i2_is=False, i3_is=False, i4_is=False, ext_mark=False)),
    (SCHEMA_two_elem_seq_with_extension_marker_present_or_not(extensionMarker_value=True), '000300870702FCB3',
        DATA_simple_seq(SCHEMA_two_elem_seq_with_extension_marker_present_or_not, i0_is=True,
                        i1_is=True, i2_is=False, i3_is=False, i4_is=False, ext_mark=True)),
    (SCHEMA_seq_with_only_extension_marker_present_or_not(extensionMarker_value=False), '0300870702FCB300178003030D4028',
        DATA_simple_seq(SCHEMA_seq_with_only_extension_marker_present_or_not, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=True, i4_is=True, ext_mark=False)),
    (SCHEMA_seq_with_only_extension_marker_present_or_not(extensionMarker_value=True), '000300870702FCB300178003030D4028',
        DATA_simple_seq(SCHEMA_seq_with_only_extension_marker_present_or_not, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=True, i4_is=True, ext_mark=True)),

])
def test_no_extension_no_default_no_optional_components_present_sequence_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value=True), '800300870707E00302FCB3020017058003030D400128',
        DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=True, i4_is=True, ext_mark=True)),
    (SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value=True), '800300870707C00302FCB3020017058003030D40',
        DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=True, i4_is=False, ext_mark=True)),
    (SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value=True), '800300870707800302FCB3020017',
        DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=False, i4_is=False, ext_mark=True)),
    (SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value=True), '800300870707000302FCB3',
        DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,
                        i1_is=True, i2_is=False, i3_is=False, i4_is=False, ext_mark=True)),
])
def test_extension_components_are_present_but_no_default_no_optional_sequence_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_seq_with_some_optional_elements_in_root(extensionMarker_value=False), '0003008707001728',
        DATA_simple_seq(SCHEMA_seq_with_some_optional_elements_in_root, i0_is=True,
                        i1_is=False, i2_is=True, i3_is=False, i4_is=True)),
    (SCHEMA_seq_with_some_optional_elements_in_root(extensionMarker_value=False), '800300870702FCB3001728',
        DATA_simple_seq(SCHEMA_seq_with_some_optional_elements_in_root, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=False, i4_is=True)),
    (SCHEMA_seq_with_some_optional_elements_in_root(extensionMarker_value=False), '400300870700178003030D4028',
        DATA_simple_seq(SCHEMA_seq_with_some_optional_elements_in_root, i0_is=True,
                        i1_is=False, i2_is=True, i3_is=True, i4_is=True)),
    (SCHEMA_seq_with_some_optional_elements_in_root(extensionMarker_value=False), 'C00300870702FCB300178003030D4028',
        DATA_simple_seq(SCHEMA_seq_with_some_optional_elements_in_root, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=True, i4_is=True)),
    (SCHEMA_seq_with_only_optional_elements_in_root(extensionMarker_value=False), 'C00300870702FCB3',
        DATA_simple_seq(SCHEMA_seq_with_only_optional_elements_in_root, i0_is=True,
                        i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_seq_with_only_optional_elements_in_root(extensionMarker_value=False), '8003008707',
        DATA_simple_seq(SCHEMA_seq_with_only_optional_elements_in_root, i0_is=True,
                        i1_is=False, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_seq_with_only_optional_elements_in_root(extensionMarker_value=False), '4002FCB3',
        DATA_simple_seq(SCHEMA_seq_with_only_optional_elements_in_root, i0_is=False,
                        i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_seq_with_only_optional_elements_in_root(extensionMarker_value=False), '00',
        DATA_simple_seq(SCHEMA_seq_with_only_optional_elements_in_root, i0_is=False,
                        i1_is=False, i2_is=False, i3_is=False, i4_is=False)),
])
def test_optional_components_present_in_extension_root_sequence_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_seq_with_default_elements_in_root(extensionMarker_value=False), '0003008707001728',
        DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True,
                        i1_is=False, i2_is=True, i3_is=False, i4_is=True)),
    (SCHEMA_seq_with_default_elements_in_root(extensionMarker_value=False), '800300870702FCB3001728',
        DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=False, i4_is=True)),
    (SCHEMA_seq_with_default_elements_in_root(extensionMarker_value=False), '400300870700178003030D4028',
        DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True,
                        i1_is=False, i2_is=True, i3_is=True, i4_is=True)),
    (SCHEMA_seq_with_default_elements_in_root(extensionMarker_value=False), 'C00300870702FCB300178003030D4028',
        DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=True, i4_is=True)),
])
def test_default_components_with_none_default_values_present_in_extension_root_sequence_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_seq_with_default_elements_in_root(extensionMarker_value=False), '0003008707001728',    # no other test is needed here
        DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True,                      # as default values are never encoded
                        i1_is=False, i2_is=True, i3_is=False, i4_is=True)),                        # so they never will be decoded
])
def test_default_components_with_default_values_present_in_filled_schema_are_not_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value=True), '0003008707',
        DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,
                        i1_is=False, i2_is=False, i3_is=False, i4_is=False, ext_mark=True)),
    (SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value=True), '800300870707000302FCB3',
        DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,
                        i1_is=True, i2_is=False, i3_is=False, i4_is=False, ext_mark=True)),
    (SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value=True), '800300870707800302FCB3020017',
        DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=False, i4_is=False, ext_mark=True)),
    (SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value=True), '800300870707C00302FCB3020017058003030D40',
        DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=True, i4_is=False, ext_mark=True)),
    (SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value=True), '800300870707E00302FCB3020017058003030D400128',
        DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,
                        i1_is=True, i2_is=True, i3_is=True, i4_is=True, ext_mark=True)),
])
def test_elements_in_extension_addition_may_not_be_present_even_if_no_optional_in_schema_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_sequence_of_boolean(), '0000', DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=False, addition_present=False)),
    (SCHEMA_sequence_of_boolean(), '0001', DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=False, addition_present=False)),    # Other version
    (SCHEMA_sequence_of_boolean(), '001F', DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=False, addition_present=False)),    # Other version
    (SCHEMA_sequence_of_boolean(), '7FE0', DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=True, addition_present=False)),
    (SCHEMA_sequence_of_boolean(), '7FFF', DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=True, addition_present=False)),     # Other version
    (SCHEMA_sequence_of_boolean(), '8002BFF801000100010001000100010001000100010001000100',
        DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=False, addition_present=True, addition_val=False)),
    (SCHEMA_sequence_of_boolean(), '8002BFF801800180018001800180018001800180018001800180',
        DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=False, addition_present=True, addition_val=True)),
    (SCHEMA_sequence_of_boolean(), 'FFE2BFF801000100010001000100010001000100010001000100',
        DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=True, addition_present=True, addition_val=False)),
    (SCHEMA_sequence_of_boolean(), 'FFE2BFF801800180018001800180018001800180018001800180',
        DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=True, addition_present=True, addition_val=True)),
])
def test_sequence_of_boolean_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_sequence_of_octetstring(), 'E002DEAD02BEEF00ABCD01AA02BBB002CCCC03DDDDD0',
        DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=True, o4_is=True, o5_is=True)),
    (SCHEMA_sequence_of_octetstring(), '6002DEAD00ABCD01AA02BBB002CCCC03DDDDD0',
        DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=False, o4_is=True, o5_is=True)),
    (SCHEMA_sequence_of_octetstring(), 'A002DEAD02BEEF00ABCD01AA02CCCC03DDDDD0',
        DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=True, o4_is=False, o5_is=True)),
    (SCHEMA_sequence_of_octetstring(), 'C002DEAD02BEEF00ABCD01AA02BBB003DDDDD0',
        DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=True, o4_is=True, o5_is=False)),
    (SCHEMA_sequence_of_octetstring(), '2002DEAD00ABCD01AA02CCCC03DDDDD0',
        DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=False, o4_is=False, o5_is=True)),
    (SCHEMA_sequence_of_octetstring(), '4002DEAD00ABCD01AA02BBB003DDDDD0',
        DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=False, o4_is=True, o5_is=False)),
    (SCHEMA_sequence_of_octetstring(), '8002DEAD02BEEF00ABCD01AA03DDDDD0',
        DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=True, o4_is=False, o5_is=False)),
    (SCHEMA_sequence_of_octetstring(), '0002DEAD00ABCD01AA03DDDDD0',
        DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=False, o4_is=False, o5_is=False)),
])
def test_sequence_of_octetstring_no_extension_marker_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_sequence_of_bitstring(), 'F00CF0F010DEAD10BEEF10ABCDF810FEED0014F0F0F0F0F010BBBB14CCCCC05C0280C003F0F0F00418DDDDDD',
        DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=True, b3_is=True, b9_is=True)),
    (SCHEMA_sequence_of_bitstring(), 'B00CF0F010DEAD10ABCDF810FEED0014F0F0F0F0F010BBBB14CCCCC05C0280C003F0F0F00418DDDDDD',
        DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=False, b3_is=True, b9_is=True)),
    (SCHEMA_sequence_of_bitstring(), 'D00CF0F010DEAD10BEEFF810FEED0014F0F0F0F0F010BBBB14CCCCC05C0280C003F0F0F00418DDDDDD',
        DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=True, b3_is=False, b9_is=True)),
    (SCHEMA_sequence_of_bitstring(), 'F00CF0F010DEAD10BEEF10ABCDF810FEED0014F0F0F0F0F010BBBB14CCCCC04C03F0F0F00418DDDDDD',
        DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=True, b3_is=True, b9_is=False)),
    (SCHEMA_sequence_of_bitstring(), '900CF0F010DEADF810FEED0014F0F0F0F0F010BBBB14CCCCC05C0280C003F0F0F00418DDDDDD',
        DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=False, b3_is=False, b9_is=True)),
    (SCHEMA_sequence_of_bitstring(), 'B00CF0F010DEAD10ABCDF810FEED0014F0F0F0F0F010BBBB14CCCCC04C03F0F0F00418DDDDDD',
        DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=False, b3_is=True, b9_is=False)),
    (SCHEMA_sequence_of_bitstring(), 'D00CF0F010DEAD10BEEFF810FEED0014F0F0F0F0F010BBBB14CCCCC04C03F0F0F00418DDDDDD',
        DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=True, b3_is=False, b9_is=False)),
    (SCHEMA_sequence_of_bitstring(), '900CF0F010DEADF810FEED0014F0F0F0F0F010BBBB14CCCCC04C03F0F0F00418DDDDDD',
        DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=False, b3_is=False, b9_is=False)),
])
def test_sequence_of_bitstring_with_extension_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_sequence_of_enumerated(), 'EC0A80E001800100', DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=True, e3_is=True, e4_is=True)),
    (SCHEMA_sequence_of_enumerated(), 'AA80E001800100', DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=False, e3_is=True, e4_is=True)),
    (SCHEMA_sequence_of_enumerated(), 'CC0A0701800100', DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=True, e3_is=False, e4_is=True)),
    (SCHEMA_sequence_of_enumerated(), 'EC0A80A00100', DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=True, e3_is=True, e4_is=False)),
    (SCHEMA_sequence_of_enumerated(), '8A0701800100', DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=False, e3_is=False, e4_is=True)),
    (SCHEMA_sequence_of_enumerated(), 'AA80A00100', DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=False, e3_is=True, e4_is=False)),
    (SCHEMA_sequence_of_enumerated(), 'CC0A050100', DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=True, e3_is=False, e4_is=False)),
    (SCHEMA_sequence_of_enumerated(), '8A050100', DATA_enumerated_seq(SCHEMA_sequence_of_enumerated,  e1_is=False, e3_is=False, e4_is=False)),
])
def test_sequence_of_enumerated_with_extension_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_sequence_with_extension_addition_groups_1(), '00019901AA', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_1, s0='99', s1='AA')),
    (SCHEMA_sequence_with_extension_addition_groups_1(), '80019901AA07000401BB01CC', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_1, s0='99', s1='AA', s2='BB', s3='CC')),
    (SCHEMA_sequence_with_extension_addition_groups_1(), '80019901AA07800401BB01CC0201DD', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_1, s0='99', s1='AA', s2='BB', s3='CC', s4='DD')),
    (SCHEMA_sequence_with_extension_addition_groups_1(), '80019901AA07C00401BB01CC0201DD0201EE', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_1, s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE')),
    (SCHEMA_sequence_with_extension_addition_groups_1(), '80019901AA07E00401BB01CC0201DD0201EE0201FF', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_1, s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE', s6='FF')),
    (SCHEMA_sequence_with_extension_addition_groups_2(), '000199', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_2, s0='99')),
    (SCHEMA_sequence_with_extension_addition_groups_2(), '80019905000201AA', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_2, s0='99', s1='AA')),
    (SCHEMA_sequence_with_extension_addition_groups_2(), '80019905800201AA038001BB', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_2, s0='99', s1='AA', s2='BB')),
    (SCHEMA_sequence_with_extension_addition_groups_2(), '80019905800201AA034001CC', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_2, s0='99', s1='AA', s3='CC')),
    (SCHEMA_sequence_with_extension_addition_groups_2(), '80019905800201AA05C001BB01CC', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_2, s0='99', s1='AA', s2='BB', s3='CC')),
    (SCHEMA_sequence_with_extension_addition_groups_2(), '80019905C00201AA05C001BB01CC078001DD01EE01FF', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_2, s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE', s6='FF')),
    (SCHEMA_sequence_with_extension_addition_groups_2(), '80019905C00201AA05C001BB01CC050001DD01FF', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_2, s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s6='FF')),
    (SCHEMA_sequence_with_extension_addition_groups_2(), '80019905400201AA078001DD01EE01FF', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_2, s0='99', s1='AA', s4='DD', s5='EE', s6='FF')),
    (SCHEMA_sequence_with_extension_addition_groups_2(), '80019905400201AA050001DD01FF', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_2, s0='99', s1='AA', s4='DD', s6='FF')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '000199', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '80019907000201AA', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99', s1='AA')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '80019907800201AA0201BB', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99', s1='AA', s2='BB')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '80019906800201BB', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99', s2='BB')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '80019907C00201AA0201BB050001CC01DD', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99', s1='AA', s2='BB', s3='CC', s4='DD')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '80019907C00201AA0201BB078001CC01DD01EE', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '80019907E00201AA0201BB078001CC01DD01EE038001FF', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE', s6='FF')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '80019907E00201AA0201BB050001CC01DD038001FF', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s6='FF')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '80019906E00201BB050001CC01DD038001FF', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99', s2='BB', s3='CC', s4='DD', s6='FF')),
    (SCHEMA_sequence_with_extension_addition_groups_3(), '80019906C00201BB050001CC01DD', DATA_extension_addition_groups_seq(
        SCHEMA_sequence_with_extension_addition_groups_3, s0='99', s2='BB', s3='CC', s4='DD')),
])
def test_sequence_with_extension_addition_groups_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema) == value