from asn1PERser.codec.per.decoder import decode
from asn1PERser.test.parsing.asn1_python_code.SimpleProtocol import SimpleMessage
from asn1PERser.test.per.encoder.test_per_encode_SimpleProtocol import DATA_alive_message, DATA_start_message, \
    DATA_data_message_1, DATA_data_message_2


def test_alive_message_can_be_decoded():
    assert decode(per_stream=bytes.fromhex('4C5CD5FE55403039'), asn1Spec=SimpleMessage()) == DATA_alive_message()


def test_start_message_can_be_decoded():
    assert decode(per_stream=bytes.fromhex('00000AC05CD5FE55403039D8ED0000'), asn1Spec=SimpleMessage()) == DATA_start_message()


def test_data_message_1_can_be_decoded():
    assert decode(per_stream=bytes.fromhex('70D90320F0F0F880DEAD40BEEF40FEED00AAC0BBBBBBBB'), asn1Spec=SimpleMessage()) == DATA_data_message_1()


def test_data_message_2_can_be_decoded():
    assert decode(per_stream=bytes.fromhex('60010043DEADBEEF'), asn1Spec=SimpleMessage()) == DATA_data_message_2()
