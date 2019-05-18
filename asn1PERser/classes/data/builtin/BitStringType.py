from pyasn1.type.univ import BitString
from asn1PERser.codec.per.encoder import encode_bitstring
from asn1PERser.codec.per.decoder import decode_bitstring
from asn1PERser.classes.types.constraint import NoConstraint


class BitStringType(BitString):
    subtypeSpec = NoConstraint()

    def fill_field_list(self, field_list):
        bitstring_field_list = encode_bitstring(self)
        if bitstring_field_list:
            field_list.extend(bitstring_field_list)

    def create_field_list(self, per_bytes):
        decoded = decode_bitstring(self, per_bytes)
        return decoded
