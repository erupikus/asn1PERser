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


class MyEnumerated(EnumeratedType):
    enumerationRoot = NamedValues(
        ('four', 0),
        ('five', 1),
        ('six', 2),
    )
    namedValues = enumerationRoot


class MySeq(SequenceType):
    class d24(EnumeratedType):
        enumerationRoot = NamedValues(
            ('one', 0),
            ('two', 1),
            ('three', 2),
        )
        namedValues = enumerationRoot

    rootComponent = AdditiveNamedTypes(
        DefaultedNamedType('d00', IntegerType(10)),
        DefaultedNamedType('d01', IntegerType(0)),
        DefaultedNamedType('d02', MyInteger(11)),
        DefaultedNamedType('d03', MyInteger(0)),
        DefaultedNamedType('d04', OctetStringType(binValue='11111111')),
        DefaultedNamedType('d05', OctetStringType(binValue='')),
        DefaultedNamedType('d06', OctetStringType(hexValue='AAAA')),
        DefaultedNamedType('d07', OctetStringType(hexValue='')),
        DefaultedNamedType('d08', MyOctetString(binValue='01010101')),
        DefaultedNamedType('d09', MyOctetString(binValue='')),
        DefaultedNamedType('d10', MyOctetString(hexValue='BBBB')),
        DefaultedNamedType('d11', MyOctetString(hexValue='')),
        DefaultedNamedType('d12', BitStringType(binValue='0000')),
        DefaultedNamedType('d13', BitStringType(binValue='')),
        DefaultedNamedType('d14', BitStringType(hexValue='DDDD')),
        DefaultedNamedType('d15', BitStringType(hexValue='')),
        DefaultedNamedType('d16', MyBitString(binValue='10101')),
        DefaultedNamedType('d17', MyBitString(binValue='')),
        DefaultedNamedType('d18', MyBitString(hexValue='EE')),
        DefaultedNamedType('d19', MyBitString(hexValue='')),
        DefaultedNamedType('d20', BooleanType(False)),
        DefaultedNamedType('d21', BooleanType(True)),
        DefaultedNamedType('d22', MyBoolean(False)),
        DefaultedNamedType('d23', MyBoolean(True)),
        DefaultedNamedType('d24', d24('two')),
        DefaultedNamedType('d25', MyEnumerated('six')),
    )
    componentType = rootComponent


