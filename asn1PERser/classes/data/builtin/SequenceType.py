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

    def toDict(self, key_name=None):
        component_dict = OrderedDict()
        for componentType, componentValue in self.items():
            if (componentValue is not noValue and componentValue.isValue):
                value_dict = componentValue.toDict(componentType)
                component_dict.update(value_dict)
            elif hasattr(componentValue, 'componentType'):
                value_dict = componentValue.toDict(componentType)
                if value_dict[componentType]:
                    component_dict.update(value_dict)
        return {key_name if key_name else self.__class__.__name__: component_dict}
