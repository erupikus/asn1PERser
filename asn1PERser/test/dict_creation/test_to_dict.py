import pytest
from pyasn1.type.namedtype import NamedType
from asn1PERser.classes.data.builtin import IntegerType, OctetStringType, BitStringType, BooleanType, \
    SequenceOfType, SequenceType, EnumeratedType, ChoiceType
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.test.parsing.asn1_python_code.Choice_Simple import Order, MyInteger, MyBoolean, MyBitString, \
    MyOctetString
from asn1PERser.test.parsing.asn1_python_code.SimpleTypes import MyEnumerated
from asn1PERser.test.parsing.asn1_python_code.SimpleProtocol import SimpleMessage, Port, UTC_Timestamp, \
    SequenceNumber, Start, Data, Payload, Message


@pytest.mark.parametrize("schema, value", [
    (IntegerType(10), {'IntegerType': 10}),
    (OctetStringType(binValue='101001011100'), {'OctetStringType': 'a5c0'}),
    (OctetStringType(hexValue='DEADBEEF'), {'OctetStringType': 'deadbeef'}),
    (BitStringType(binValue='101001011100'), {'BitStringType': 2652}),
    (BitStringType(hexValue='a5c0'), {'BitStringType': 42432}),
    (BooleanType(True), {'BooleanType': True}),
    (BooleanType(False), {'BooleanType': False}),
])
def test_create_simple_types_dict(schema, value):
    assert schema.toDict() == value


@pytest.mark.parametrize("schema, key_name, value", [
    (IntegerType(-987654), 'myInt', {'myInt': -987654}),
    (OctetStringType(binValue='101001011100'), 'myOctetString_1', {'myOctetString_1': 'a5c0'}),
    (OctetStringType(hexValue='DEADBEEF'), 'myOctetString_2', {'myOctetString_2': 'deadbeef'}),
    (BitStringType(binValue='101001011100'), 'MY_BIT_STRING_1', {'MY_BIT_STRING_1': 2652}),
    (BitStringType(hexValue='a5c0'), 'MY_BIT_STRING_1', {'MY_BIT_STRING_1': 42432}),
    (BooleanType(True), 'fuNNY_bool_one', {'fuNNY_bool_one': True}),
    (BooleanType(False), 'sad_bool', {'sad_bool': False}),
])
def test_create_simple_types_with_custom_key_names_dict(schema, key_name,  value):
    assert schema.toDict(key_name) == value


def create_choice(selection, initialized_type):
    order = Order()
    order[selection] = initialized_type
    return order


@pytest.mark.parametrize("schema, key_name, value", [
    (create_choice('one', IntegerType(12345)), '', {'Order': {'one': 12345}}),
    (create_choice('two', MyInteger(0)), '', {'Order': {'two': 0}}),
    (create_choice('three', OctetStringType(hexValue='feed')), '', {'Order': {'three': 'feed'}}),
    (create_choice('four', MyOctetString(hexValue='deefabcd')), 'customOrder', {'customOrder': {'four': 'deefabcd'}}),
    (create_choice('five', BitStringType(binValue='111100001111')), 'other_order', {'other_order': {'five': 3855}}),
    (create_choice('six', MyBitString(hexValue='babe')), '', {'Order': {'six': 47806}}),
    (create_choice('seven', BooleanType(True)), 'boolOrder', {'boolOrder': {'seven': True}}),
    (create_choice('eight', MyBoolean(False)), '', {'Order': {'eight': False}}),
])
def test_create_choice_dict(schema, key_name, value):
    assert schema.toDict(key_name) == value


@pytest.mark.parametrize("schema, key_name, value", [
    (MyEnumerated('one'), '', {'MyEnumerated': 'one'}),
    (MyEnumerated('two'), 'myEnum', {'myEnum': 'two'}),
    (MyEnumerated('three'), '', {'MyEnumerated': 'three'}),
])
def test_create_enumerated_dict(schema, key_name, value):
    assert schema.toDict(key_name) == value


def create_simple_sequence():
    class MySimpleSeq(SequenceType):
        rootComponent = AdditiveNamedTypes(
            NamedType('one', IntegerType()),
            NamedType('two', BooleanType()),
            NamedType('three', MyEnumerated()),
            NamedType('four', BitStringType()),
            NamedType('five', OctetStringType()),
        )
        componentType = rootComponent

    mySeq = MySimpleSeq()
    mySeq['one'] = IntegerType(-1)
    mySeq['two'] = BooleanType(True)
    mySeq['three'] = MyEnumerated('one')
    mySeq['four'] = BitStringType(binValue='0111')
    mySeq['five'] = OctetStringType(hexValue='bada')

    return mySeq


def test_create_simple_sequence_dict():
    assert create_simple_sequence().toDict() == {'MySimpleSeq': {'one': -1,
                                                                 'two': True,
                                                                 'three': 'one',
                                                                 'four': 7,
                                                                 'five': 'bada'}}


