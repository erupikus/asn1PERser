import pytest
from pyasn1.type.namedtype import NamedType, OptionalNamedType
from asn1PERser.classes.data.builtin import IntegerType, OctetStringType, BitStringType, BooleanType, \
    SequenceOfType, SequenceType, EnumeratedType, ChoiceType
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.test.parsing.asn1_python_code.Choice_Simple import Order, MyInteger, MyBoolean, MyBitString, \
    MyOctetString
from asn1PERser.test.parsing.asn1_python_code.SimpleTypes import MyEnumerated
from asn1PERser.test.parsing.asn1_python_code.SimpleProtocol import SimpleMessage, Port, UTC_Timestamp, \
    SequenceNumber, Start, Data, Payload, Message


@pytest.mark.parametrize("schema, value", [
    (IntegerType(10), 10),
    (OctetStringType(binValue='101001011100'), 'a5c0'),
    (OctetStringType(hexValue='DEADBEEF'), 'deadbeef'),
    (OctetStringType(hexValue='51800d80609bddfd80048054c0609bddfd800481de'), '51800d80609bddfd80048054c0609bddfd800481de'),
    (BitStringType(binValue='101001011100'), 2652),
    (BitStringType(hexValue='a5c0'), 42432),
    (BooleanType(True), True),
    (BooleanType(False), False),
])
def test_create_simple_types_dict(schema, value):
    assert schema.toDict() == value


def create_choice(selection, initialized_type):
    order = Order()
    order[selection] = initialized_type
    return order


@pytest.mark.parametrize("schema, value", [
    (create_choice('one', IntegerType(12345)), {'one': 12345}),
    (create_choice('two', MyInteger(0)), {'two': 0}),
    (create_choice('three', OctetStringType(hexValue='feed')), {'three': 'feed'}),
    (create_choice('four', MyOctetString(hexValue='deefabcd')), {'four': 'deefabcd'}),
    (create_choice('five', BitStringType(binValue='111100001111')), {'five': 3855}),
    (create_choice('six', MyBitString(hexValue='babe')), {'six': 47806}),
    (create_choice('seven', BooleanType(True)), {'seven': True}),
    (create_choice('eight', MyBoolean(False)), {'eight': False}),
])
def test_create_choice_dict(schema, value):
    assert schema.toDict() == value


@pytest.mark.parametrize("schema, value", [
    (MyEnumerated('one'), 'one'),
    (MyEnumerated('two'), 'two'),
    (MyEnumerated('three'), 'three'),
])
def test_create_enumerated_dict(schema, value):
    assert schema.toDict() == value


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
    assert create_simple_sequence().toDict() == {'one': -1,
                                                 'two': True,
                                                 'three': 'one',
                                                 'four': 7,
                                                 'five': 'bada'}


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


@pytest.mark.parametrize("schema, value", [
    (create_simple_sequence_of(IntegerType, [1, 22, 333, 4444]), [1, 22, 333, 4444]),
    (create_simple_sequence_of(BitStringType, ['0011', '10', '10001000'], 'binValue'), [3, 2, 136]),
    (create_simple_sequence_of(OctetStringType, ['dead', 'beef'], 'hexValue'), ['dead', 'beef']),
])
def test_create_simple_sequence_of_dict(schema, value):
    assert schema.toDict() == value


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

    simple_message_dict = {'start': {'sequenceNumber': 1,
                                     'timestamp': {'seconds': 1234567,
                                                   'useconds': 7654321},
                                     'srcPort': 10000,
                                     'dstPort': 20000}}

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

    simple_message_dict = {'data': {'sequenceNumber': 55555,
                                    'swRelease': 'rel2',
                                    'macroId': 986895,
                                    'payload': ['dead', 'beef', 'feed', 'aa', 'bbbbbbbb']}}

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

    top_seq_dict = {'one': [{'aa': 1, 'bb': 2},
                            {'aa': 3, 'bb': 4}],
                    'two': [{'cc': 5, 'dd': 6},
                            {'cc': 7, 'dd': 8},
                            {'cc': 9, 'dd': 10}]}

    assert top_seq.toDict() == top_seq_dict


def test_sequence_with_optional_types_dict():
    class Inner(SequenceType):
        rootComponent = AdditiveNamedTypes(
            OptionalNamedType('a', IntegerType()),
            OptionalNamedType('b', IntegerType()),
        )
        componentType = rootComponent

    class TopSeq(SequenceType):
        rootComponent = AdditiveNamedTypes(
            NamedType('one', IntegerType()),
            OptionalNamedType('two', Inner()),
        )
        componentType = rootComponent

    top = TopSeq()
    top['one'] = IntegerType(0)

    assert top.toDict() == {'one': 0}

    # top = TopSeq()
    # top['one'] = IntegerType(-1)
    #
    # inner = Inner()
    # inner['b'] = IntegerType(10)
    # top['two'] = inner
    #
    # assert top.toDict() == {'TopSeq': {'one': -1,
    #                                    'two': {'b': 10}}}