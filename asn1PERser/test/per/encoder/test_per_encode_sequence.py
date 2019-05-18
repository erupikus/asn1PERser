import pytest
from pyasn1.type.namedtype import NamedType, NamedTypes, DefaultedNamedType, OptionalNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.codec.per.encoder import encode as per_encoder
from asn1PERser.codec.per.encoder import MandatoryExtensionFieldNotPresent
from asn1PERser.classes.data.builtin.SequenceType import SequenceType
from asn1PERser.classes.data.builtin.IntegerType import IntegerType
from asn1PERser.classes.data.builtin.BooleanType import BooleanType
from asn1PERser.classes.data.builtin.OctetStringType import OctetStringType
from asn1PERser.classes.data.builtin.BitStringType import BitStringType
from asn1PERser.classes.data.builtin.EnumeratedType import EnumeratedType
from asn1PERser.classes.types.constraint import ValueRange, ValueSize, ExtensionMarker


I0_VAL = 34567
I1_VAL = -845
I2_VAL = 23
I3_VAL = 200000
I4_VAL = 5


class i0(IntegerType):
    pass


class i1(IntegerType):
    pass


class i2(IntegerType):
    subtypeSpec = ValueRange(0, 100000, extensionMarker=True)


class i3(IntegerType):
    subtypeSpec = ValueRange(128, 1000, extensionMarker=True)


class i4(IntegerType):
    subtypeSpec = ValueRange(0, 10, extensionMarker=True)


class o2(OctetStringType):
    subtypeSpec = ValueSize(2, 6)


class b0(BitStringType):
    subtypeSpec = ValueSize(0, 10, extensionMarker=True)


class b4(BitStringType):
    subtypeSpec = ValueSize(5, 5)


class b6(BitStringType):
    subtypeSpec = ValueSize(20, 1000)


class b9(BitStringType):
    subtypeSpec = ValueSize(1, 2)


class b10(BitStringType):
    subtypeSpec = ValueSize(20, 20)


class e0(EnumeratedType):
    subtypeSpec = ExtensionMarker(True)
    enumerationRoot = NamedValues(
        ('a0', 0),
        ('a1', 1)
    )
    namedValues = enumerationRoot


class e1(EnumeratedType):
    subtypeSpec = ExtensionMarker(True)
    enumerationRoot = NamedValues(
        ('b0', 0)
    )
    extensionAddition = NamedValues(
        ('b1', 1),
        ('b2', 2)
    )
    namedValues = enumerationRoot + extensionAddition


class e2(EnumeratedType):
    enumerationRoot = NamedValues(
        ('c0', 0),
        ('c1', 1),
        ('c2', 2)
    )
    namedValues = enumerationRoot


class e3(EnumeratedType):
    subtypeSpec = ExtensionMarker(True)
    enumerationRoot = NamedValues(
        ('d0', 0),
        ('d1', 1),
        ('d2', 2)
    )
    namedValues = enumerationRoot


class e4(EnumeratedType):
    subtypeSpec = ExtensionMarker(True)
    enumerationRoot = NamedValues(
        ('f0', 0)
    )
    extensionAddition = NamedValues(
        ('f1', 1)
    )
    namedValues = enumerationRoot + extensionAddition


class e5(EnumeratedType):
    enumerationRoot = NamedValues(
        ('g0', 0)
    )
    namedValues = enumerationRoot


def SCHEMA_two_elem_seq_with_extension_marker_present_or_not(extensionMarker_value):
    class MySeq(SequenceType):
        '''
        If extensionMarker_value == False:
            MySeq ::= SEQUENCE
            {
             i0    INTEGER,
             i1    INTEGER
            }

        else:
            MySeq ::= SEQUENCE
            {
             i0    INTEGER,
             i1    INTEGER
             ...
            }
        '''
        subtypeSpec = ExtensionMarker(extensionMarker_value)
        rootComponent = NamedTypes(
            NamedType('i0', IntegerType()),
            NamedType('i1', IntegerType())
        )
        componentType = rootComponent
    return MySeq()


