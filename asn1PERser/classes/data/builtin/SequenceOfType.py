from pyasn1.type.univ import SequenceOf
from asn1PERser.codec.per.encoder import encode_sequence_of
from asn1PERser.codec.per.decoder import decode_sequence_of
from asn1PERser.classes.types.constraint import SequenceOfValueSize, MAX


class SequenceOfType(SequenceOf):
    subtypeSpec = SequenceOfValueSize(0, MAX)

    def fill_field_list(self, field_list):
        sequence_of_field_list = encode_sequence_of(self)
        if sequence_of_field_list:
            field_list.extend(sequence_of_field_list)

    def create_field_list(self, per_bytes):
        decoded = decode_sequence_of(self, per_bytes)
        return decoded
