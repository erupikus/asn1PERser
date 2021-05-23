from ..type import SimpleType
from asn1PERser.classes.templates.creator import template_filler
from asn1PERser.classes.module import already_filled_template


class EnumeratedType(SimpleType):
    def __init__(self):
        super(EnumeratedType, self).__init__()
        self._EnumerationItems = []
        self.typereference = self.__class__.__name__

    def fill_template(self, has_parent=False):
        root_named_values = []
        addition_named_values = []
        extension_marker_present = False
        enumeration_index = 0
        for EnumerationItem in self.EnumerationItems:
            if EnumerationItem == '...':
                extension_marker_present = True
                continue
            if not extension_marker_present:
                root_named_values.append({'field_name': str(EnumerationItem).strip(),
                                          'field_index': enumeration_index})
            else:
                addition_named_values.append({'field_name': str(EnumerationItem).strip(),
                                              'field_index': enumeration_index})
            enumeration_index += 1
        filled_template = template_filler.fill(asn_type=self.__class__.__name__,
                                               class_name=self.template_class_name,
                                               class_type=self.__class__.__name__,
                                               extension_marker=extension_marker_present,
                                               root_named_values=root_named_values,
                                               addition_named_values=addition_named_values)
        if has_parent:
            return (None, filled_template)
        if filled_template in already_filled_template:
            return ''
        already_filled_template.add(filled_template)
        return filled_template

    @property
    def EnumerationItems(self):
        return self._EnumerationItems

    @EnumerationItems.setter
    def EnumerationItems(self, EnumerationItem):
        if isinstance(EnumerationItem, str):
            self._EnumerationItems.append(EnumerationItem)
        else:
            self._EnumerationItems.append({EnumerationItem[1]: EnumerationItem[0]})

    def parse_value(self, value):
        return "'" + value + "'"

    def __repr__(self):
        return '\n\t'.join([super(EnumeratedType, self).__repr__()] + \
                           ['{' + str(item).strip() + '}' for item in self.EnumerationItems if item])