def SCHEMA_seq_with_only_extension_marker_present_or_not(extensionMarker_value):
    class MySeq(SequenceType):
        '''
        If extensionMarker_value == False:
            MySeq ::= SEQUENCE
            {
             i0    INTEGER,
             i1    INTEGER,
             i2    INTEGER (0..100000),
             i3    INTEGER (128..1000,...),
             i4    INTEGER (0..10,...)
            }

        else:
            MySeq ::= SEQUENCE
            {
             i0    INTEGER,
             i1    INTEGER,
             i2    INTEGER (0..100000),
             i3    INTEGER (128..1000,...),
             i4    INTEGER (0..10,...),
             ...
            }
        '''
        subtypeSpec = ExtensionMarker(extensionMarker_value)
        rootComponent = NamedTypes(
            NamedType('i0', IntegerType()),
            NamedType('i1', IntegerType()),
            NamedType('i2', i2()),
            NamedType('i3', i3()),
            NamedType('i4', i4()),
        )
        componentType = rootComponent
    return MySeq()


def SCHEMA_seq_with_elements_in_extension_addition(extensionMarker_value):
    class MySeq(SequenceType):
        '''
            MySeq ::= SEQUENCE
            {
             i0    INTEGER,
             ...,
             i1    INTEGER,
             i2    INTEGER (0..100000),
             i3    INTEGER (128..1000,...),
             i4    INTEGER (0..10,...)
            }
        '''
        subtypeSpec = ExtensionMarker(extensionMarker_value)
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType())
        )
        extensionAddition = AdditiveNamedTypes(
            NamedType('i1', IntegerType()),
            NamedType('i2', i2()),
            NamedType('i3', i3()),
            NamedType('i4', i4())
        )
        componentType = rootComponent + extensionAddition
    return MySeq()


def SCHEMA_seq_with_some_optional_elements_in_root(extensionMarker_value):
    class SeqOptional(SequenceType):
        '''
        MySeq ::= SEQUENCE
        {
            i0    INTEGER,
            i1    INTEGER OPTIONAL,
            i2    INTEGER (0..100000),
            i3    INTEGER (128..1000,...) OPTIONAL,
            i4    INTEGER (0..10,...)
        }
        '''
        subtypeSpec = ExtensionMarker(extensionMarker_value)
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
            OptionalNamedType('i1', IntegerType()),
            NamedType('i2', i2()),
            OptionalNamedType('i3', i3()),
            NamedType('i4', i4())
        )
        componentType = rootComponent
    return SeqOptional()


def SCHEMA_seq_with_only_optional_elements_in_root(extensionMarker_value):
    class SeqOptional(SequenceType):
        '''
        MySeq ::= SEQUENCE
        {
            i0  [0]  INTEGER OPTIONAL,
            i1       INTEGER OPTIONAL
        }
        '''
        subtypeSpec = ExtensionMarker(extensionMarker_value)
        rootComponent = AdditiveNamedTypes(
            OptionalNamedType('i0', IntegerType()),
            OptionalNamedType('i1', IntegerType())
        )
        componentType = rootComponent
    return SeqOptional()


def SCHEMA_seq_with_default_elements_in_root(extensionMarker_value):
    class SeqOptional(SequenceType):
        '''
        MySeq ::= SEQUENCE
        {
            i0    INTEGER,
            i1    INTEGER DEFAULT 10,
            i2    INTEGER (0..100000),
            i3    INTEGER (128..1000,...) DEFAULT 300,
            i4    INTEGER (0..10,...)
        }
        '''
        subtypeSpec = ExtensionMarker(extensionMarker_value)
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
            DefaultedNamedType('i1', IntegerType(10)),
            NamedType('i2', i2()),
            DefaultedNamedType('i3', i3(300)),
            NamedType('i4', i4())
        )
        componentType = rootComponent
    return SeqOptional()


