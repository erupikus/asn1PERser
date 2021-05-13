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

    def toDict(self, is_root=True):
        component_list = []
        for componentValue in self:
            if (componentValue is not noValue and componentValue.isValue) or hasattr(componentValue, 'componentType'):
                value_dict = componentValue.toDict(is_root=False)
                if value_dict is not noValue:
                    component_list.append(value_dict)

        if is_root:
            return component_list
        if not component_list:
            return noValue
        return component_list
