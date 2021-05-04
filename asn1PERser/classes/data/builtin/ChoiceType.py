from pyasn1.type.univ import Choice, noValue
from asn1PERser.codec.per.encoder import encode_choice
from asn1PERser.codec.per.decoder import decode_choice
from asn1PERser.classes.types.constraint import NoConstraint


class ChoiceType(Choice):
    subtypeSpec = NoConstraint()
    rootComponent = None
    extensionAddition = None
    extensionAdditionGroups = []

    def fill_field_list(self, field_list):
        choice_field_list = encode_choice(self)
        if choice_field_list:
            field_list.extend(choice_field_list)

    def create_field_list(self, per_bytes):
        decoded = decode_choice(self, per_bytes)
        return decoded

    def toDict(self, key_name=None):
        for componentType, componentValue in self.items():
            if componentValue is not noValue and componentValue.isValue:
                return {key_name if key_name else self.__class__.__name__: componentValue.toDict(componentType)}