def SCHEMA_sequence_of_boolean(extensionMarker_value=True):
    class SeqOfBool(SequenceType):
        '''
        MySeq ::= SEQUENCE
        {
            b0    BOOLEAN,
            b1    BOOLEAN,
            b2    BOOLEAN,
            b3    BOOLEAN,
            b4    BOOLEAN,
            b5    BOOLEAN,
            b6    BOOLEAN,
            b7    BOOLEAN,
            b8    BOOLEAN,
            b9    BOOLEAN,
            ...,
            b10   BOOLEAN,
            b11   BOOLEAN,
            b12   BOOLEAN,
            b13   BOOLEAN,
            b14   BOOLEAN,
            b15   BOOLEAN,
            b16   BOOLEAN,
            b17   BOOLEAN,
            b18   BOOLEAN,
            b19   BOOLEAN,
            b20   BOOLEAN
        }
        '''
        subtypeSpec = ExtensionMarker(extensionMarker_value)
        rootComponent = AdditiveNamedTypes(
            NamedType('b0', BooleanType()),
            NamedType('b1', BooleanType()),
            NamedType('b2', BooleanType()),
            NamedType('b3', BooleanType()),
            NamedType('b4', BooleanType()),
            NamedType('b5', BooleanType()),
            NamedType('b6', BooleanType()),
            NamedType('b7', BooleanType()),
            NamedType('b8', BooleanType()),
            NamedType('b9', BooleanType()),
        )
        extensionAddition = AdditiveNamedTypes(
            NamedType('b10', BooleanType()),
            NamedType('b11', BooleanType()),
            NamedType('b12', BooleanType()),
            NamedType('b13', BooleanType()),
            NamedType('b14', BooleanType()),
            NamedType('b15', BooleanType()),
            NamedType('b16', BooleanType()),
            NamedType('b17', BooleanType()),
            NamedType('b18', BooleanType()),
            NamedType('b19', BooleanType()),
            NamedType('b20', BooleanType()),
        )
        componentType = rootComponent + extensionAddition
    return SeqOfBool()


def SCHEMA_sequence_of_octetstring():
    class SeqOfOctet(SequenceType):
        '''
        MySeq ::= SEQUENCE {
            o0    OCTET STRING,
            o1    OCTET STRING OPTIONAL,
            o2    OCTET STRIMG (SIZE(2..6)),
            o3    OCTET STRING,
            o4    OCTET STRING DEFAULT 'FFFFFF'H,
            o5    OCTET STRING OPTIONAL,
            o6    OCTET STRING
        }
        '''
        rootComponent = AdditiveNamedTypes(
            NamedType('o0', OctetStringType()),
            OptionalNamedType('o1', OctetStringType()),
            NamedType('o2', o2()),
            NamedType('o3', OctetStringType()),
            DefaultedNamedType('o4', OctetStringType(hexValue='FFFFFF')),
            OptionalNamedType('o5', OctetStringType()),
            NamedType('o6', OctetStringType()),
        )
        componentType = rootComponent
    return SeqOfOctet()


def SCHEMA_sequence_of_bitstring():
    class SeqOfBit(SequenceType):
        '''
        MySeq  ::= SEQUENCE {
            b0    BIT STRING (SIZE(0..10, ...)),
            b1    BIT STRING,
            b2    BIT STRING DEFAULT 'AAAA'H,
            b3    BIT STRING OPTIONAL,
            b4    BIT STRING (SIZE(5..5)),
            b5    BIT STRING,
            b6    BIT STRING (SIZE(20..1000)),
            b7    BIT STRING,
            b8    BIT STRING,
            ...,
            b9    BIT STRING (SIZE(1..2)) OPTIONAL,
            b10   BIT STRING (SIZE(20..20)),
            b11   BIT STRING
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('b0', b0()),
            NamedType('b1', BitStringType()),
            DefaultedNamedType('b2', BitStringType(hexValue='AAAA')),
            OptionalNamedType('b3', BitStringType()),
            NamedType('b4', b4()),
            NamedType('b5', BitStringType()),
            NamedType('b6', b6()),
            NamedType('b7', BitStringType()),
            NamedType('b8', BitStringType())
        )
        extensionAddition = AdditiveNamedTypes(
            OptionalNamedType('b9', b9()),
            NamedType('b10', b10()),
            NamedType('b11', BitStringType())
        )
        componentType = rootComponent + extensionAddition
    return SeqOfBit()


def SCHEMA_sequence_of_enumerated():
    class SeqOfEnum(SequenceType):
        '''
        SeqOfEnum ::= SEQUENCE {
            e0    ENUMERATED {a0, a1, ...},
            e1    ENUMERATED {b0, ..., b1, b2} OPTIONAL,
            e2    ENUMERATED {c0, c1, c2},
            e3    ENUMERATED {d0, d1, d2, ...} DEFAULT d1,
            ...,
            e4    ENUMERATED {f0, ..., f1} OPTIONAL,
            e5    ENUMERATED {g0}
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('e0', e0()),
            OptionalNamedType('e1', e1()),
            NamedType('e2', e2()),
            DefaultedNamedType('e3', e3('d1'))
        )
        extensionAddition = AdditiveNamedTypes(
            OptionalNamedType('e4', e4()),
            NamedType('e5', e5())
        )
        componentType = rootComponent + extensionAddition
    return SeqOfEnum()


