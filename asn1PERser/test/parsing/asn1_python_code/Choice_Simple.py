from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


class MyInteger(IntegerType):
    pass


class MyOctetString(OctetStringType):
    pass


class MyBitString(BitStringType):
    pass


class MyBoolean(BooleanType):
    pass


class Order(ChoiceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('one', IntegerType()),
        NamedType('two', MyInteger()),
        NamedType('three', OctetStringType()),
        NamedType('four', MyOctetString()),
        NamedType('five', BitStringType()),
        NamedType('six', MyBitString()),
        NamedType('seven', BooleanType()),
        NamedType('eight', MyBoolean()),
    )
    componentType = rootComponent