def create_simple_sequence_of(seq_of_type, values, input_type=None):
    class MySeqOf(SequenceOfType):
        componentType = seq_of_type()

    my_seq_of = MySeqOf()
    for value in values:
        if not input_type:
            my_seq_of.extend([seq_of_type(value)])
        elif input_type == 'hexValue':
            my_seq_of.extend([seq_of_type(hexValue=value)])
        elif input_type == 'binValue':
            my_seq_of.extend([seq_of_type(binValue=value)])

    return my_seq_of


@pytest.mark.parametrize("schema, key_name, value", [
    (create_simple_sequence_of(IntegerType, [1, 22, 333, 4444]), 'my_seq_of', {'my_seq_of': [1, 22, 333, 4444]}),
    (create_simple_sequence_of(BitStringType, ['0011', '10', '10001000'], 'binValue'), '', {'MySeqOf': [3, 2, 136]}),
    (create_simple_sequence_of(OctetStringType, ['dead', 'beef'], 'hexValue'), '', {'MySeqOf': ['dead', 'beef']}),
])
def test_create_simple_sequence_of_dict(schema, key_name, value):
    assert schema.toDict(key_name) == value


def test_simple_protocol_start_dict():
    src_port = Port(10000)
    dst_port = Port(20000)

    timestamp = UTC_Timestamp()
    timestamp['seconds'] = UTC_Timestamp.seconds(1234567)
    timestamp['useconds'] = UTC_Timestamp.useconds(7654321)

    sequence_num = SequenceNumber(1)

    start_message = Start()
    start_message['sequenceNumber'] = sequence_num
    start_message['timestamp'] = timestamp
    start_message['srcPort'] = src_port
    start_message['dstPort'] = dst_port

    simple_message = SimpleMessage()
    simple_message['start'] = start_message

    simple_message_dict = {'SimpleMessage': {'start': {'sequenceNumber': 1,
                                                       'timestamp': {'seconds': 1234567,
                                                                     'useconds': 7654321},
                                                       'srcPort': 10000,
                                                       'dstPort': 20000}}}

    assert simple_message.toDict() == simple_message_dict


def test_simple_protocol_data_dict():
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

    simple_message_dict = {'SimpleMessage': {'data': {'sequenceNumber': 55555,
                                                      'swRelease': 'rel2',
                                                      'macroId': 986895,
                                                      'payload': ['dead', 'beef', 'feed', 'aa', 'bbbbbbbb']}}}

    assert simple_message.toDict() == simple_message_dict


def test_more_complicated_sequence():
    class FirstInnerSeq(SequenceType):
        rootComponent = AdditiveNamedTypes(
            NamedType('aa', IntegerType()),
            NamedType('bb', IntegerType()),
        )
        componentType = rootComponent

    class SecondInnerSeq(SequenceType):
        rootComponent = AdditiveNamedTypes(
            NamedType('cc', IntegerType()),
            NamedType('dd', IntegerType()),
        )
        componentType = rootComponent

    class FirstSeqOf(SequenceOfType):
        componentType = FirstInnerSeq()

    class SecondSeqOf(SequenceOfType):
        componentType = SecondInnerSeq()

    class TopSequence(SequenceType):
        rootComponent = AdditiveNamedTypes(
            NamedType('one', FirstSeqOf()),
            NamedType('two', SecondSeqOf()),
        )
        componentType = rootComponent

    first_inner_seq_1 = FirstInnerSeq()
    first_inner_seq_1['aa'] = IntegerType(1)
    first_inner_seq_1['bb'] = IntegerType(2)

    first_inner_seq_2 = FirstInnerSeq()
    first_inner_seq_2['aa'] = IntegerType(3)
    first_inner_seq_2['bb'] = IntegerType(4)

    second_inner_seq_1 = SecondInnerSeq()
    second_inner_seq_1['cc'] = IntegerType(5)
    second_inner_seq_1['dd'] = IntegerType(6)

    second_inner_seq_2 = SecondInnerSeq()
    second_inner_seq_2['cc'] = IntegerType(7)
    second_inner_seq_2['dd'] = IntegerType(8)

    second_inner_seq_3 = SecondInnerSeq()
    second_inner_seq_3['cc'] = IntegerType(9)
    second_inner_seq_3['dd'] = IntegerType(10)

    first_seq_of = FirstSeqOf()
    first_seq_of.extend([first_inner_seq_1, first_inner_seq_2])

    second_seq_of = SecondSeqOf()
    second_seq_of.extend([second_inner_seq_1, second_inner_seq_2, second_inner_seq_3])

    top_seq = TopSequence()
    top_seq['one'] = first_seq_of
    top_seq['two'] = second_seq_of

    top_seq_dict = {'TopSequence': {'one': [{'aa': 1, 'bb': 2},
                                            {'aa': 3, 'bb': 4}],
                                    'two': [{'cc': 5, 'dd': 6},
                                            {'cc': 7, 'dd': 8},
                                            {'cc': 9, 'dd': 10}]}}

    assert top_seq.toDict() == top_seq_dict
