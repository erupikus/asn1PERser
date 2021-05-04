from pyasn1.type.univ import Integer
from pyasn1.type.univ import noValue
from asn1PERser.codec.per.encoder import encode_integer
from asn1PERser.codec.per.decoder import decode_integer
from asn1PERser.classes.types.constraint import NoConstraint


class IntegerType(Integer):
    subtypeSpec = NoConstraint()

    def __init__(self, value=noValue, **kwargs):
        super(IntegerType, self).__init__(value, **kwargs)

    def fill_field_list(self, field_list):
        integer_field_list = encode_integer(self)
        if integer_field_list:
            field_list.extend(integer_field_list)

    def create_field_list(self, per_bytes):
        decoded = decode_integer(self, per_bytes)
        return decoded

    def toDict(self, key_name=None):
        return {key_name if key_name else self.__class__.__name__: int(self)}
