import pytest
from asn1PERser.codec.per.decoder import decode as per_decoder
from asn1PERser.test.per.encoder.test_per_encode_mixed_schemas import DATA_first_sequence, MySeq, \
    DATA_seq__of__seq_of__of__seq_in_ext_add, DATA_seq__of__seq_of__of__seq_in_ext_add_group, \
    DATA_seq__of__seq_of__of__seq_in_root, OuterSeq, OuterSeq1, OuterSeq2


def test_first_sequence_can_be_decoded():
    assert per_decoder(per_stream=bytearray.fromhex('8004F401640202DEAD02BEEF'), asn1Spec=MySeq()) == DATA_first_sequence()


def test_seq_of_seq_of_of_seq_in_root_can_be_decoded():
    assert per_decoder(per_stream=bytearray.fromhex('80010A0114'), asn1Spec=OuterSeq()) == DATA_seq__of__seq_of__of__seq_in_root(my_sof1_is=True, my_sof2_is=False)
    assert per_decoder(per_stream=bytearray.fromhex('C0010A011400011E0128'), asn1Spec=OuterSeq()) == DATA_seq__of__seq_of__of__seq_in_root(my_sof1_is=True, my_sof2_is=True)
    assert per_decoder(per_stream=bytearray.fromhex('40011E0128'), asn1Spec=OuterSeq()) == DATA_seq__of__seq_of__of__seq_in_root(my_sof1_is=False, my_sof2_is=True)


def test_seq_of_seq_of_of_seq_in_extension_addition_can_be_decoded():
    assert per_decoder(per_stream=bytearray.fromhex('8001F603000500010A0114'), asn1Spec=OuterSeq1()) == DATA_seq__of__seq_of__of__seq_in_ext_add(my_sof1_is=True, my_sof2_is=False)
    assert per_decoder(per_stream=bytearray.fromhex('8001F603800500010A01140500011E0128'), asn1Spec=OuterSeq1()) == DATA_seq__of__seq_of__of__seq_in_ext_add(my_sof1_is=True, my_sof2_is=True)
    assert per_decoder(per_stream=bytearray.fromhex('8001F602800500011E0128'), asn1Spec=OuterSeq1()) == DATA_seq__of__seq_of__of__seq_in_ext_add(my_sof1_is=False, my_sof2_is=True)
    assert per_decoder(per_stream=bytearray.fromhex('0001F6'), asn1Spec=OuterSeq1()) == DATA_seq__of__seq_of__of__seq_in_ext_add(my_sof1_is=False, my_sof2_is=False)


def test_seq_of_seq_of_of_seq_in_extension_addition_group_can_be_encoded():
    assert per_decoder(per_stream=bytearray.fromhex('8001F6010580010A0114'), asn1Spec=OuterSeq2()) == DATA_seq__of__seq_of__of__seq_in_ext_add_group(my_sof1_is=True, my_sof2_is=False)
    assert per_decoder(per_stream=bytearray.fromhex('8001F6010AC0010A011400011E0128'), asn1Spec=OuterSeq2()) == DATA_seq__of__seq_of__of__seq_in_ext_add_group(my_sof1_is=True, my_sof2_is=True)
    assert per_decoder(per_stream=bytearray.fromhex('8001F6010540011E0128'), asn1Spec=OuterSeq2()) == DATA_seq__of__seq_of__of__seq_in_ext_add_group(my_sof1_is=False, my_sof2_is=True)
    assert per_decoder(per_stream=bytearray.fromhex('0001F6'), asn1Spec=OuterSeq2()) == DATA_seq__of__seq_of__of__seq_in_ext_add_group(my_sof1_is=False, my_sof2_is=False)