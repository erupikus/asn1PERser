from asn1PERser.classes.parse_actions import parse_TypeAssignment, parse_ValueAssignment
from .lexical_items import valuereference, typereference, assignment
from .type_def import Type
from .value_def import Value


# 16.2
ValueAssignment = (valuereference + Type + assignment + Value).setParseAction(parse_ValueAssignment)


# 16.1
TypeAssignment = (typereference + assignment + Type).setParseAction(parse_TypeAssignment)
