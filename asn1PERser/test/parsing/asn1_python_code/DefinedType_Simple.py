from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


class MyInt1(IntegerType):
    subtypeSpec = ValueRange(-5, -1)


class MyOctetString1(OctetStringType):
    subtypeSpec = ValueSize(1, 4)


class MyBitString1(BitStringType):
    pass


class MyBoolean1(BooleanType):
    pass


class MyEnumerated1(EnumeratedType):
    enumerationRoot = NamedValues(
        ('four', 0),
        ('five', 1),
        ('six', 2),
    )
    namedValues = enumerationRoot


class MySeq1(SequenceType):
    rootComponent = AdditiveNamedTypes(
        DefaultedNamedType('d00', IntegerType(10)),
        DefaultedNamedType('d01', IntegerType(0)),
    )
    componentType = rootComponent


MyInt2 = MyInt1


MyOctetString2 = MyOctetString1


MyBitString2 = MyBitString1


MyBoolean2 = MyBoolean1


MyEnumerated2 = MyEnumerated1


MyInt2 = MyInt1


MyInt3 = MyInt2


MyOctetString2 = MyOctetString1


MyOctetString3 = MyOctetString2


MyBitString2 = MyBitString1


MyBitString3 = MyBitString2


MyBoolean2 = MyBoolean1


MyBoolean3 = MyBoolean2


MyEnumerated2 = MyEnumerated1


MyEnumerated3 = MyEnumerated2


class MySeq3(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('d03', MyInt2()),
        NamedType('d04', MyInt3()),
        NamedType('d05', MyOctetString2()),
        NamedType('d06', MyOctetString3()),
        NamedType('d07', MyBitString2()),
        NamedType('d08', MyBitString3()),
        NamedType('d09', MyBoolean2()),
        NamedType('d10', MyBoolean3()),
        NamedType('d11', MyEnumerated2()),
        NamedType('d12', MyEnumerated3()),
    )
    componentType = rootComponent


