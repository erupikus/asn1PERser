from pyasn1.type.univ import Enumerated
from asn1PERser.codec.per.encoder import encode_enumerated
from asn1PERser.codec.per.decoder import decode_enumerated
from asn1PERser.classes.types.constraint import NoConstraint


class EnumeratedType(Enumerated):
    subtypeSpec = NoConstraint()
    enumerationRoot = None
    extensionAddition = None

    def fill_field_list(self, field_list):
        type_field_list = encode_enumerated(self)
        if type_field_list:
            field_list.extend(type_field_list)

    def create_field_list(self, per_bytes):
        decoded = decode_enumerated(self, per_bytes)
        return decoded