def SCHEMA_sequence_with_extension_addition_groups_1():
    class MySeq(SequenceType):
        '''
        MySeq ::= SEQUENCE {
            s0    OCTET STRING,
            s1    OCTET STRING,
            ...,
            [[
            s2    OCTET STRING,
            s3    OCTET STRING
            ]],
            [[
            s4    OCTET STRING
            ]],
            [[
            s5    OCTET STRING
            ]],
            [[
            s6    OCTET STRING
            ]]
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('s0', OctetStringType()),
            NamedType('s1', OctetStringType())
        )
        extensionAdditionGroups = [
            AdditiveNamedTypes(
                NamedType('s2', OctetStringType()),
                NamedType('s3', OctetStringType())
            ),
            AdditiveNamedTypes(
                NamedType('s4', OctetStringType())
            ),
            AdditiveNamedTypes(
                NamedType('s5', OctetStringType())
            ),
            AdditiveNamedTypes(
                NamedType('s6', OctetStringType())
            )
        ]
        componentType = rootComponent + extensionAdditionGroups
    return MySeq()


def SCHEMA_sequence_with_extension_addition_groups_2():
    class MySeq(SequenceType):
        '''
        MySeq ::= SEQUENCE {
            s0    OCTET STRING,
            ...,
            [[
            s1    OCTET STRING
            ]],
            [[
            s2    OCTET STRING OPTIONAL,
            s3    OCTET STRING OPTIONAL
            ]],
            [[
            s4    OCTET STRING,
            s5    OCTET STRING OPTIONAL,
            s6    OCTET STRING
            ]]
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('s0', OctetStringType())
        )
        extensionAdditionGroups = [
            AdditiveNamedTypes(
                NamedType('s1', OctetStringType())
            ),
            AdditiveNamedTypes(
                OptionalNamedType('s2', OctetStringType()),
                OptionalNamedType('s3', OctetStringType())
            ),
            AdditiveNamedTypes(
                NamedType('s4', OctetStringType()),
                OptionalNamedType('s5', OctetStringType()),
                NamedType('s6', OctetStringType())
            )
        ]
        componentType = rootComponent + extensionAdditionGroups
    return MySeq()


