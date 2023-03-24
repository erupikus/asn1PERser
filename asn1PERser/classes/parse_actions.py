from copy import deepcopy
from collections import namedtuple
from asn1PERser.classes.types.builtin import SequenceType, DefinedType, \
    VisibleString, NumericString, IntegerType, DateType, RealType, BooleanType, \
    ChoiceType, EnumeratedType, IA5String, UTF8String, OctetStringType, \
    BitStringType, SequenceOfType, builtin_types
from asn1PERser.classes.module import ModuleDefinition, typereference_to_type
from asn1PERser.asn_definitions.constraint_def import Constraint


constraint_tuple = namedtuple('constraint', 'lowerEndpoint upperEndpoint extensionMarker')


def parse_ModuleDefinition(toks):
    module = ModuleDefinition()
    module.ModuleIdentifier = toks['ModuleIdentifier'][0]
    module.EncodingReferenceDefault = toks['EncodingReferenceDefault'] if 'EncodingReferenceDefault' in toks.keys() else ''
    module.TagDefault = toks['TagDefault'] if 'TagDefault' in toks.keys() else ''
    module.ExtensionDefault = toks['ExtensionDefault'] if 'ExtensionDefault' in toks.keys() else ''
    module.ModuleBody = toks['ModuleBody'] if 'ModuleBody' in toks.keys() else ''
    return module


def parse_ValueAssignment(toks):
    item_valuereference = toks[0]
    item_type = toks[1][0]
    item_value = toks[-1]
    item_type.valuereference = item_valuereference
    item_type.Value = item_value
    return item_type


def parse_TypeAssignment(toks):
    item_typereference = toks[0]
    item_type = toks[2][0]

    if item_type.typereference in builtin_types:
        item_type.typereference = item_typereference
    else:
        item_type.identifier = item_typereference
    typereference_to_type[item_typereference] = deepcopy(item_type)
    return item_type


def parse_BitStringType(toks):
    return BitStringType()


def parse_OctetStringType(toks):
    return OctetStringType()


def parse_SequenceType(toks):
    sequence_type = SequenceType()
    for Type in toks[1:]:
        sequence_type.ComponentTypeList = Type
    return sequence_type


def parse_SequenceOfType(toks):
    sequence_of_type = SequenceOfType()
    component_type = toks[1][0]
    sequence_of_type.ComponentType = component_type
    return sequence_of_type


def parse_ChoiceType(toks):
    choice_type = ChoiceType()
    for Type in toks[1:]:
        choice_type.AlternativeTypeList = Type
    return choice_type


def parse_DefinedType(toks):
    return DefinedType(toks[0])


def parse_IA5String(toks):
    return IA5String()


def parse_UTF8String(toks):
    return UTF8String()


def parse_VisibleString(toks):
    return VisibleString()


def parse_NumericString(toks):
    return NumericString()


def parse_IntegerType(toks):
    return IntegerType()


def parse_RealType(toks):
    return RealType()


def parse_BooleanType(toks):
    return BooleanType()


def parse_ComponentType(toks):
    identifier = toks[0]
    Type = toks[1][0]
    Type.identifier = identifier
    try:
        if toks[2] == 'OPTIONAL':
            Type.optional = True
        if toks[2] == 'DEFAULT':
            Type.default = toks[3]
    except IndexError:
        pass
    return Type


def parse_NamedType(toks):
    pass


def parse_ConstrainedType(toks):
    Type = toks[0]
    constraint = toks[1]
    Type.constraint = constraint
    return Type


def parse_TypeWithConstraint(toks):
    constrain = toks[1]
    if toks[0] == "SEQUENCE":
        componentType = toks[3]
        Type = parse_SequenceOfType(["SEQUENCE OF", componentType])
    if toks[0] == "SET":
        raise NotImplemented
    return [Type, constrain]


def parse_DateType(toks):
    return DateType()


def parse_AlternativeTypeList(toks):
    alternate_type_list = []
    for identifier, Type in zip(toks[0::2], toks[1::2]):
        Type = Type[0]
        Type.identifier = identifier
        alternate_type_list.append(Type)
    return alternate_type_list


def parse_ExtensionAdditionAlternativesList(toks):
    toks = list(toks)
    alternate_type_list = []
    is_extension_addition_group = False
    if '[[' in toks:
        is_extension_addition_group = True
        toks.remove('[[')
        toks.remove(']]')
    for identifier, Type in zip(toks[0::2], toks[1::2]):
        Type = Type[0]
        Type.identifier = identifier
        alternate_type_list.append(Type)
    if is_extension_addition_group:
        alternate_type_list.insert(0, '[[')
        alternate_type_list.append(']]')
    return alternate_type_list


def parse_EnumeratedType(toks):
    enumerated_type = EnumeratedType()
    for EnumerationItem in toks[1:]:
        enumerated_type.EnumerationItems = EnumerationItem
    return enumerated_type


def parse_Constraint(toks):
    constraint = toks[0]
    if constraint[0] == 'SIZE':
        return constraint[1]
    constraint = '(' + ' '.join(constraint) + ')'
    parsed = list(Constraint.parseString(constraint))
    ext_mark = False
    if '...' in parsed:
        parsed.remove('...')
        ext_mark = True
    return constraint_tuple(lowerEndpoint=parsed[0], upperEndpoint=parsed[-1], extensionMarker=ext_mark)
