import os
import re
import logging
from asn1PERser.classes.templates import Template
from asn1PERser.classes.types.type import SimpleType, ComponentType, DefType


logger = logging.getLogger("asn1perser.moduleParser")

typereference_to_type = {}
valuereference_to_type = {}
constants = {}
already_filled_template = set()


class ModuleDefinition(Template):
    def __init__(self):
        self._ModuleIdentifier = ''
        self._EncodingReferenceDefault = ''
        self._TagDefault = ''
        self._ExtensionDefault = ''
        self._ModuleBody = ''

    def create_python_template(self, path=None):
        template = self.fill_template()
        if not path:
            return template
        with open(os.path.join(path, self.ModuleIdentifier + '.py'), 'w') as template_file:
            template_file.write(template)

    def fill_template(self):
        already_filled_template.clear()
        template = super(ModuleDefinition, self).fill_template()
        if self.ModuleBody:
            for Assignment in self.ModuleBody:
                template += Assignment.fill_template()
        return template

    def sort_assigment_list(self, AssignmentList):
        value_assignments = []
        constant_assignments = []
        simple_type_assignments = []
        component_type_assignments = []
        type_type_assignments = []
        for assignment in AssignmentList:
            if isinstance(assignment, SimpleType):
                if assignment.valuereference:
                    value_assignments.append(assignment)
                else:
                    simple_type_assignments.append(assignment)
            elif isinstance(assignment, DefType):
                if assignment.valuereference:
                    constant_assignments.append(assignment)
                    constants[assignment.valuereference] = assignment
                else:
                    type_type_assignments.append(assignment)
            else:
                component_type_assignments.append(assignment)
        component_type_assignments = self.sort_components(component_type_assignments)
        type_type_assignments, component_type_assignments = self.additional_sort(type_type_assignments, component_type_assignments)
        return [] + value_assignments + simple_type_assignments + type_type_assignments + constant_assignments + component_type_assignments

    def sort_components(self, component_type_assignments):
        MAX_ITERATIONS = 100
        all_sorted = False
        already_moved_typereferences = []
        new_order_typereferences = []
        new_order_components = []
        iter = 0

        while iter != MAX_ITERATIONS:
            components_typereferences = [component_type.typereference for component_type in component_type_assignments]
            if all_sorted:
                break
            all_sorted = True
            iter += 1
            for component_index in range(len(component_type_assignments)):
                ComponentType = component_type_assignments[component_index]
                for subcomponent in self._get_subcomponents(ComponentType):
                    if subcomponent.typereference in new_order_typereferences:
                        continue

                    try:
                        inner_component_index = components_typereferences.index(subcomponent.typereference)
                    except ValueError:
                        continue
                    if inner_component_index > component_index and subcomponent.typereference not in already_moved_typereferences:
                        new_order_typereferences.append(subcomponent.typereference)
                        new_order_components.append(component_type_assignments[inner_component_index])
                        already_moved_typereferences.append(subcomponent.typereference)
                        all_sorted = False
                else:
                    if ComponentType.typereference not in new_order_typereferences:
                        new_order_typereferences.append(ComponentType.typereference)
                        new_order_components.append(ComponentType)

            component_type_assignments = new_order_components[:]
            new_order_components = []
            new_order_typereferences = []
            already_moved_typereferences = []
        else:
            logger.warning("Could not sort components properly. This could lead to 'NameError' as some class"
                           " definition may be lower than its instantiation (Python reads .py files"
                           " from top to bottom.")
        return component_type_assignments

    def _get_subcomponents(self, component):
        subcomponents = []
        if component.__class__.__name__ == 'DefinedType':
            return [component]
        for subcomponent in component:
            if isinstance(subcomponent, str):  # elipsis: ...
                continue
            if subcomponent.typereference in ['IntegerType', 'BooleanType', 'OctetStringType',
                                              'BitStringType', 'EnumeratedType']:
                continue
            if subcomponent.typereference in ['ChoiceType', 'SequenceType', 'SequenceOfType']:
                subcomponents += self._get_subcomponents(subcomponent)
            else:
                subcomponents.append(subcomponent)
        return subcomponents

    def additional_sort(self, type_type_assignments, component_type_assignments):
        components_typereferences = [component_type.typereference for component_type in component_type_assignments]
        type_type_typereferences = [type_type.typereference for type_type in type_type_assignments]

        new_type_type_assignments = []

        for type_index in range(len(type_type_typereferences)):
            type_type_typereference = type_type_typereferences[type_index]
            try:
                type_in_components_index = components_typereferences.index(type_type_typereference)
            except ValueError:
                new_type_type_assignments.append(type_type_assignments[type_index])
                continue

            type_type_component = type_type_assignments[type_index]
            component_type_assignments.insert(type_in_components_index + 1, type_type_component)
            components_typereferences = [component_type.typereference for component_type in component_type_assignments]

        return (new_type_type_assignments, component_type_assignments)

    @property
    def ModuleIdentifier(self):
        return self._ModuleIdentifier

    @ModuleIdentifier.setter
    def ModuleIdentifier(self, ModuleIdentifier):
        self._ModuleIdentifier = ModuleIdentifier

    @property
    def EncodingReferenceDefault(self):
        return self._EncodingReferenceDefault

    @EncodingReferenceDefault.setter
    def EncodingReferenceDefault(self, EncodingReferenceDefault):
        self._EncodingReferenceDefault = EncodingReferenceDefault

    @property
    def TagDefault(self):
        return self._TagDefault

    @TagDefault.setter
    def TagDefault(self, TagDefault):
        self._TagDefault = TagDefault

    @property
    def ExtensionDefault(self):
        return self._ExtensionDefault

    @ExtensionDefault.setter
    def ExtensionDefault(self, ExtensionDefault):
        self._ExtensionDefault = ExtensionDefault

    @property
    def ModuleBody(self):
        return self._ModuleBody

    @ModuleBody.setter
    def ModuleBody(self, AssignmentList):
        self._ModuleBody = self.sort_assigment_list(AssignmentList)

    def __repr__(self):
        module_str = self.ModuleIdentifier
        if self.EncodingReferenceDefault:
            module_str += ' ' + self.EncodingReferenceDefault
        if self.TagDefault:
            module_str += ' ' + self.TagDefault
        if self.ExtensionDefault:
            module_str += ' ' + self.ExtensionDefault
        module_str += ' ' + 'BEGIN' + '\n'
        if self.ModuleBody:
            for Assignment in self.ModuleBody:
                module_str += str(Assignment)
        module_str += 'END'
        return module_str


def remove_comments(asn1_schema):
    return _remove_line_comments(asn1_schema)


def _remove_line_comments(asn1_schema):
    no_comments = ''
    for line in asn1_schema.splitlines():
        line = re.sub('--.*', '', line)
        line += '\n'
        no_comments += line
    return no_comments
