from pyasn1.type.univ import Sequence
from asn1PERser.codec.per.encoder import encode_sequence
from asn1PERser.codec.per.decoder import decode_sequence
from asn1PERser.classes.types.constraint import NoConstraint


class SequenceType(Sequence):
    subtypeSpec = NoConstraint()
    rootComponent = None
    extensionAddition = None
    extensionAdditionGroups = []

    def fill_field_list(self, field_list):
        sequence_field_list = encode_sequence(self)
        if sequence_field_list:
            field_list.extend(sequence_field_list)

    def create_field_list(self, per_bytes):
        decoded = decode_sequence(self, per_bytes)
        return decoded
