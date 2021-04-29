import os
from jinja2 import Environment, FileSystemLoader


class TemplateFiller(object):
    def __init__(self):
        file_loader = FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files/'))
        self.env = Environment(loader=file_loader)

    def fill(self, asn_type, type_or_value='type', **kwargs):
        if asn_type in ('BooleanType', 'IntegerType', 'OctetStringType', 'BitStringType') and type_or_value == 'value':
            template = self.env.get_template('simple_value.txt')
        else:
            template = self.env.get_template('{}.txt'.format(asn_type))
        return template.render(**kwargs)


template_filler = TemplateFiller()
