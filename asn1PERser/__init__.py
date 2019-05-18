from asn1PERser.codec.per.decoder import decode
from asn1PERser.codec.per.encoder import encode
from asn1PERser.classes.module import remove_comments
from asn1PERser.asn_definitions.module_def import ModuleDefinition


__all__ = ['decode', 'encode', 'parse_asn1_schema']


def parse_asn1_schema(asn1_schema, output_folder=None):
    no_comment_schema = remove_comments(asn1_schema)
    parsed_asn = ModuleDefinition.parseString(no_comment_schema)[0]
    return parsed_asn.create_python_template(path=output_folder)
