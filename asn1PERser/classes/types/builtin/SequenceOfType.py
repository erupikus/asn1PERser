from ..type import ComponentType
from asn1PERser.classes.templates.creator import template_filler
from asn1PERser.classes.module import already_filled_template


class SequenceOfType(ComponentType):
    def __init__(self):
        super(SequenceOfType, self).__init__()
        self._ComponentType = None
        self.typereference = self.__class__.__name__

    def fill_template(self, has_parent=False):
        filled_template = template_filler.fill(asn_type=self.__class__.__name__,
                                               class_name=self.template_class_name,
                                               class_type=self.__class__.__name__,
                                               field_type=self.ComponentType.template_field_type,
                                               constraint={'extensionMarker': self.constraint.extensionMarker,
                                                           'lowerEndpoint': self.constraint.lowerEndpoint,
                                                           'upperEndpoint': self.constraint.upperEndpoint})
        if has_parent:
            return ([self.ComponentType], filled_template)
        if filled_template in already_filled_template:
            return ''
        already_filled_template.add(filled_template)
        if self.ComponentType.typereference in ['IntegerType', 'BooleanType', 'OctetStringType', 'BitStringType']:
            return filled_template
        components_template = self.ComponentType.fill_template()
        return components_template + filled_template

    @property
    def ComponentType(self):
        return self._ComponentType

    @ComponentType.setter
    def ComponentType(self, ComponentType):
        self._ComponentType = ComponentType

    def __repr__(self):
        return '\n\t'.join([super(SequenceOfType, self).__repr__(), str(self.ComponentType)])