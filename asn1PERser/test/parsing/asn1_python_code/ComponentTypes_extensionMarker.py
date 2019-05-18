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
    namedValues = enumerationRoot


class ThirdSequence(SequenceOfType):
    componentType = OctetStringType()


class MyChoice(ChoiceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('c0', IntegerType()),
        NamedType('c1', ThirdSequence()),
        NamedType('c2', BooleanType()),
    )
    componentType = rootComponent


class YetOtherSeq(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('myEnum', MyEnum()),
        NamedType('myChoice', MyChoice()),
    )
    componentType = rootComponent


class OtherSequence(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('yetOtherSeq', YetOtherSeq()),
        NamedType('myBool', BooleanType()),
    )
    componentType = rootComponent


class MySeq(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('int0', IntegerType()),
        NamedType('otherSeq', OtherSequence()),
    )
    componentType = rootComponent


