from ..type import DefType, SimpleType
from asn1PERser.classes.module import typereference_to_type
from asn1PERser.classes.templates.creator import template_filler


class DefinedType(DefType):
    def __init__(self, typereference):
        super(DefinedType, self).__init__()
        self.typereference = typereference

    def fill_template(self):
        defined_type = typereference_to_type[self.typereference]

        if self.identifier and self.typereference and not self.Value:  # Foo ::= Bar
            return template_filler.fill(asn_type='type_type', type_or_value='type',
                                        identifier=self.identifier.replace('-', '_'),
                                        typereference=self.typereference.replace('-', '_'))

        if self.Value and self.valuereference and self.typereference:  # foo SomeType ::= value
            while not defined_type.__class__.__name__ in ['IntegerType', 'BooleanType', 'OctetStringType', 'BitStringType']:
                defined_type = typereference_to_type[defined_type.typereference]
            defined_type.valuereference = self.valuereference
            defined_type.typereference = self.typereference
            defined_type.Value = self.Value
            return template_filler.fill(asn_type='simple_value', type_or_value='value',
                                        valuereference=self.valuereference,
                                        class_type=self.typereference.replace('-','_'),
                                        value=defined_type.Value)
        if self.Value:
            defined_type.Value = self.Value
            return defined_type.fill_template()
        if defined_type.__class__.__name__ != self.__class__.__name__:
            return defined_type.fill_template()
        return template_filler.fill(asn_type=self.__class__.__name__, type_or_value='type',
                                    class_name=self.template_field_type, class_type=defined_type.template_class_name)
