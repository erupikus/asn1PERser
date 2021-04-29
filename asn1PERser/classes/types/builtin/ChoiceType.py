from ..type import ComponentType
from asn1PERser.classes.templates.creator import template_filler
from asn1PERser.classes.module import already_filled_template


class ChoiceType(ComponentType):
    def __init__(self):
        super(ChoiceType, self).__init__()
        self.typereference = self.__class__.__name__
        self._AlternativeTypeList = []

    def fill_template(self, has_parent=False):
        extension_marker_present = False
        root_alternatives_types = []
        addition_alternatives_types = []
        alternatives_templates = []
        subtypes_templates = []
        extension_addition_groups = []
        single_extension_group = []
        in_extension_addition_group = False
        for AlternativeType in self.AlternativeTypeList:
            if AlternativeType == '[[':
                in_extension_addition_group = True
                continue
            if AlternativeType == ']]':
                in_extension_addition_group = False
                extension_addition_groups.append(list(single_extension_group))
                del single_extension_group[:]
                continue
            if in_extension_addition_group:
                single_extension_group.append(self._fill_named_types(AlternativeType))
            if AlternativeType == '...':
                extension_marker_present = True
                continue
            if not in_extension_addition_group:
                if not extension_marker_present:
                    root_alternatives_types.append(self._fill_named_types(AlternativeType))
                else:
                    addition_alternatives_types.append(self._fill_named_types(AlternativeType))
            if AlternativeType.typereference in ['IntegerType', 'BooleanType', 'OctetStringType', 'BitStringType']:
                if AlternativeType.is_constrained():
                    _, subtypes_template = AlternativeType.fill_template(has_parent=True)
                    subtypes_templates.append(subtypes_template[:-2])    # remove 2 last new line characters
                continue
            elif AlternativeType.typereference in ['ChoiceType', 'SequenceType', 'EnumeratedType', 'SequenceOfType']:
                inner_defined_templates, subtypes_template = AlternativeType.fill_template(has_parent=True)
                subtypes_templates.append(subtypes_template[:-2])
                if inner_defined_templates:
                    alternatives_templates.extend(inner_defined_templates)
                continue
            else:
                pass
            alternatives_templates.append(AlternativeType)
        filled_template = template_filler.fill(asn_type=self.__class__.__name__,
                                               class_name=self.template_class_name,
                                               class_type=self.__class__.__name__,
                                               subtemplates=subtypes_templates,
                                               extension_marker=extension_marker_present,
                                               root_alternatives_types=root_alternatives_types,
                                               addition_alternatives_types=addition_alternatives_types,
                                               extension_addition_groups=extension_addition_groups)
        if has_parent:
            return (alternatives_templates, filled_template)
        if filled_template in already_filled_template:
            return ''
        already_filled_template.add(filled_template)
        alternatives_templates = ''.join([alternative_template.fill_template() for alternative_template in alternatives_templates])
        return alternatives_templates + filled_template

    @property
    def AlternativeTypeList(self):
        return self._AlternativeTypeList

    @AlternativeTypeList.setter
    def AlternativeTypeList(self, item):
        self._AlternativeTypeList.append(item)

    def _fill_named_types(self, ComponentType):
        named_type_properties = {'field_name': str(ComponentType.identifier),
                                 'field_type': str(ComponentType.template_field_type)}
        if ComponentType.typereference in ['IntegerType', 'BooleanType', 'OctetStringType', 'BitStringType']:
            if ComponentType.is_constrained():
                named_type_properties['field_type'] = str(ComponentType.template_class_name)
        elif ComponentType.typereference in ['ChoiceType', 'SequenceType', 'EnumeratedType', 'SequenceOfType']:
            named_type_properties['field_type'] = str(ComponentType.template_class_name)
        return named_type_properties

    def __repr__(self):
        if self.AlternativeTypeList:
            alternatives = ''
            for AlternativeType in self.AlternativeTypeList:
                alternatives += '\t' + str(AlternativeType).rstrip() + '\n'
            return '\t' + super(ChoiceType, self).__repr__() + '\n' + alternatives
        return '\t' + super(ChoiceType, self).__repr__()
