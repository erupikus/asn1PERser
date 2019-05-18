import pytest
from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd
from asn1PERser.codec.per.encoder import encode as per_encoder


#-------------------------------------
class DataSeq(SequenceType):
    rootComponent = NamedTypes(
        NamedType('myBool0', BooleanType()),
        NamedType('myBitString', BitStringType())
    )
    componentType = rootComponent


class some_enum(EnumeratedType):
    namedValues = NamedValues(
        ('one', 0),
        ('two', 1),
        ('three', 2)
    )


class some_seqOf(SequenceOfType):
    componentType = OctetStringType()


class MySeq(SequenceType):
    rootComponent = NamedTypes(
        NamedType('some-seq', DataSeq()),
        NamedType('some-enum', some_enum()),
        NamedType('some-integer', IntegerType()),
        NamedType('some-seqOf', some_seqOf())
    )
    componentType = rootComponent


def DATA_first_sequence():
    '''
    mySeq MySeq ::= {
        some-seq {
            myBool0    TRUE,
            myBitString    '1111'B
        },
        some-enum two,
        some-integer  100,
        some-seqOf {'DEAD'H, 'BEEF'H}
    }
    '''
    data_seq = DataSeq()
    data_seq['myBool0'] = BooleanType(True)
    data_seq['myBitString'] = BitStringType(binValue='1111')

    some_seqOf_component = some_seqOf()
    some_seqOf_component.extend([OctetStringType(hexValue='DEAD'),
                                 OctetStringType(hexValue='BEEF')])

    my_seq = MySeq()
    my_seq['some-seq'] = data_seq
    my_seq['some-enum'] = some_enum('two')
    my_seq['some-integer'] = IntegerType(100)
    my_seq['some-seqOf'] = some_seqOf_component

    return my_seq


def test_first_sequence_can_be_encoded():
    per_encoded = per_encoder(asn1Spec=DATA_first_sequence())
    assert per_encoded == bytes.fromhex('8004F401640202DEAD02BEEF')

#-------------------------------------


'''
OuterSeq ::= SEQUENCE {
    sof1   MySof1 OPTIONAL,
    sof2   MySof2 OPTIONAL
}

MySof1 ::= SEQUENCE (SIZE(1..2)) OF InnerSeq1
MySof2 ::= SEQUENCE (SIZE(1..2)) OF InnerSeq2

InnerSeq1 ::= SEQUENCE {
    i0   INTEGER,
    i1   INTEGER
}

InnerSeq2 ::= SEQUENCE {
    i2   INTEGER,
    i3   INTEGER
}
'''

class InnerSeq1(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('i0', IntegerType()),
        NamedType('i1', IntegerType()),
    )
    componentType = rootComponent


class InnerSeq2(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('i2', IntegerType()),
        NamedType('i3', IntegerType()),
    )
    componentType = rootComponent


class MySof1(SequenceOfType):
    subtypeSpec = SequenceOfValueSize(1, 2)
    componentType = InnerSeq1()


class MySof2(SequenceOfType):
    subtypeSpec = SequenceOfValueSize(1, 2)
    componentType = InnerSeq2()


class OuterSeq(SequenceType):
    rootComponent = AdditiveNamedTypes(
        OptionalNamedType('sof1', MySof1()),
        OptionalNamedType('sof2', MySof2()),
    )
    componentType = rootComponent


def DATA_seq__of__seq_of__of__seq_in_root(my_sof1_is=False, my_sof2_is=False):
    inner_seq_1 = InnerSeq1()
    inner_seq_1['i0'] = IntegerType(10)
    inner_seq_1['i1'] = IntegerType(20)

    inner_seq_2 = InnerSeq2()
    inner_seq_2['i2'] = IntegerType(30)
    inner_seq_2['i3'] = IntegerType(40)

    my_sof1 = MySof1()
    my_sof1.extend([inner_seq_1])

    my_sof2 = MySof2()
    my_sof2.extend([inner_seq_2])

    outer = OuterSeq()

    if my_sof1_is:
        outer['sof1'] = my_sof1
    if my_sof2_is:
        outer['sof2'] = my_sof2
    return outer


@pytest.mark.parametrize("data, encoded", [
    (DATA_seq__of__seq_of__of__seq_in_root(my_sof1_is=True, my_sof2_is=False), '80010A0114'),
    (DATA_seq__of__seq_of__of__seq_in_root(my_sof1_is=True, my_sof2_is=True), 'C0010A011400011E0128'),
    (DATA_seq__of__seq_of__of__seq_in_root(my_sof1_is=False, my_sof2_is=True), '40011E0128'),
])
def test_seq_of_seq_of_of_seq_in_root_can_be_encoded(data, encoded):
    assert per_encoder(asn1Spec=data) == bytes.fromhex(encoded)


#-----------------------------


