from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


class MyEnum(EnumeratedType):
    subtypeSpec = ExtensionMarker(True)
    enumerationRoot = NamedValues(
        ('zero', 0),
        ('one', 1),
        ('two', 2),
        ('three', 3),
    )
    extensionAddition = NamedValues(
        ('four', 4),
        ('five', 5),
    )
    namedValues = enumerationRoot + extensionAddition


class ThirdSequence(SequenceOfType):
    componentType = OctetStringType()


class MyChoice(ChoiceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('c0', IntegerType()),
        NamedType('c1', ThirdSequence()),
        NamedType('c2', BooleanType()),
    )
    extensionAddition = AdditiveNamedTypes(
        NamedType('c3', IntegerType()),
        NamedType('c4', BooleanType()),
    )
    componentType = rootComponent + extensionAddition


class YetOtherSeq(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('myEnum', MyEnum()),
        NamedType('myChoice', MyChoice()),
    )
    extensionAddition = AdditiveNamedTypes(
        NamedType('add3', OctetStringType()),
        NamedType('add4', IntegerType()),
    )
    componentType = rootComponent + extensionAddition


class OtherSequence(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('yetOtherSeq', YetOtherSeq()),
        NamedType('myBool', BooleanType()),
    )
    extensionAddition = AdditiveNamedTypes(
        NamedType('add2', BitStringType()),
    )
    componentType = rootComponent + extensionAddition


class MySeq(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('int0', IntegerType()),
        NamedType('otherSeq', OtherSequence()),
    )
    extensionAddition = AdditiveNamedTypes(
        NamedType('add0', IntegerType()),
        NamedType('add1', BooleanType()),
    )
    componentType = rootComponent + extensionAddition


