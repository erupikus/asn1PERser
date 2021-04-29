import os
import re
from asn1PERser.classes.templates import Template
from asn1PERser.classes.types.type import SimpleType


typereference_to_type = {}
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
        simple_type_assignments = []
        component_type_assignments = []
        for assignment in AssignmentList:
            if isinstance(assignment, SimpleType):
                if assignment.valuereference:
                    value_assignments.append(assignment)
                else:
                    simple_type_assignments.append(assignment)
            else:
                component_type_assignments.append(assignment)
        return [] + value_assignments + simple_type_assignments + component_type_assignments

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
