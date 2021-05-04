from collections import OrderedDict
from pyasn1.type.univ import SequenceOf, noValue
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

    def toDict(self, key_name=None):
        component_list = []
        for component in self.components:
            component_dict = component.toDict()
            for k,v in component_dict.items():
                component_list.append(v)
        return {key_name if key_name else self.__class__.__name__: component_list}
