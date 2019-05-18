import pytest
from asn1PERser.codec.per.encoder import encode as per_encoder
from asn1PERser.classes.data.builtin.BooleanType import BooleanType


@pytest.mark.parametrize("boolean, encoded", [
    (BooleanType(value=True), '80'),
    (BooleanType(value=False), '00')
])
def test_boolean_type_can_be_encoded(boolean, encoded):
    assert per_encoder(boolean) == bytes.fromhex(encoded)
