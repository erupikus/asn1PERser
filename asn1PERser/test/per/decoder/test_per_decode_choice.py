import pytest
from asn1PERser.codec.per.decoder import decode as per_decoder
from asn1PERser.test.per.encoder.test_per_encode_choice import SCHEMA_single_item_choice, SCHEMA_no_extension_simple_choice, \
    SCHEMA_reverse_no_extension_simple_choice, SCHEMA_reverse_with_extension_simple_choice, \
    SCHEMA_selected_choice_from_extension_addition_more_elems, SCHEMA_selected_choice_from_extension_addition_one_elem, \
    SCHEMA_single_item_choice_with_extension, SCHEMA_with_extension_simple_choice, SCHEMA_selected_choice_from_extension_addition_groups_1, \
    SCHEMA_selected_choice_from_extension_addition_groups_2, DATA_choice


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_single_item_choice(), '010A', DATA_choice(SCHEMA_single_item_choice(), identifier='i0', value=10)),
    (SCHEMA_single_item_choice(), '030186A0', DATA_choice(SCHEMA_single_item_choice(), identifier='i0', value=100000)),
    (SCHEMA_no_extension_simple_choice(), '00010A', DATA_choice(SCHEMA_no_extension_simple_choice(), identifier='i0', value=10)),
    (SCHEMA_no_extension_simple_choice(), '00030186A0', DATA_choice(SCHEMA_no_extension_simple_choice(), identifier='i0', value=100000)),
    (SCHEMA_no_extension_simple_choice(), '80010A', DATA_choice(SCHEMA_no_extension_simple_choice(), identifier='i1', value=10)),
    (SCHEMA_no_extension_simple_choice(), '80030186A0', DATA_choice(SCHEMA_no_extension_simple_choice(), identifier='i1', value=100000)),
    (SCHEMA_reverse_no_extension_simple_choice(), '80010A', DATA_choice(SCHEMA_reverse_no_extension_simple_choice(), identifier='i0', value=10)),
    (SCHEMA_reverse_no_extension_simple_choice(), '80030186A0', DATA_choice(SCHEMA_reverse_no_extension_simple_choice(), identifier='i0', value=100000)),
    (SCHEMA_reverse_no_extension_simple_choice(), '00010A', DATA_choice(SCHEMA_reverse_no_extension_simple_choice(), identifier='i1', value=10)),
    (SCHEMA_reverse_no_extension_simple_choice(), '00030186A0', DATA_choice(SCHEMA_reverse_no_extension_simple_choice(), identifier='i1', value=100000)),
])
def test_no_extension_marker_choice_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_single_item_choice_with_extension(), '000108', DATA_choice(SCHEMA_single_item_choice_with_extension(), identifier='i0', value=8)),
    (SCHEMA_single_item_choice_with_extension(), '0003010B90', DATA_choice(SCHEMA_single_item_choice_with_extension(), identifier='i0', value=68496)),
    (SCHEMA_with_extension_simple_choice(), '0002FF7E', DATA_choice(SCHEMA_with_extension_simple_choice(), identifier='i0', value=-130)),
    (SCHEMA_with_extension_simple_choice(), '00025B9F', DATA_choice(SCHEMA_with_extension_simple_choice(), identifier='i0', value=23455)),
    (SCHEMA_with_extension_simple_choice(), '4001FF', DATA_choice(SCHEMA_with_extension_simple_choice(), identifier='i1', value=-1)),
    (SCHEMA_with_extension_simple_choice(), '4003FE7960', DATA_choice(SCHEMA_with_extension_simple_choice(), identifier='i0', value=-100000)),
    (SCHEMA_reverse_with_extension_simple_choice(), '40010A', DATA_choice(SCHEMA_reverse_with_extension_simple_choice(), identifier='i0', value=10)),
    (SCHEMA_reverse_with_extension_simple_choice(), '40030186A0', DATA_choice(SCHEMA_reverse_with_extension_simple_choice(), identifier='i0', value=100000)),
    (SCHEMA_reverse_with_extension_simple_choice(), '00010A', DATA_choice(SCHEMA_reverse_with_extension_simple_choice(), identifier='i1', value=10)),
    (SCHEMA_reverse_with_extension_simple_choice(), '00030186A0', DATA_choice(SCHEMA_reverse_with_extension_simple_choice(), identifier='i1', value=100000)),
])
def test_only_extension_marker_preset_choice_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '00010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i0', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '04010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i1', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '0C010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i3', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '18010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i6', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '24010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i9', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '30010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i12', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '3C010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i15', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '40010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i16', value=10)),
])
def test_extension_present_but_choice_from_root_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_selected_choice_from_extension_addition_one_elem(), '8002010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_one_elem(), identifier='i2', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_one_elem(), '800302F830',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_one_elem(), identifier='i2', value=-2000)),
    (SCHEMA_selected_choice_from_extension_addition_one_elem(), '8102010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_one_elem(), identifier='i3', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_one_elem(), '810302F830',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_one_elem(), identifier='i3', value=-2000)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '80020100',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i17', value=0)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '8002010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i17', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '810201F6',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i18', value=-10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '8202010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i19', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '8502010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i22', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '8702010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i24', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '8902010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i26', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '8C02010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i29', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '9002010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i33', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '9102010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i34', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_more_elems(), '9202010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i35', value=10)),
])
def test_choice_from_extension_addition_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '00010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i0', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '40010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i1', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '8002010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i2', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '8102010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i3', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '8202010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i4', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '8302010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i5', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '8402010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i6', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '8502010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i7', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '8602010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i8', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_1(), '8702010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i9', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_2(), '00010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i0', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_2(), '40010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i1', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_2(), '8002010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i5', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_2(), '8102010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i7', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_2(), '8202010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i8', value=10)),
    (SCHEMA_selected_choice_from_extension_addition_groups_2(), '8302010A',
        DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i9', value=10)),
])
def test_choice_from_extension_addition_groups_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytearray.fromhex(encoded), asn1Spec=schema()) == value
