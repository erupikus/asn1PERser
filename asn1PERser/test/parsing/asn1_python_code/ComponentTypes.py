from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


class Meters(IntegerType):
    pass


class Picture(OctetStringType):
    pass


class MoveOrder(ChoiceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('up', Meters()),
        NamedType('down', Meters()),
        NamedType('left', Meters()),
        NamedType('right', Meters()),
    )
    componentType = rootComponent


class Data(SequenceType):
    class pictures(SequenceOfType):
        componentType = Picture()

    rootComponent = AdditiveNamedTypes(
        NamedType('id', IntegerType()),
        NamedType('pictures', pictures()),
    )
    componentType = rootComponent


class Order(ChoiceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('move', MoveOrder()),
        NamedType('sendData', Data()),
    )
    componentType = rootComponent


