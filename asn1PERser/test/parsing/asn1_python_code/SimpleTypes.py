from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


constant_Int = IntegerType(10)


constant_Bool = BooleanType(True)


constant_Octet_String_one = OctetStringType(hexValue='DEAD')


constant_Octet_String_two = OctetStringType(binValue='11110000')


constant_Bit_String_one = BitStringType(hexValue='BEEF')


constant_Bit_String_two = BitStringType(binValue='01010101')


class MyInt(IntegerType):
    pass


class My_Int(IntegerType):
    pass


class MyBool(BooleanType):
    pass


class My_Bool(BooleanType):
    pass


class MyOctetString(OctetStringType):
    pass


class My_Octet_String(OctetStringType):
    pass


class MyBitString(BitStringType):
    pass


class My_Bit_String(BitStringType):
    pass


class MyEnumerated(EnumeratedType):
    enumerationRoot = NamedValues(
        ('one', 0),
        ('two', 1),
        ('three', 2),
    )
    namedValues = enumerationRoot


class My_Enumerated(EnumeratedType):
    enumerationRoot = NamedValues(
        ('one', 0),
        ('two', 1),
        ('three', 2),
    )
    namedValues = enumerationRoot


my_constant_Int = MyInt(200)


my_constant_Int_Two = My_Int(12345)


my_constant_Bool = MyBool(False)


my_constant_Bool_Two = My_Bool(True)


my_constant_Octet_String_one = MyOctetString(hexValue='FEED')


my_constant_Octet_String_one_Two = My_Octet_String(hexValue='DEEF')


my_constant_Octet_String_two = MyOctetString(binValue='00001111')


my_constant_Octet_String_two_Two = My_Octet_String(binValue='11110000')


my_constant_Bit_String_one = MyBitString(hexValue='ABCD')


my_constant_Bit_String_one_Two = My_Bit_String(hexValue='DCBA')


my_constant_Bit_String_two = MyBitString(binValue='10101010')


my_constant_Bit_String_two_Two = My_Bit_String(binValue='01010101')


