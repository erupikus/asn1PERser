import pytest
from asn1PERser.codec.per.encoder import encode as per_encoder
from asn1PERser.codec.per.encoder import SizeConstrainViolated, InvalidComponentIndexIntoStructuredType
from asn1PERser.classes.data.builtin.SequenceOfType import SequenceOfType
from asn1PERser.classes.data.builtin.IntegerType import IntegerType
from asn1PERser.classes.types.constraint import SequenceOfValueSize


I0_VAL = 34567
I1_VAL = -845
I2_VAL = 23
I3_VAL = 200000
I4_VAL = 5


def SCHEMA_no_constrains_sequence_of():
    class MySeqOf(SequenceOfType):
        '''
        MySeqOf::= SEQUENCE OF INTEGER
        '''
        componentType = IntegerType()

    return MySeqOf()


def SCHEMA_constrained_seq_of_no_extension(lb, ub):
    class MySeqOf(SequenceOfType):
        '''
        MySeqOf::= SEQUENCE (SIZE(lowerEndpoint..upperEndpoint)) OF INTEGER
        '''
        subtypeSpec = SequenceOfValueSize(lb, ub)
        componentType = IntegerType()

    return MySeqOf()


def SCHEMA_constrained_seq_of_extension_present(lb, ub):
    class MySeqOf(SequenceOfType):
        '''
        MySeqOf::= SEQUENCE (SIZE(lowerEndpoint..upperEndpoint,...)) OF INTEGER
        '''
        subtypeSpec = SequenceOfValueSize(lb, ub, extensionMarker=True)
        componentType = IntegerType()

    return MySeqOf()


def DATA_seq_of(schema_seq_of, i0_is, i1_is, i2_is, i3_is, i4_is):
    seq_of = schema_seq_of
    if i0_is:
        seq_of.extend([IntegerType(I0_VAL)])
    if i1_is:
        seq_of.extend([IntegerType(I1_VAL)])
    if i2_is:
        seq_of.extend([IntegerType(I2_VAL)])
    if i3_is:
        seq_of.extend([IntegerType(I3_VAL)])
    if i4_is:
        seq_of.extend([IntegerType(I4_VAL)])
    return seq_of


@pytest.mark.parametrize("sequence_of, encoded", [
    (DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=False, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     '00'),
    (DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     '0103008707'),
    (DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     '020300870702FCB3'),
    (DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False),
     '030300870702FCB30117'),
    (DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False),
     '040300870702FCB3011703030D40'),
    (DATA_seq_of(SCHEMA_no_constrains_sequence_of(), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     '050300870702FCB3011703030D400105'),
])
def test_no_constrains_sequence_of_integer_can_be_encoded(sequence_of, encoded):
    assert per_encoder(sequence_of) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("sequence_of, encoded", [
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=0, ub=2), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     '4003008707'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=0, ub=2), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     '800300870702FCB3'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     '000300870702FCB3'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False),
     '400300870702FCB30117'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False),
     '800300870702FCB3011703030D40'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     'C00300870702FCB3011703030D400105'),
])
def test_constrained_sequence_of_no_extension_can_be_encoded(sequence_of, encoded):
    assert per_encoder(sequence_of) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("sequence_of, encoded", [
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=1, ub=1), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     '03008707'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=2, ub=2), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     '0300870702FCB3'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=3, ub=3), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False),
     '0300870702FCB30117'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=4, ub=4), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False),
     '0300870702FCB3011703030D40'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=5, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     '0300870702FCB3011703030D400105'),
])
def test_constrained_sequence_of_of_fixed_length_no_extension_can_be_encoded(sequence_of, encoded):
    assert per_encoder(sequence_of) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("sequence_of, encoded", [
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=2), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     '2003008707'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=2), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     '400300870702FCB3'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     '000300870702FCB3'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False),
     '200300870702FCB30117'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False),
     '400300870702FCB3011703030D40'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=2, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     '600300870702FCB3011703030D400105'),
])
def test_constrained_sequence_of_with_extension_and_num_of_elems_is_within_extension_root_can_be_encoded(sequence_of, encoded):
    assert per_encoder(sequence_of) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("sequence_of, encoded", [
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=0), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     '800103008707'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=0), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     '80020300870702FCB3'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=0, ub=0), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False),
     '80030300870702FCB30117'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=1, ub=1), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     '80020300870702FCB3'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=1, ub=1), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     '80050300870702FCB3011703030D400105'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=1, ub=3), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False),
     '80040300870702FCB3011703030D40'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=1, ub=3), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     '80050300870702FCB3011703030D400105'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=3, ub=4), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     '80050300870702FCB3011703030D400105'),
    (DATA_seq_of(SCHEMA_constrained_seq_of_extension_present(lb=3, ub=4), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     '800103008707'),
])
def test_constrained_sequence_of_with_extension_and_num_of_elems_is_not_within_extension_root_can_be_encoded(sequence_of, encoded):
    assert per_encoder(sequence_of) == bytearray.fromhex(encoded)

@pytest.mark.parametrize("sequence_of, exception", [
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=4, ub=5), i0_is=False, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     pytest.raises(SizeConstrainViolated)),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=4, ub=5), i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     pytest.raises(SizeConstrainViolated)),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=4, ub=5), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     pytest.raises(SizeConstrainViolated)),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=4, ub=5), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False),
     pytest.raises(SizeConstrainViolated)),
])
def test_constrained_sequence_of_with_num_of_elems_less_than_lower_bound_and_no_extension_raises(sequence_of, exception):
    with exception:
        per_encoder(sequence_of)


@pytest.mark.parametrize("sequence_of, exception", [
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=1, ub=2), i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False),
     pytest.raises(InvalidComponentIndexIntoStructuredType)),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=1, ub=2), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False),
     pytest.raises(InvalidComponentIndexIntoStructuredType)),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=1, ub=2), i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     pytest.raises(InvalidComponentIndexIntoStructuredType)),
    (DATA_seq_of(SCHEMA_constrained_seq_of_no_extension(lb=1, ub=1), i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     pytest.raises(InvalidComponentIndexIntoStructuredType)),
])
def test_constrained_sequence_with_num_of_elems_greater_than_upper_bound_and_no_extension_raises(sequence_of, exception):
    with exception:
        per_encoder(sequence_of)