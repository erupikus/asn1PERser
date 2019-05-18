from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


class MyEnum(EnumeratedType):
    enumerationRoot = NamedValues(
        ('one', 0),
        ('two', 1),
    )
    namedValues = enumerationRoot


class MySeq(SequenceType):
    class i0(IntegerType):
        subtypeSpec = ValueRange(10, 20)

    rootComponent = AdditiveNamedTypes(
        NamedType('i0', i0()),
        NamedType('i1', IntegerType()),
    )
    componentType = rootComponent


class Data1(SequenceType):
    class d1(BitStringType):
        subtypeSpec = ValueSize(1, 20, extensionMarker=True)

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('d0', OctetStringType()),
    )
    extensionAdditionGroups = [
        AdditiveNamedTypes(
            NamedType('d1', d1()),
            NamedType('d2', MySeq()),
        ),
    ]
    componentType = rootComponent + extensionAdditionGroups


class Data2(ChoiceType):
    class c0(IntegerType):
        subtypeSpec = ValueRange(1, MAX)

    class c3(OctetStringType):
        subtypeSpec = ValueSize(5, 10)

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('c0', c0()),
    )
    extensionAdditionGroups = [
        AdditiveNamedTypes(
            NamedType('c1', MyEnum()),
            NamedType('c2', BooleanType()),
        ),
        AdditiveNamedTypes(
            NamedType('c3', c3()),
            NamedType('c4', MySeq()),
        ),
    ]
    componentType = rootComponent + extensionAdditionGroups


class Data3(SequenceType):
    class s3(IntegerType):
        subtypeSpec = ValueRange(-10, 100)

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('s0', IntegerType()),
    )
    extensionAddition = AdditiveNamedTypes(
        NamedType('s4', IntegerType()),
        NamedType('s5', IntegerType()),
    )
    extensionAdditionGroups = [
        AdditiveNamedTypes(
            NamedType('s1', MySeq()),
            OptionalNamedType('s2', IntegerType()),
        ),
        AdditiveNamedTypes(
            NamedType('s3', s3()),
            NamedType('s6', MyEnum()),
        ),
    ]
    componentType = rootComponent + extensionAddition + extensionAdditionGroups


