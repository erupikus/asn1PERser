from ..type import Type
from asn1PERser.classes.module import typereference_to_type
from asn1PERser.classes.templates.creator import template_filler


class DefinedType(Type):
    def __init__(self, typereference):
        super().__init__()
        self.typereference = typereference

    def fill_template(self):
        defined_type = typereference_to_type[self.typereference]
        defined_type.valuereference = self.valuereference

        if self.Value:
            defined_type.Value = self.Value
            return defined_type.fill_template()
        if defined_type.__class__.__name__ != self.__class__.__name__:
            return defined_type.fill_template()
        return template_filler.fill(asn_type=self.__class__.__name__, type_or_value='type',
                                    class_name=self.template_field_type, class_type=defined_type.template_class_name)

    @property
    def default(self):
        if self.typereference in typereference_to_type.keys():
            defined_type = typereference_to_type[self.typereference]
            if self._default:
                return defined_type.parse_value(self._default)
            return self._default
        return self._default

    @default.setter
    def default(self, default):
        self._default = default


    def __repr__(self):
        return '\t' + super().__repr__() + '\n'
