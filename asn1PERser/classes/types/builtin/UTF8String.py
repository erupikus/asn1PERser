from ..type import SimpleType
from asn1PERser.classes.templates.creator import TemplateFiller


class UTF8String(SimpleType):
    def __init__(self):
        super(UTF8String, self).__init__()
        self.typereference = "UTF8String"

    def fill_template(self):
        return TemplateFiller.fill(asn_type=self.__class__.__name__,
                                   class_name=self.template_class_name)

    def __repr__(self):
        return '\t' + super(UTF8String, self).__repr__() + '\n'
