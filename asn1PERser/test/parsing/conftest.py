import os
import pytest
from asn1PERser.asn_definitions.module_def import ModuleDefinition


@pytest.fixture(scope='function')
def asn1_schema(request):
    schema_dir = os.path.split(__file__)[0]
    with open(os.path.join(schema_dir, 'asn1_schemas/{name}'.format(name=request.param)), 'r') as schema:
        return schema.read()


@pytest.fixture(scope='function')
def python_code(request):
    parsed_dir = os.path.split(__file__)[0]
    with open(os.path.join(parsed_dir, 'asn1_python_code/{name}'.format(name=request.param)), 'r') as parsed_schema:
        return parsed_schema.read()


@pytest.fixture()
def parse_schema():
    def _parse_schema(schema):
        parsed = ModuleDefinition.parseString(schema)
        parsed_to_python = parsed[0].create_python_template(path=None)
        return parsed_to_python
    return _parse_schema
