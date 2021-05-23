from ..type import SimpleType
from asn1PERser.classes.templates.creator import template_filler
from asn1PERser.classes.module import already_filled_template


class IntegerType(SimpleType):
    def __init__(self):
        super(IntegerType, self).__init__()
        self.typereference = self.__class__.__name__

    def fill_template(self, has_parent=False):
        if self.Value:
            return template_filler.fill(asn_type=self.__class__.__name__, type_or_value='value',
                                        valuereference=self.valuereference, value=self.Value,
                                        class_type=self.template_field_type)
        filled_template = template_filler.fill(asn_type=self.__class__.__name__, type_or_value='type',
                                               class_name=self.template_class_name, class_type=self.__class__.__name__,
                                               constraint={'extensionMarker': self.constraint.extensionMarker,
                                                           'lowerEndpoint': self.constraint.lowerEndpoint,
                                                           'upperEndpoint': self.constraint.upperEndpoint})
        if has_parent:
            return (None, filled_template)
        if filled_template not in already_filled_template:
            already_filled_template.add(filled_template)
            return filled_template
        return ''
