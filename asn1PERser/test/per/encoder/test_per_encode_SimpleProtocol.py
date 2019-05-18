from asn1PERser.test.parsing.asn1_python_code.SimpleProtocol import *
from asn1PERser.codec.per.encoder import encode


def DATA_alive_message():
    '''
    simple_message SimpleMessage ::= alive : {
        timestamp {
            seconds 1557528149,
            useconds 12345
        }
    }
    '''
    utc_timestamp = UTC_Timestamp()
    utc_timestamp['seconds'] = UTC_Timestamp.seconds(1557528149)
    utc_timestamp['useconds'] = UTC_Timestamp.useconds(12345)

    msg_alive = Alive()
    msg_alive['timestamp'] = utc_timestamp

    simple_message = SimpleMessage()
    simple_message['alive'] = msg_alive

    return simple_message


def DATA_start_message():
    '''
    simple_message SimpleMessage ::= start : {
        sequenceNumber    10,
        timestamp {
            seconds 1557528149,
            useconds 12345
        },
        srcPort    65533,
        dstPort    10000
    }
    '''
    utc_timestamp = UTC_Timestamp()
    utc_timestamp['seconds'] = UTC_Timestamp.seconds(1557528149)
    utc_timestamp['useconds'] = UTC_Timestamp.useconds(12345)

    msg_start = Start()
    msg_start['sequenceNumber'] = SequenceNumber(10)
    msg_start['timestamp'] = utc_timestamp
    msg_start['srcPort'] = Port(65533)
    msg_start['dstPort'] = Port(10000)

    simple_message = SimpleMessage()
    simple_message['start'] = msg_start

    return simple_message


def DATA_data_message_1():
    '''
    simple_message SimpleMessage ::= data : {
        sequenceNumber    55555,
        swRelease  rel2,
        macroId    '11110000111100001111'B,
        payload {
            'DEAD'H,
            'BEEF'H,
            'FEED'H,
            'AA'H,
            'BBBBBBBB'H
        }
    }
    '''
    data_payload = Payload()
    data_payload.extend([Message(hexValue='DEAD')])
    data_payload.extend([Message(hexValue='BEEF')])
    data_payload.extend([Message(hexValue='FEED')])
    data_payload.extend([Message(hexValue='AA')])
    data_payload.extend([Message(hexValue='BBBBBBBB')])

    msg_data = Data()
    msg_data['sequenceNumber'] = SequenceNumber(55555)
    msg_data['swRelease'] = Data.swRelease('rel2')
    msg_data['macroId'] = Data.macroId(binValue='11110000111100001111')
    msg_data['payload'] = data_payload

    simple_message = SimpleMessage()
    simple_message['data'] = msg_data

    return simple_message


def DATA_data_message_2():
    '''
    simple_message SimpleMessage ::= data : {
        sequenceNumber    256,
        swRelease  rel3,
        payload {
            'DEADBEEF'H
        }
    }
    '''
    data_payload = Payload()
    data_payload.extend([Message(hexValue='DEADBEEF')])

    msg_data = Data()
    msg_data['sequenceNumber'] = SequenceNumber(256)
    msg_data['swRelease'] = Data.swRelease('rel3')
    msg_data['payload'] = data_payload

    simple_message = SimpleMessage()
    simple_message['data'] = msg_data

    return simple_message


def test_alive_message_can_be_encoded():
    per_encoded = encode(asn1Spec=DATA_alive_message())
    assert per_encoded == bytes.fromhex('4C5CD5FE55403039')


def test_start_message_can_be_encoded():
    per_encoded = encode(asn1Spec=DATA_start_message())
    assert per_encoded == bytes.fromhex('00000AC05CD5FE55403039D8ED0000')


def test_data_message_1_can_be_encoded():
    per_encoded = encode(asn1Spec=DATA_data_message_1())
    assert per_encoded == bytes.fromhex('70D90320F0F0F880DEAD40BEEF40FEED00AAC0BBBBBBBB')


def test_data_message_2_can_be_encoded():
    per_encoded = encode(asn1Spec=DATA_data_message_2())
    assert per_encoded == bytes.fromhex('60010043DEADBEEF')
