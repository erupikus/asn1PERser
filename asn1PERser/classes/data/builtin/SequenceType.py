from collections import OrderedDict
from pyasn1.type.univ import Sequence, noValue
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

    def to_dict(self, is_root=True):
        component_dict = OrderedDict()
        for componentType, componentValue in self.items():
            if (componentValue is not noValue and componentValue.isValue) or hasattr(componentValue, 'componentType'):
                value_dict = componentValue.to_dict(is_root=False)
                if value_dict is not noValue:
                    component_dict[componentType] = value_dict

        if is_root:
            return component_dict
        if not component_dict:
            return noValue
        return component_dict
