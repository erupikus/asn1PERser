from .creator import template_filler


class Template(object):
    def fill_template(self):
        return template_filler.fill('header')

    @property
    def template_class_name(self):
        return self.identifier.replace('-','_') if self.identifier else self.typereference.replace('-','_')

    @property
    def template_field_type(self):
        return self.typereference.replace('-','_') if self.typereference else self.identifier.replace('-','_')
