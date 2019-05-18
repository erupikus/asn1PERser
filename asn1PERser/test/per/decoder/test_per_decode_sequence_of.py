import pytest
from asn1PERser.codec.per.decoder import decode as per_decoder
from asn1PERser.test.per.encoder.test_per_encode_sequence_of import SCHEMA_constrained_seq_of_no_extension, \
    SCHEMA_constrained_seq_of_extension_present, SCHEMA_no_constrains_sequence_of, DATA_seq_of


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_no_constrains_sequence_of(), '00',
        DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=False, i1_is=False, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_no_constrains_sequence_of(), '0103008707',
        DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_no_constrains_sequence_of(), '020300870702FCB3',
        DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_no_constrains_sequence_of(), '030300870702FCB30117',
        DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False)),
    (SCHEMA_no_constrains_sequence_of(), '040300870702FCB3011703030D40',
        DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False)),
    (SCHEMA_no_constrains_sequence_of(), '050300870702FCB3011703030D400105',
        DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True)),
])
def test_no_constrains_sequence_of_integer_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytes.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_seq_of_no_extension(lb=0, ub=2), '4003008707',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=0, ub=2), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_no_extension(lb=0, ub=2), '800300870702FCB3',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=0, ub=2), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), '000300870702FCB3',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), '400300870702FCB30117',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), '800300870702FCB3011703030D40',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False)),
    (SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), 'C00300870702FCB3011703030D400105',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True)),
])
def test_constrained_sequence_of_no_extension_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytes.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_seq_of_no_extension(lb=1, ub=1), '03008707',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=1, ub=1), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_no_extension(lb=2, ub=2), '0300870702FCB3',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=2), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_no_extension(lb=3, ub=3), '0300870702FCB30117',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=3, ub=3), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_no_extension(lb=4, ub=4), '0300870702FCB3011703030D40',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=4, ub=4), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False)),
    (SCHEMA_constrained_seq_of_no_extension(lb=5, ub=5), '0300870702FCB3011703030D400105',
        DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=5, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True)),
])
def test_constrained_sequence_of_of_fixed_length_no_extension_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytes.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_seq_of_extension_present(lb=0, ub=2), '2003008707',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=2), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=0, ub=2), '400300870702FCB3',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=2), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), '000300870702FCB3',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), '200300870702FCB30117',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), '400300870702FCB3011703030D40',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), '600300870702FCB3011703030D400105',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True)),
])
def test_constrained_sequence_of_with_extension_and_num_of_elems_is_within_extension_root_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytes.fromhex(encoded), asn1Spec=schema) == value


@pytest.mark.parametrize("schema, encoded, value", [
    (SCHEMA_constrained_seq_of_extension_present(lb=0, ub=0), '800103008707',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=0), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=0, ub=0), '80020300870702FCB3',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=0), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=0, ub=0), '80030300870702FCB30117',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=0), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=1, ub=1), '80020300870702FCB3',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=1, ub=1), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=1, ub=1), '80050300870702FCB3011703030D400105',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=1, ub=1), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True)),
    (SCHEMA_constrained_seq_of_extension_present(lb=1, ub=3), '80040300870702FCB3011703030D40',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=1, ub=3), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False)),
    (SCHEMA_constrained_seq_of_extension_present(lb=1, ub=3), '80050300870702FCB3011703030D400105',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=1, ub=3), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True)),
    (SCHEMA_constrained_seq_of_extension_present(lb=3, ub=4), '80050300870702FCB3011703030D400105',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=3, ub=4), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True)),
    (SCHEMA_constrained_seq_of_extension_present(lb=3, ub=4), '800103008707',
        DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=3, ub=4), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False)),
])
def test_constrained_sequence_of_with_extension_and_num_of_elems_is_not_within_extension_root_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytes.fromhex(encoded), asn1Spec=schema) == value
