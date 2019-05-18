from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


minNumber = IntegerType(-10)


maxNumber = IntegerType(255)


class MyBitString(BitStringType):
    subtypeSpec = ValueSize(1, maxNumber, extensionMarker=True)


class TcpData(IntegerType):
    pass


class SrcUdpTput(IntegerType):
    pass


class TgtUdpTput(IntegerType):
    pass


class InnerSequence(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('i0', IntegerType()),
        NamedType('i1', IntegerType()),
    )
    componentType = rootComponent


class MySeq1(SequenceType):
    class data(ChoiceType):
        class my_int_2(IntegerType):
            subtypeSpec = ValueRange(1, 2)

        rootComponent = AdditiveNamedTypes(
            NamedType('inner-seq', InnerSequence()),
            NamedType('my-int-1', IntegerType()),
            NamedType('my-int-2', my_int_2()),
            NamedType('my-bit', MyBitString()),
        )
        componentType = rootComponent

    class my_int_3(IntegerType):
        subtypeSpec = ValueRange(10, 20)

    rootComponent = AdditiveNamedTypes(
        NamedType('data', data()),
        NamedType('my-int-3', my_int_3()),
        NamedType('my-octet', OctetStringType()),
    )
    componentType = rootComponent


class MySeq2(SequenceType):
    class enum_one(EnumeratedType):
        subtypeSpec = ExtensionMarker(True)
        enumerationRoot = NamedValues(
            ('one', 0),
            ('two', 1),
        )
        namedValues = enumerationRoot

    class o1(OctetStringType):
        subtypeSpec = ValueSize(1, 10)

    rootComponent = AdditiveNamedTypes(
        NamedType('i0', IntegerType()),
        NamedType('enum-one', enum_one()),
        NamedType('o1', o1()),
    )
    componentType = rootComponent


class SrcTcpData(SequenceType):
    class data(SequenceOfType):
        subtypeSpec = SequenceOfValueSize(1, maxNumber)
        componentType = TcpData()

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('data', data()),
    )
    componentType = rootComponent


class TgtTcpData(SequenceType):
    class data(SequenceOfType):
        subtypeSpec = SequenceOfValueSize(1, maxNumber)
        componentType = TcpData()

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('data', data()),
    )
    componentType = rootComponent


class SrcUdpData(SequenceType):
    class data(SequenceOfType):
        subtypeSpec = SequenceOfValueSize(1, maxNumber)
        componentType = SrcUdpTput()

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('data', data()),
    )
    componentType = rootComponent


class TgtUdpData(SequenceType):
    class data(SequenceOfType):
        subtypeSpec = SequenceOfValueSize(1, maxNumber)
        componentType = TgtUdpTput()

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('data', data()),
    )
    componentType = rootComponent


class BigIpData(SequenceType):
    class d0(IntegerType):
        subtypeSpec = ValueRange(-1, 1)

    class d1(OctetStringType):
        subtypeSpec = ValueSize(1, 20)

    rootComponent = AdditiveNamedTypes(
        NamedType('d0', d0()),
        NamedType('d1', d1()),
    )
    componentType = rootComponent


class IpData(SequenceType):
    class data(SequenceOfType):
        subtypeSpec = SequenceOfValueSize(1, maxNumber)
        componentType = BigIpData()

    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('data', data()),
    )
    componentType = rootComponent


class MyChoice(ChoiceType):
    class enum_two(EnumeratedType):
        enumerationRoot = NamedValues(
            ('three', 0),
            ('four', 1),
        )
        namedValues = enumerationRoot

    class inner_seq_2(SequenceType):
        class i1(BitStringType):
            subtypeSpec = ValueSize(1, 2)

        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
            NamedType('i1', i1()),
        )
        componentType = rootComponent

    class o1(OctetStringType):
        subtypeSpec = ValueSize(1, 10)

    rootComponent = AdditiveNamedTypes(
        NamedType('enum-two', enum_two()),
        NamedType('inner-seq-2', inner_seq_2()),
        NamedType('o1', o1()),
        NamedType('my-int-4', IntegerType()),
    )
    componentType = rootComponent


