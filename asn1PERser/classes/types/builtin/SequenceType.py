from ..type import ComponentType
from asn1PERser.classes.templates.creator import template_filler
from asn1PERser.classes.module import already_filled_template


class SequenceType(ComponentType):
    def __init__(self):
        super(SequenceType, self).__init__()
        self._ComponentTypeList = []
        self.typereference = self.__class__.__name__

    def fill_template(self, has_parent=False):
        root_named_types = []
        addition_named_types = []
        subtypes_templates = []
        components_templates = []
        extension_addition_groups = []
        single_extension_group = []
        in_extension_addition_group = False
        extension_marker_present = False
        for ComponentType in self.ComponentTypeList:
            if ComponentType == '[[':
                in_extension_addition_group = True
                continue
            if ComponentType == ']]':
                in_extension_addition_group = False
                extension_addition_groups.append(list(single_extension_group))
                del single_extension_group[:]
                continue
            if in_extension_addition_group:
                single_extension_group.append(self._fill_named_types(ComponentType))
            if ComponentType == '...':
                extension_marker_present = True
                continue
            if not in_extension_addition_group:
                if not extension_marker_present:
                    root_named_types.append(self._fill_named_types(ComponentType))
                else:
                    addition_named_types.append(self._fill_named_types(ComponentType))
            if ComponentType.typereference in ['IntegerType', 'BooleanType', 'OctetStringType', 'BitStringType']:
                if ComponentType.is_constrained():
                    _, subtypes_template = ComponentType.fill_template(has_parent=True)
                    subtypes_templates.append(subtypes_template[:-2])    # remove 2 last new line characters
                continue
            elif ComponentType.typereference in ['ChoiceType', 'SequenceType', 'EnumeratedType', 'SequenceOfType']:
                inner_defined_templates, subtypes_template = ComponentType.fill_template(has_parent=True)
                subtypes_templates.append(subtypes_template[:-2])
                if inner_defined_templates:
                    components_templates.extend(inner_defined_templates)
                continue
            else:
                pass
            components_templates.append(ComponentType)
        filled_template = template_filler.fill(asn_type=self.__class__.__name__,
                                               class_name=self.template_class_name,
                                               class_type=self.__class__.__name__,
                                               subtemplates=subtypes_templates,
                                               extension_marker=extension_marker_present,
                                               root_named_types=root_named_types,
                                               addition_named_types=addition_named_types,
                                               extension_addition_groups=extension_addition_groups)
        if has_parent:
            return (components_templates, filled_template)
        if filled_template in already_filled_template:
            return ''
        already_filled_template.add(filled_template)
        components_templates = ''.join([component_template.fill_template() for component_template in components_templates])
        return components_templates + filled_template

    @property
    def ComponentTypeList(self):
        return self._ComponentTypeList

    @ComponentTypeList.setter
    def ComponentTypeList(self, item):
        self._ComponentTypeList.append(item)

    def _fill_named_types(self, ComponentType):
        named_type_properties = {'optional': False,
                                 'default': False,
                                 'field_name': str(ComponentType.identifier),
                                 'field_type': str(ComponentType.template_field_type)}
        if ComponentType.typereference in ['IntegerType', 'BooleanType', 'OctetStringType', 'BitStringType']:
            if ComponentType.is_constrained():
                named_type_properties['field_type'] = str(ComponentType.template_class_name)
        elif ComponentType.typereference in ['ChoiceType', 'SequenceType', 'EnumeratedType', 'SequenceOfType']:
            named_type_properties['field_type'] = str(ComponentType.template_class_name)
        if ComponentType.optional:
            named_type_properties['optional'] = True
        elif ComponentType.default is not None:
            named_type_properties['default'] = True
            named_type_properties['default_value'] = str(ComponentType.default)
        else:
            pass
        return named_type_properties

    def __repr__(self):
        return '\n\t'.join([super(SequenceType, self).__repr__()] + \
                           [str(ComponentType) for ComponentType in self.ComponentTypeList])
