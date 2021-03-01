import pytest


@pytest.mark.parametrize("asn1_schema, python_code", [
    ('SimpleTypes.asn1', 'SimpleTypes.py'),
    ('Types_constrained.asn1', 'Types_constrained.py'),
    ('Sequence_Simple.asn1', 'Sequence_Simple.py'),
    ('Sequence_Mixed.asn1', 'Sequence_Mixed.py'),
    ('Choice_Simple.asn1', 'Choice_Simple.py'),
    ('ComponentTypes.asn1', 'ComponentTypes.py'),
    ('ComponentTypes_extensionMarker.asn1', 'ComponentTypes_extensionMarker.py'),
    ('ComponentTypes_extensionAddition.asn1', 'ComponentTypes_extensionAddition.py'),
    ('Sequence_Default.asn1', 'Sequence_Default.py'),
    ('Types_containing_constrained_types.asn1', 'Types_containing_constrained_types.py'),
    ('ComponentTypes_containing_ComponentTypes.asn1', 'ComponentTypes_containing_ComponentTypes.py'),
    ('SimpleProtocol.asn1', 'SimpleProtocol.py'),
    ('ComponentTypes_extensionAdditionGroup.asn1', 'ComponentTypes_extensionAdditionGroup.py'),
    ('DefinedType_Simple.asn1', 'DefinedType_Simple.py'),
], indirect=['asn1_schema', 'python_code'])
def test_schema(asn1_schema, python_code, parse_schema):
    parsed_schema = parse_schema(asn1_schema)
    assert parsed_schema == python_code
