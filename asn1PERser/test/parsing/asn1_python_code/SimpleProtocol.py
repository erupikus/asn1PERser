from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


class Port(IntegerType):
    subtypeSpec = ValueRange(10000, 65535)


class SequenceNumber(IntegerType):
    subtypeSpec = ValueRange(0, 65535)


class Message(OctetStringType):
    subtypeSpec = ValueSize(1, 4)


class UTC_Timestamp(SequenceType):
    class seconds(IntegerType):
        subtypeSpec = ValueRange(0, 4294967295)

    class useconds(IntegerType):
        subtypeSpec = ValueRange(0, 4294967295)

    rootComponent = AdditiveNamedTypes(
        NamedType('seconds', seconds()),
        NamedType('useconds', useconds()),
    )
    componentType = rootComponent


class Start(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('sequenceNumber', SequenceNumber()),
        NamedType('timestamp', UTC_Timestamp()),
        NamedType('srcPort', Port()),
        NamedType('dstPort', Port()),
    )
    componentType = rootComponent


class Stop(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('sequenceNumber', SequenceNumber()),
        NamedType('timestamp', UTC_Timestamp()),
        NamedType('srcPort', Port()),
        NamedType('dstPort', Port()),
    )
    componentType = rootComponent


class Alive(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('timestamp', UTC_Timestamp()),
    )
    componentType = rootComponent


class Payload(SequenceOfType):
    subtypeSpec = SequenceOfValueSize(1, 5)
    componentType = Message()


class Data(SequenceType):
    class swRelease(EnumeratedType):
        subtypeSpec = ExtensionMarker(True)
        enumerationRoot = NamedValues(
            ('rel1', 0),
            ('rel2', 1),
            ('rel3', 2),
        )
        namedValues = enumerationRoot

    class macroId(BitStringType):
        subtypeSpec = ValueSize(20, 20)

    rootComponent = AdditiveNamedTypes(
        NamedType('sequenceNumber', SequenceNumber()),
        NamedType('swRelease', swRelease()),
        OptionalNamedType('macroId', macroId()),
        NamedType('payload', Payload()),
    )
    componentType = rootComponent


class SimpleMessage(ChoiceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('start', Start()),
        NamedType('stop', Stop()),
        NamedType('alive', Alive()),
        NamedType('data', Data()),
    )
    componentType = rootComponent