def SCHEMA_sequence_with_extension_addition_groups_3():
    class MySeq(SequenceType):
        '''
        MySeq ::= SEQUENCE {
            s0    OCTET STRING,
            ...,
            s1    OCTET STRING OPTIONAL,
            s2    OCTET STRING,
            [[
            s3    OCTET STRING,
            s4    OCTET STRING,
            s5    OCTET STRING OPTIONAL
            ]],
            [[
            s6    OCTET STRING OPTIONAL
            ]]
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('s0', OctetStringType())
        )
        extensionAddition = AdditiveNamedTypes(
            OptionalNamedType('s1', OctetStringType()),
            NamedType('s2', OctetStringType())
        )
        extensionAdditionGroups = [
            AdditiveNamedTypes(
                NamedType('s3', OctetStringType()),
                NamedType('s4', OctetStringType()),
                OptionalNamedType('s5', OctetStringType())
            ),
            AdditiveNamedTypes(
                OptionalNamedType('s6', OctetStringType())
            )
        ]
        componentType = rootComponent + extensionAddition + extensionAdditionGroups
    return MySeq()


def DATA_simple_seq(seq, i0_is=False, i0_val=I0_VAL, i1_is=False, i1_val=I1_VAL, i2_is=False, i2_val=I2_VAL,
                    i3_is=False, i3_val=I3_VAL, i4_is=False, i4_val=I4_VAL, ext_mark=False):
    seq = seq(ext_mark)
    if i0_is:
        seq['i0'] = i0(i0_val)
    if i1_is:
        seq['i1'] = i1(i1_val)
    if i2_is:
        seq['i2'] = i2(i2_val)
    if i3_is:
        seq['i3'] = i3(i3_val)
    if i4_is:
        seq['i4'] = i4(i4_val)
    return seq


def DATA_bool_seq(seq, root_val, addition_present, addition_val=False):
    seq = seq()
    seq['b0'] = BooleanType(root_val)
    seq['b1'] = BooleanType(root_val)
    seq['b2'] = BooleanType(root_val)
    seq['b3'] = BooleanType(root_val)
    seq['b4'] = BooleanType(root_val)
    seq['b5'] = BooleanType(root_val)
    seq['b6'] = BooleanType(root_val)
    seq['b7'] = BooleanType(root_val)
    seq['b8'] = BooleanType(root_val)
    seq['b9'] = BooleanType(root_val)
    if addition_present:
        seq['b10'] = BooleanType(addition_val)
        seq['b11'] = BooleanType(addition_val)
        seq['b12'] = BooleanType(addition_val)
        seq['b13'] = BooleanType(addition_val)
        seq['b14'] = BooleanType(addition_val)
        seq['b15'] = BooleanType(addition_val)
        seq['b16'] = BooleanType(addition_val)
        seq['b17'] = BooleanType(addition_val)
        seq['b18'] = BooleanType(addition_val)
        seq['b19'] = BooleanType(addition_val)
        seq['b20'] = BooleanType(addition_val)
    return seq


def DATA_octet_seq(seq, o1_is, o4_is, o5_is):
    seq = seq()
    seq['o0'] = OctetStringType(hexValue='DEAD')
    if o1_is:
        seq['o1'] = OctetStringType(hexValue='BEEF')
    seq['o2'] = o2(hexValue='ABCD')
    seq['o3'] = OctetStringType(hexValue='AA')
    if o4_is:
        seq['o4'] = OctetStringType(hexValue='BBB')
    if o5_is:
        seq['o5'] = OctetStringType(hexValue='CCCC')
    seq['o6'] = OctetStringType(hexValue='DDDDD')
    return seq


def DATA_bitstring_seq(schema, b2_is, b3_is, b9_is):
    seq = schema()
    seq['b0'] = b0(binValue='111100001111')
    seq['b1'] = BitStringType(hexValue='DEAD')
    if b2_is:
        seq['b2'] = BitStringType(hexValue='BEEF')
    if b3_is:
        seq['b3'] = BitStringType(hexValue='ABCD')
    seq['b4'] = b4(binValue='11111')
    seq['b5'] = BitStringType(hexValue='FEED')
    seq['b6'] = b6(binValue='1111000011110000111100001111000011110000')
    seq['b7'] = BitStringType(hexValue='BBBB')
    seq['b8'] = BitStringType(hexValue='CCCCC')
    if b9_is:
        seq['b9'] = b9(binValue='11')
    seq['b10'] = b10(binValue='11110000111100001111')
    seq['b11'] = BitStringType(hexValue='DDDDDD')
    return seq


def DATA_enumerated_seq(schema, e1_is, e3_is, e4_is):
    seq = schema()
    seq['e0'] = 'a1'
    if e1_is:
        seq['e1'] = 'b2'
    seq['e2'] = 'c1'
    if e3_is:
        seq['e3'] = e3('d2')
    if e4_is:
        seq['e4'] = 'f1'
    seq['e5'] = 'g0'
    return seq


def DATA_extension_addition_groups_seq(schema, s0=None, s1=None, s2=None, s3=None, s4=None, s5=None, s6=None):
    seq = schema()
    if s0:
        seq['s0'] = OctetStringType(hexValue=s0)
    if s1:
        seq['s1'] = OctetStringType(hexValue=s1)
    if s2:
        seq['s2'] = OctetStringType(hexValue=s2)
    if s3:
        seq['s3'] = OctetStringType(hexValue=s3)
    if s4:
        seq['s4'] = OctetStringType(hexValue=s4)
    if s5:
        seq['s5'] = OctetStringType(hexValue=s5)
    if s6:
        seq['s6'] = OctetStringType(hexValue=s6)
    return seq


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_simple_seq(SCHEMA_two_elem_seq_with_extension_marker_present_or_not, i0_is=True, i1_is=True, i2_is=False,
                     i3_is=False, i4_is=False, ext_mark=False), '0300870702FCB3'),
    (DATA_simple_seq(SCHEMA_two_elem_seq_with_extension_marker_present_or_not, i0_is=True, i1_is=True, i2_is=False,
                     i3_is=False, i4_is=False, ext_mark=True), '000300870702FCB3'),
    (DATA_simple_seq(SCHEMA_seq_with_only_extension_marker_present_or_not, i0_is=True,i1_is=True, i2_is=True, i3_is=True,
                     i4_is=True, ext_mark=False), '0300870702FCB300178003030D4028'),
    (DATA_simple_seq(SCHEMA_seq_with_only_extension_marker_present_or_not, i0_is=True,i1_is=True, i2_is=True, i3_is=True,
                     i4_is=True, ext_mark=True), '000300870702FCB300178003030D4028'),
])
def test_no_extension_no_default_no_optional_components_present_sequence_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,i1_is=True, i2_is=True, i3_is=True,
                     i4_is=True, ext_mark=True),  '800300870707E00302FCB3020017058003030D400128'),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True,i1_is=True, i2_is=True, i3_is=True,
                     i4_is=False, ext_mark=True), '800300870707C00302FCB3020017058003030D40'),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=True, i2_is=True, i3_is=False,
                     i4_is=False, ext_mark=True), '800300870707800302FCB3020017'),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=True, i2_is=False, i3_is=False,
                     i4_is=False, ext_mark=True), '800300870707000302FCB3'),
])
def test_extension_components_are_present_but_no_default_no_optional_sequence_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_simple_seq(SCHEMA_seq_with_some_optional_elements_in_root, i0_is=True, i1_is=False, i2_is=True, i3_is=False, i4_is=True),
     '0003008707001728'),
    (DATA_simple_seq(SCHEMA_seq_with_some_optional_elements_in_root, i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=True),
     '800300870702FCB3001728'),
    (DATA_simple_seq(SCHEMA_seq_with_some_optional_elements_in_root, i0_is=True, i1_is=False, i2_is=True, i3_is=True, i4_is=True),
     '400300870700178003030D4028'),
    (DATA_simple_seq(SCHEMA_seq_with_some_optional_elements_in_root, i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     'C00300870702FCB300178003030D4028'),
    (DATA_simple_seq(SCHEMA_seq_with_only_optional_elements_in_root, i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     'C00300870702FCB3'),
    (DATA_simple_seq(SCHEMA_seq_with_only_optional_elements_in_root, i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     '8003008707'),
    (DATA_simple_seq(SCHEMA_seq_with_only_optional_elements_in_root, i0_is=False, i1_is=True, i2_is=False, i3_is=False, i4_is=False),
     '4002FCB3'),
    (DATA_simple_seq(SCHEMA_seq_with_only_optional_elements_in_root, i0_is=False, i1_is=False, i2_is=False, i3_is=False, i4_is=False),
     '00'),
])
def test_optional_components_present_in_extension_root_sequence_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True, i1_is=False, i2_is=True, i3_is=False, i4_is=True),
     '0003008707001728'),
    (DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=True),
     '800300870702FCB3001728'),
    (DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True, i1_is=False, i2_is=True, i3_is=True, i4_is=True),
     '400300870700178003030D4028'),
    (DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True),
     'C00300870702FCB300178003030D4028'),
])
def test_default_components_with_none_default_values_present_in_extension_root_sequence_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True, i1_val=10, i1_is=True, i2_is=True, i3_val=300, i3_is=False, i4_is=True),
     '0003008707001728'),
    (DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True, i1_val=10, i1_is=False, i2_is=True, i3_val=300, i3_is=True, i4_is=True),
     '0003008707001728'),
    (DATA_simple_seq(SCHEMA_seq_with_default_elements_in_root, i0_is=True, i1_val=10, i1_is=True, i2_is=True, i3_val=300, i3_is=True, i4_is=True),
     '0003008707001728'),
])
def test_default_components_with_default_values_present_in_filled_schema_are_not_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=False, ext_mark=True),
     '0003008707'),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=False, ext_mark=True),
     '800300870707000302FCB3'),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=True, i2_is=True, i3_is=False, i4_is=False, ext_mark=True),
     '800300870707800302FCB3020017'),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=False, ext_mark=True),
     '800300870707C00302FCB3020017058003030D40'),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=True, i2_is=True, i3_is=True, i4_is=True, ext_mark=True),
     '800300870707E00302FCB3020017058003030D400128'),

])
def test_elements_in_extension_addition_may_not_be_present_even_if_no_optional_in_schema_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, exception", [
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=False, i2_is=True, i3_is=False, i4_is=False, ext_mark=True),
     pytest.raises(MandatoryExtensionFieldNotPresent)),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=False, i2_is=False, i3_is=True, i4_is=False, ext_mark=True),
     pytest.raises(MandatoryExtensionFieldNotPresent)),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=False, i2_is=False, i3_is=False, i4_is=True, ext_mark=True),
     pytest.raises(MandatoryExtensionFieldNotPresent)),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=True, i2_is=False, i3_is=True, i4_is=False, ext_mark=True),
     pytest.raises(MandatoryExtensionFieldNotPresent)),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=True, i2_is=False, i3_is=False, i4_is=True, ext_mark=True),
     pytest.raises(MandatoryExtensionFieldNotPresent)),
    (DATA_simple_seq(SCHEMA_seq_with_elements_in_extension_addition, i0_is=True, i1_is=False, i2_is=True, i3_is=False, i4_is=True, ext_mark=True),
     pytest.raises(MandatoryExtensionFieldNotPresent)),

])
def test_when_mandatory_extension_field_is_not_present_then_can_not_be_encoded_and_raises(sequence, exception):
    with exception:
        per_encoder(sequence)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=False, addition_present=False), '0000'),
    (DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=True, addition_present=False), '7FE0'),
    (DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=False, addition_present=True, addition_val=False), '8002BFF801000100010001000100010001000100010001000100'),
    (DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=False, addition_present=True, addition_val=True), '8002BFF801800180018001800180018001800180018001800180'),
    (DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=True, addition_present=True, addition_val=False), 'FFE2BFF801000100010001000100010001000100010001000100'),
    (DATA_bool_seq(SCHEMA_sequence_of_boolean, root_val=True, addition_present=True, addition_val=True), 'FFE2BFF801800180018001800180018001800180018001800180'),
])
def test_sequence_of_boolean_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=True, o4_is=True, o5_is=True), 'E002DEAD02BEEF00ABCD01AA02BBB002CCCC03DDDDD0'),
    (DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=False, o4_is=True, o5_is=True), '6002DEAD00ABCD01AA02BBB002CCCC03DDDDD0'),
    (DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=True, o4_is=False, o5_is=True), 'A002DEAD02BEEF00ABCD01AA02CCCC03DDDDD0'),
    (DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=True, o4_is=True, o5_is=False), 'C002DEAD02BEEF00ABCD01AA02BBB003DDDDD0'),
    (DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=False, o4_is=False, o5_is=True), '2002DEAD00ABCD01AA02CCCC03DDDDD0'),
    (DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=False, o4_is=True, o5_is=False), '4002DEAD00ABCD01AA02BBB003DDDDD0'),
    (DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=True, o4_is=False, o5_is=False), '8002DEAD02BEEF00ABCD01AA03DDDDD0'),
    (DATA_octet_seq(SCHEMA_sequence_of_octetstring, o1_is=False, o4_is=False, o5_is=False), '0002DEAD00ABCD01AA03DDDDD0'),
])
def test_sequence_of_octetstring_no_extension_marker_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=True, b3_is=True, b9_is=True), 'F00CF0F010DEAD10BEEF10ABCDF810FEED0014F0F0F0F0F010BBBB14CCCCC05C0280C003F0F0F00418DDDDDD'),
    (DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=False, b3_is=True, b9_is=True), 'B00CF0F010DEAD10ABCDF810FEED0014F0F0F0F0F010BBBB14CCCCC05C0280C003F0F0F00418DDDDDD'),
    (DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=True, b3_is=False, b9_is=True), 'D00CF0F010DEAD10BEEFF810FEED0014F0F0F0F0F010BBBB14CCCCC05C0280C003F0F0F00418DDDDDD'),
    (DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=True, b3_is=True, b9_is=False), 'F00CF0F010DEAD10BEEF10ABCDF810FEED0014F0F0F0F0F010BBBB14CCCCC04C03F0F0F00418DDDDDD'),
    (DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=False, b3_is=False, b9_is=True), '900CF0F010DEADF810FEED0014F0F0F0F0F010BBBB14CCCCC05C0280C003F0F0F00418DDDDDD'),
    (DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=False, b3_is=True, b9_is=False), 'B00CF0F010DEAD10ABCDF810FEED0014F0F0F0F0F010BBBB14CCCCC04C03F0F0F00418DDDDDD'),
    (DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=True, b3_is=False, b9_is=False), 'D00CF0F010DEAD10BEEFF810FEED0014F0F0F0F0F010BBBB14CCCCC04C03F0F0F00418DDDDDD'),
    (DATA_bitstring_seq(SCHEMA_sequence_of_bitstring, b2_is=False, b3_is=False, b9_is=False), '900CF0F010DEADF810FEED0014F0F0F0F0F010BBBB14CCCCC04C03F0F0F00418DDDDDD'),
])
def test_sequence_of_bitstring_with_extension_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=True, e3_is=True, e4_is=True), 'EC0A80E001800100'),
    (DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=False, e3_is=True, e4_is=True), 'AA80E001800100'),
    (DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=True, e3_is=False, e4_is=True), 'CC0A0701800100'),
    (DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=True, e3_is=True, e4_is=False), 'EC0A80A00100'),
    (DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=False, e3_is=False, e4_is=True), '8A0701800100'),
    (DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=False, e3_is=True, e4_is=False), 'AA80A00100'),
    (DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=True, e3_is=False, e4_is=False), 'CC0A050100'),
    (DATA_enumerated_seq(SCHEMA_sequence_of_enumerated, e1_is=False, e3_is=False, e4_is=False), '8A050100'),
])
def test_sequence_of_enumerated_with_extension_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


@pytest.mark.parametrize("sequence, encoded", [
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_1,
                                        s0='99', s1='AA'), '00019901AA'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_1,
                                        s0='99', s1='AA', s2='BB', s3='CC'), '80019901AA07000401BB01CC'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_1,
                                        s0='99', s1='AA', s2='BB', s3='CC', s4='DD'), '80019901AA07800401BB01CC0201DD'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_1,
                                        s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE'), '80019901AA07C00401BB01CC0201DD0201EE'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_1,
                                        s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE', s6='FF'), '80019901AA07E00401BB01CC0201DD0201EE0201FF'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_2,
                                        s0='99'), '000199'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_2,
                                        s0='99', s1='AA'), '80019905000201AA'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_2,
                                        s0='99', s1='AA', s2='BB'), '80019905800201AA038001BB'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_2,
                                        s0='99', s1='AA', s3='CC'), '80019905800201AA034001CC'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_2,
                                        s0='99', s1='AA', s2='BB', s3='CC'), '80019905800201AA05C001BB01CC'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_2,
                                        s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE', s6='FF'), '80019905C00201AA05C001BB01CC078001DD01EE01FF'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_2,
                                        s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s6='FF'), '80019905C00201AA05C001BB01CC050001DD01FF'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_2,
                                        s0='99', s1='AA', s4='DD', s5='EE', s6='FF'), '80019905400201AA078001DD01EE01FF'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_2,
                                        s0='99', s1='AA', s4='DD', s6='FF'), '80019905400201AA050001DD01FF'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99'), '000199'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99', s1='AA'), '80019907000201AA'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99', s1='AA', s2='BB'), '80019907800201AA0201BB'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99', s2='BB'), '80019906800201BB'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99', s1='AA', s2='BB', s3='CC', s4='DD'), '80019907C00201AA0201BB050001CC01DD'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE'), '80019907C00201AA0201BB078001CC01DD01EE'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s5='EE', s6='FF'), '80019907E00201AA0201BB078001CC01DD01EE038001FF'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99', s1='AA', s2='BB', s3='CC', s4='DD', s6='FF'), '80019907E00201AA0201BB050001CC01DD038001FF'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99', s2='BB', s3='CC', s4='DD', s6='FF'), '80019906E00201BB050001CC01DD038001FF'),
    (DATA_extension_addition_groups_seq(SCHEMA_sequence_with_extension_addition_groups_3,
                                        s0='99', s2='BB', s3='CC', s4='DD'), '80019906C00201BB050001CC01DD'),
])
def test_sequence_with_extension_addition_groups_can_be_encoded(sequence, encoded):
    assert per_encoder(sequence) == bytes.fromhex(encoded)


# elementy w extensionAddition musza byc obecne po kolei
# jesli pierwszy element nie jest OPTIONAL, to musi on byc obecny jesli chcecmy zakodowac
# element drugi itd
# Jesli element pierwszy jesli OPTIONAL to nie musi on byc obecny jesli chcemy zakodowac
# element drugi