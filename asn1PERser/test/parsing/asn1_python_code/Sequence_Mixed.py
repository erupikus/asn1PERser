from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


class DataInt(IntegerType):
    pass


class OctetName(OctetStringType):
    pass


class MySeqOf(SequenceOfType):
    componentType = IntegerType()


class MyInnerSeq(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('one', IntegerType()),
        NamedType('two', MySeqOf()),
    )
    componentType = rootComponent


class DataSeq(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('myBool0', BooleanType()),
        NamedType('myBitString', BitStringType()),
        NamedType('myInnerSeq', MyInnerSeq()),
    )
    componentType = rootComponent


class MySeq(SequenceType):
    class some_enum(EnumeratedType):
        enumerationRoot = NamedValues(
            ('one', 0),
            ('two', 1),
            ('three', 2),
        )
        namedValues = enumerationRoot

    class some_seqOf(SequenceOfType):
        componentType = OctetName()

    rootComponent = AdditiveNamedTypes(
        NamedType('some-seq', DataSeq()),
        NamedType('some-enum', some_enum()),
        NamedType('some-integer', DataInt()),
        NamedType('some-seqOf', some_seqOf()),
    )
    componentType = rootComponent


class Record_One(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('value', IntegerType()),
    )
    componentType = rootComponent


class Record_List(SequenceOfType):
    componentType = Record_One()


class MySeq_Two(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('records', Record_List()),
    )
    componentType = rootComponent