'''
OuterSeq ::= SEQUENCE {
    s0     INTEGER,
    ...,
    sof1   MySof1 OPTIONAL,
    sof2   MySof2 OPTIONAL
}

MySof1 ::= SEQUENCE (SIZE(1..2)) OF InnerSeq1
MySof2 ::= SEQUENCE (SIZE(1..2)) OF InnerSeq2

InnerSeq1 ::= SEQUENCE {
    i0   INTEGER,
    i1   INTEGER
}

InnerSeq2 ::= SEQUENCE {
    i2   INTEGER,
    i3   INTEGER
}
'''
class OuterSeq1(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('s0', IntegerType())
    )
    extensionAddition = AdditiveNamedTypes(
        OptionalNamedType('sof1', MySof1()),
        OptionalNamedType('sof2', MySof2()),
    )
    componentType = rootComponent + extensionAddition


def DATA_seq__of__seq_of__of__seq_in_ext_add(my_sof1_is=False, my_sof2_is=False):
    inner_seq_1 = InnerSeq1()
    inner_seq_1['i0'] = IntegerType(10)
    inner_seq_1['i1'] = IntegerType(20)

    inner_seq_2 = InnerSeq2()
    inner_seq_2['i2'] = IntegerType(30)
    inner_seq_2['i3'] = IntegerType(40)

    my_sof1 = MySof1()
    my_sof1.extend([inner_seq_1])

    my_sof2 = MySof2()
    my_sof2.extend([inner_seq_2])

    outer = OuterSeq1()

    outer['s0'] = IntegerType(-10)
    if my_sof1_is:
        outer['sof1'] = my_sof1
    if my_sof2_is:
        outer['sof2'] = my_sof2
    return outer


@pytest.mark.parametrize("data, encoded", [
    (DATA_seq__of__seq_of__of__seq_in_ext_add(my_sof1_is=True, my_sof2_is=False), '8001F603000500010A0114'),
    (DATA_seq__of__seq_of__of__seq_in_ext_add(my_sof1_is=True, my_sof2_is=True), '8001F603800500010A01140500011E0128'),
    (DATA_seq__of__seq_of__of__seq_in_ext_add(my_sof1_is=False, my_sof2_is=True), '8001F602800500011E0128'),
    (DATA_seq__of__seq_of__of__seq_in_ext_add(my_sof1_is=False, my_sof2_is=False), '0001F6'),
])
def test_seq_of_seq_of_of_seq_in_extension_addition_can_be_encoded(data, encoded):
    assert per_encoder(asn1Spec=data) == bytes.fromhex(encoded)

#----------------------------------


'''
OuterSeq ::= SEQUENCE {
    s0     INTEGER,
    ...,
    [[
    sof1   MySof1 OPTIONAL,
    sof2   MySof2 OPTIONAL
    ]]
}

MySof1 ::= SEQUENCE (SIZE(1..2)) OF InnerSeq1
MySof2 ::= SEQUENCE (SIZE(1..2)) OF InnerSeq2

InnerSeq1 ::= SEQUENCE {
    i0   INTEGER,
    i1   INTEGER
}

InnerSeq2 ::= SEQUENCE {
    i2   INTEGER,
    i3   INTEGER
}
'''
class OuterSeq2(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('s0', IntegerType())
    )
    extensionAdditionGroups = [
        AdditiveNamedTypes(
            OptionalNamedType('sof1', MySof1()),
            OptionalNamedType('sof2', MySof2()),
        )
    ]
    componentType = rootComponent + extensionAdditionGroups


def DATA_seq__of__seq_of__of__seq_in_ext_add_group(my_sof1_is=False, my_sof2_is=False):
    inner_seq_1 = InnerSeq1()
    inner_seq_1['i0'] = IntegerType(10)
    inner_seq_1['i1'] = IntegerType(20)

    inner_seq_2 = InnerSeq2()
    inner_seq_2['i2'] = IntegerType(30)
    inner_seq_2['i3'] = IntegerType(40)

    my_sof1 = MySof1()
    my_sof1.extend([inner_seq_1])

    my_sof2 = MySof2()
    my_sof2.extend([inner_seq_2])

    outer = OuterSeq2()

    outer['s0'] = IntegerType(-10)
    if my_sof1_is:
        outer['sof1'] = my_sof1
    if my_sof2_is:
        outer['sof2'] = my_sof2
    return outer


@pytest.mark.parametrize("data, encoded", [
    (DATA_seq__of__seq_of__of__seq_in_ext_add_group(my_sof1_is=True, my_sof2_is=False), '8001F6010580010A0114'),
    (DATA_seq__of__seq_of__of__seq_in_ext_add_group(my_sof1_is=True, my_sof2_is=True), '8001F6010AC0010A011400011E0128'),
    (DATA_seq__of__seq_of__of__seq_in_ext_add_group(my_sof1_is=False, my_sof2_is=True), '8001F6010540011E0128'),
    (DATA_seq__of__seq_of__of__seq_in_ext_add_group(my_sof1_is=False, my_sof2_is=False), '0001F6'),
])
def test_seq_of_seq_of_of_seq_in_extension_addition_group_can_be_encoded(data, encoded):
    assert per_encoder(asn1Spec=data) == bytes.fromhex(encoded)
