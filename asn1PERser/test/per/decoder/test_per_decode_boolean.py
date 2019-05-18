import pytest
from asn1PERser.codec.per.decoder import decode as per_decoder
from asn1PERser.classes.data.builtin.BooleanType import BooleanType


@pytest.mark.parametrize("schema, encoded, value", [
    (BooleanType, '80', BooleanType(value=True)),
    (BooleanType, '00', BooleanType(value=False)),
])
def test_boolean_type_can_be_decoded(schema, encoded, value):
    assert per_decoder(per_stream=bytes.fromhex(encoded), asn1Spec=schema()) == value
