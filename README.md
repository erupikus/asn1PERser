# asn1PERser
This library can parse ASN.1 text schemas into Python code. ASN.1 PER (Aligned) decoder/encoder is included to use with parsed schemas.

Supported ASN.1 types and their constraints are:

| ASN.1 Type   | Single value | Value range | Value size | can be extended (...) | used Python contraint class |
|:------------:|:------------:|:-----------:|:----------:|:---------------------:|:---------------------------:|
| INTEGER      |      X       |     X       |            |       X               |       ValueRange            |
| BOOLEAN      |              |             |            |                       |                             |
| ENUMERATED   |              |             |            |       X               |       ExtensionMarker       |
| BIT STRING   |      X       |             |     X      |       X               |       ValueSize             |
| OCTET STRING |      X       |             |     X      |       X               |       ValueSize             |
| CHOICE       |              |             |            |       X               |       ExtensionMarker       |
| SEQUENCE     |              |             |            |       X               |       ExtensionMarker       |
| SEQUENCE OF  |      X       |             |     X      |       X               |       SequenceOfValueSize   |

Table of contents:
1. [Examples](#examples)
2. [Decoding from string](#decoding-from-string)
3. [Dictionary creation](#dictionary-creation)
4. [Additional info](#additional-info)
5. [History](#history)
6. [Known bugs](#known-bugs)

## Examples
Following ASN.1 schema:

```python
asn_schema = '''\
SimpleProtocol DEFINITIONS AUTOMATIC TAGS ::=
BEGIN
SimpleMessage ::= CHOICE {
    start    Start,
    stop     Stop,
    alive    Alive,
    data     Data,
    ...
}

Start ::= SEQUENCE {
    sequenceNumber    SequenceNumber,
    timestamp         UTC-Timestamp,
    srcPort           Port,
    dstPort           Port
}

Stop ::= SEQUENCE {
    sequenceNumber    SequenceNumber,
    timestamp         UTC-Timestamp,
    srcPort           Port,
    dstPort           Port
}

Alive ::= SEQUENCE {
    timestamp         UTC-Timestamp,
    ...
}

Data ::= SEQUENCE {
    sequenceNumber    SequenceNumber,
    swRelease         ENUMERATED {rel1, rel2, rel3, ...},
    macroId           BIT STRING (SIZE(20)) OPTIONAL,
    payload           Payload
}

Port ::= INTEGER (10000..65535)

SequenceNumber ::= INTEGER (0..65535)

UTC-Timestamp ::= SEQUENCE {
    seconds     INTEGER (0..4294967295),
    useconds    INTEGER (0..4294967295)
}

Payload ::= SEQUENCE (SIZE(1..5)) OF Message

Message ::= OCTET STRING (SIZE(1..4))

END
'''
```

can be parsed into Python code like this:
```python
from asn1PERser import parse_asn1_schema


parse_asn1_schema(asn1_schema=asn_schema, output_folder=r'C:/my_code/')
```

Above code will create file 'SimpleProtocol.py' in folder (which must exist) 'C:/my_code/':
```python
from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType, DefaultedNamedType
from pyasn1.type.namedval import NamedValues
from asn1PERser.classes.data.builtin import *
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import MIN, MAX, NoConstraint, ExtensionMarker, SequenceOfValueSize, \
    ValueRange, SingleValue, ValueSize, ConstraintOr, ConstraintAnd


class Port(IntegerType):
    subtypeSpec = ValueRange(10000, 65535)


class SequenceNumber(IntegerType):
    subtypeSpec = ValueRange(0, 65535)


class Message(OctetStringType):
    subtypeSpec = ValueSize(1, 4)


class UTC_Timestamp(SequenceType):
    class seconds(IntegerType):
        subtypeSpec = ValueRange(0, 4294967295)

    class useconds(IntegerType):
        subtypeSpec = ValueRange(0, 4294967295)

    rootComponent = AdditiveNamedTypes(
        NamedType('seconds', seconds()),
        NamedType('useconds', useconds()),
    )
    componentType = rootComponent


class Start(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('sequenceNumber', SequenceNumber()),
        NamedType('timestamp', UTC_Timestamp()),
        NamedType('srcPort', Port()),
        NamedType('dstPort', Port()),
    )
    componentType = rootComponent


class Stop(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('sequenceNumber', SequenceNumber()),
        NamedType('timestamp', UTC_Timestamp()),
        NamedType('srcPort', Port()),
        NamedType('dstPort', Port()),
    )
    componentType = rootComponent


class Alive(SequenceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('timestamp', UTC_Timestamp()),
    )
    componentType = rootComponent


class Payload(SequenceOfType):
    subtypeSpec = SequenceOfValueSize(1, 5)
    componentType = Message()


class Data(SequenceType):
    class swRelease(EnumeratedType):
        subtypeSpec = ExtensionMarker(True)
        enumerationRoot = NamedValues(
            ('rel1', 0),
            ('rel2', 1),
            ('rel3', 2),
        )
        namedValues = enumerationRoot

    class macroId(BitStringType):
        subtypeSpec = ValueSize(20, 20)

    rootComponent = AdditiveNamedTypes(
        NamedType('sequenceNumber', SequenceNumber()),
        NamedType('swRelease', swRelease()),
        OptionalNamedType('macroId', macroId()),
        NamedType('payload', Payload()),
    )
    componentType = rootComponent


class SimpleMessage(ChoiceType):
    subtypeSpec = ExtensionMarker(True)
    rootComponent = AdditiveNamedTypes(
        NamedType('start', Start()),
        NamedType('stop', Stop()),
        NamedType('alive', Alive()),
        NamedType('data', Data()),
    )
    componentType = rootComponent



```

When schema is parsed it can be used - message can be created, encoded and decoded, using PER encoder/decoder, into bytes
or Python structure:
```python
from asn1PERser import encode, decode
from SimpleProtocol import *


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

per_bytes = encode(asn1Spec=simple_message)
print('encoded alive bytes as hex string:')
print(per_bytes.hex())
print('\n')

decoded = decode(per_stream=per_bytes, asn1Spec=SimpleMessage())
print('decoded alive message structure as string...:')
print(decoded)

print('...can be accessed like dictionary:')
print(decoded['alive']['timestamp']['seconds'])
```

above will output:
```
encoded alive bytes as hex string:
4c5cd5fe55403039


decoded alive message structure as string...:
SimpleMessage:
 alive=Alive:
  timestamp=UTC_Timestamp:
   seconds=1557528149
   useconds=12345



...can be accessed like dictionary:
1557528149


...can be transformed into dictionary:
{'alive': OrderedDict([('timestamp', OrderedDict([('seconds', 1557528149), ('useconds', 12345)]))])}
```

Next message:
```python
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

per_bytes = encode(asn1Spec=simple_message)
print('encoded start bytes as hex string:')
print(per_bytes.hex())
print('\n')

decoded = decode(per_stream=per_bytes, asn1Spec=SimpleMessage())
print('start message structure as string...:')
print(decoded)
print('...can be accessed like dictionary:')
print(decoded['start']['srcPort'])
```

above will output:
```
encoded start bytes as hex string:
00000ac05cd5fe55403039d8ed0000


start message structure as string...:
SimpleMessage:
 start=Start:
  sequenceNumber=10
  timestamp=UTC_Timestamp:
   seconds=1557528149
   useconds=12345

  srcPort=65533
  dstPort=10000


...can be accessed like dictionary:
65533


...can be transformed into dictionary:
{'start': OrderedDict([('sequenceNumber', 10), ('timestamp', OrderedDict([('seconds', 1557528149), ('useconds', 12345)])), ('srcPort', 65533), ('dstPort', 10000)])}
```

Next message:
```python
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

per_bytes = encode(asn1Spec=simple_message)
print('encoded data bytes as hex string:')
print(per_bytes.hex())
print('\n')

decoded = decode(per_stream=per_bytes, asn1Spec=SimpleMessage())
print('data message structure as string...:')
print(decoded)
print('...can be accessed like dictionary:')
print(bytes(decoded['data']['payload'][0]).hex())
```

above will output:
```
encoded data bytes as hex string:
70d90320f0f0f880dead40beef40feed00aac0bbbbbbbb


data message structure as string...:
SimpleMessage:
 data=Data:
  sequenceNumber=55555
  swRelease=rel2
  macroId=986895
  payload=Payload:
   0xdead   0xbeef   0xfeed   0xaa   0xbbbbbbbb


...can be accessed like dictionary:
dead


...can be transformed into dictionary:
{'data': OrderedDict([('sequenceNumber', 55555), ('swRelease', 'rel2'), ('macroId', 986895), ('payload', ['dead', 'beef', 'feed', 'aa', 'bbbbbbbb'])])}
```

Next message:
```python
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

per_bytes = encode(asn1Spec=simple_message)
print('encoded data bytes as hex string:')
print(per_bytes.hex())
print('\n')

decoded = decode(per_stream=per_bytes, asn1Spec=SimpleMessage())
print('data message structure as string...:')
print(decoded)
print('...can be accessed like dictionary:')
print(decoded['data']['swRelease'])
```

above will output:
```
encoded data bytes as hex string:
60010043deadbeef


data message structure as string...:
SimpleMessage:
 data=Data:
  sequenceNumber=256
  swRelease=rel3
  payload=Payload:
   0xdeadbeef


...can be accessed like dictionary:
rel3


...can be transformed into dictionary:
{'data': OrderedDict([('sequenceNumber', 256), ('swRelease', 'rel3'), ('payload', ['deadbeef'])])}
```

## Decoding from string
When encoded bytes are given as __string__ use _bytearray.fromhex()_:

```

pure_string = str('70d90320f0f0f880dead40beef40feed00aac0bbbbbbbb')
real_bytes = bytearray.fromhex(pure_string)

decoded = decode(asn1Spec=SimpleMessage(), per_stream=real_bytes)
print(decoded)
```

above will output:
```
SimpleMessage:
 data=Data:
  sequenceNumber=55555
  swRelease=rel2
  macroId=986895
  payload=Payload:
   0xdead   0xbeef   0xfeed   0xaa   0xbbbbbbbb
```

## Dictionary creation
  Data above can be accessed like dictionary but it is not a dictionary.
  Method '__to_dict__' was added to make dictionary creation simple:

```
msg_dict = decoded.to_dict()
print(type(msg_dict))
print(msg_dict)
```

output:
```
<class 'dict'>
{'data': OrderedDict([('sequenceNumber', 55555), ('swRelease', 'rel2'), ('macroId', 986895), ('payload', ['dead', 'beef', 'feed', 'aa', 'bbbbbbbb'])])}
```

To better show created structure, json.dumps() can be used:
```
print(json.dumps(msg_dict, indent=2))
```

output:
```
{
  "data": {
    "sequenceNumber": 55555,
    "swRelease": "rel2",
    "macroId": 986895,
    "payload": [
      "dead",
      "beef",
      "feed",
      "aa",
      "bbbbbbbb"
    ]
  }
}
```

## Additional info

For more examples please see library tests:
- parsing tests, located in test/parsing/ folder.
- coding/encoding tests, located in test/per folder.

All above examples and tests where checked using:
https://asn1.io/asn1playground/

This library inherits extensively from pyasn1 library so BER and other encoding should also work here.

Parsing may take time - when trying to parse about 2000 lines of ASN.1 it took 15-20 minutes.
Tests for parsing also take time.

## History

See CHANGES file.

## Known bugs
- Defining BitStringType type with default hexValue set to empty string (''), like:
```
...
d15     BIT STRING DEFAULT ''H,
...
```
will parse to Python code but running it will cause exception:
```
pyasn1.error.PyAsn1Error: BitStringType.fromHexString() error: invalid literal for int() with base 16: ''
```

- This will parse, but sorting algorith may not sort it corretly:
```
    
    MySeq2 ::= MySeq1   -- ok since one level of nesting is ok

    MySeq3 ::= MySeq1   -- ok since one level of nesting is ok
    
    MySeq1 ::= SEQUENCE {
        d00     INTEGER
    }

    MySeq4 ::= MySeq2   -- NOT OK! 2nd level of nesting 
```
This will parse into:
```python
MySeq4 = MySeq2


class MySeq1(SequenceType):
    rootComponent = AdditiveNamedTypes(
        NamedType('d00', IntegerType()),
    )
    componentType = rootComponent


MySeq3 = MySeq1


MySeq2 = MySeq1
```
so Python will not find MySeq2 - this will lead to NameError.
