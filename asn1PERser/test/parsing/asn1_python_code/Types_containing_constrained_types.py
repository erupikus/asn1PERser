from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


minNumber = IntegerType(-10)


maxNumber = IntegerType(255)


class MyEnum(EnumeratedType):
    subtypeSpec = ExtensionMarker(True)
    enumerationRoot = NamedValues(
        ('one', 0),
        ('two', 1),
        ('three', 2),
    )
    namedValues = enumerationRoot


class MySeq1(SequenceType):
    class my_Int1(IntegerType):
        subtypeSpec = ValueRange(minNumber, 10, extensionMarker=True)

    class myBitString1(BitStringType):
        subtypeSpec = ValueSize(0, maxNumber)

    class myOctetString1(OctetStringType):
        subtypeSpec = ValueSize(1, 4)

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('my-Int1', my_Int1()),
        NamedType('my-Int2', IntegerType()),
        NamedType('myBitString1', myBitString1()),
        NamedType('myOctetString1', myOctetString1()),
    )
    componentType = rootComponent


class MySeq2(SequenceType):
    class myOctetString2(OctetStringType):
        subtypeSpec = ValueSize(1, 4, extensionMarker=True)

    class myInt4(IntegerType):
        subtypeSpec = ValueRange(MIN, 1)

    rootComponent = AdditiveNamedTypes(
        NamedType('myInt3', IntegerType()),
        NamedType('myOctetString2', myOctetString2()),
        NamedType('myInt4', myInt4()),
    )
    componentType = rootComponent


class Data(SequenceType):
    class i0(IntegerType):
        subtypeSpec = ValueRange(0, MAX)

    class i2(OctetStringType):
        subtypeSpec = ValueSize(1, 10)

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('i0', i0()),
        NamedType('i1', OctetStringType()),
    )
    extensionAddition = AdditiveNamedTypes(
        NamedType('i2', i2()),
    )
    componentType = rootComponent + extensionAddition


class DataList(SequenceOfType):
    subtypeSpec = SequenceOfValueSize(1, 10)
    componentType = Data()


class MyChoice(ChoiceType):
    class c0(OctetStringType):
        subtypeSpec = ValueSize(0, maxNumber, extensionMarker=True)

    class c_two(IntegerType):
        subtypeSpec = ValueRange(MIN, 0)

    class c4(BitStringType):
        subtypeSpec = ValueSize(0, 20)

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('c0', c0()),
        NamedType('c1', IntegerType()),
        NamedType('c-two', c_two()),
    )
    extensionAddition = AdditiveNamedTypes(
        NamedType('c3', MyEnum()),
        NamedType('c4', c4()),
    )
    componentType = rootComponent + extensionAddition


