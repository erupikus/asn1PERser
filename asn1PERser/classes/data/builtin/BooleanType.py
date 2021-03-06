from pyasn1.type.univ import Boolean
from asn1PERser.codec.per.encoder import encode_boolean
from asn1PERser.codec.per.decoder import decode_boolean


class BooleanType(Boolean):
    def fill_field_list(self, field_list):
        boolean_field_list = encode_boolean(self)
        if boolean_field_list:
            field_list.extend(boolean_field_list)

    def create_field_list(self, per_bytes):
        decoded = decode_boolean(self, per_bytes)
        return decoded

    def to_dict(self, is_root=True):
        return bool(self)
