from pyasn1.type.univ import OctetString
from asn1PERser.codec.per.encoder import encode_octetstring
from asn1PERser.codec.per.decoder import decode_octetstring
from asn1PERser.classes.types.constraint import NoConstraint


class OctetStringType(OctetString):
    subtypeSpec = NoConstraint()

    def fill_field_list(self, field_list):
        octetstring_field_list = encode_octetstring(self)
        if octetstring_field_list:
            field_list.extend(octetstring_field_list)

    def create_field_list(self, per_bytes):
        decoded = decode_octetstring(self, per_bytes)
        return decoded

    def toDict(self, key_name=None):
        return {key_name if key_name else self.__class__.__name__: ''.join(format(byte, 'x') for byte in self.asNumbers())}
