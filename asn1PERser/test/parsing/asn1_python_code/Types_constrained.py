from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


maxNumber = IntegerType(255)


class MyInt1(IntegerType):
    subtypeSpec = ValueRange(-5, -1)


class MyInt2(IntegerType):
    subtypeSpec = ValueRange(-25, 20000000, extensionMarker=True)


class MyInt3(IntegerType):
    subtypeSpec = ValueRange(-25, MAX)


class MyInt4(IntegerType):
    subtypeSpec = ValueRange(MIN, 0)


class MyInt5(IntegerType):
    subtypeSpec = ValueRange(MIN, maxNumber)


class MyOctetString1(OctetStringType):
    subtypeSpec = ValueSize(1, 4)


class MyOctetString2(OctetStringType):
    subtypeSpec = ValueSize(0, 30, extensionMarker=True)


class MyOctetString3(OctetStringType):
    subtypeSpec = ValueSize(0, maxNumber, extensionMarker=True)


class MyBitString1(BitStringType):
    subtypeSpec = ValueSize(10, 100)


class MyBitString2(BitStringType):
    subtypeSpec = ValueSize(100, 10000, extensionMarker=True)


class MyBitString3(BitStringType):
    subtypeSpec = ValueSize(0, maxNumber, extensionMarker=True)


class MySeqOf1(SequenceOfType):
    subtypeSpec = SequenceOfValueSize(1, maxNumber)
    componentType = OctetStringType()


class MySeqOf2(SequenceOfType):
    subtypeSpec = SequenceOfValueSize(1, maxNumber, extensionMarker=True)
    componentType = MyBitString1()


