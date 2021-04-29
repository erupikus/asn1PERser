import pytest
from pyasn1.type.namedtype import NamedType, NamedTypes, DefaultedNamedType, OptionalNamedType
from asn1PERser.codec.per.encoder import encode as per_encoder
from asn1PERser.classes.data.builtin.ChoiceType import ChoiceType
from asn1PERser.classes.data.builtin.IntegerType import IntegerType
from asn1PERser.classes.types.type import AdditiveNamedTypes
from asn1PERser.classes.types.constraint import ExtensionMarker


def SCHEMA_single_item_choice():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i0  INTEGER
        }
        '''
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
        )
        componentType = rootComponent
    return MyChoice


def SCHEMA_no_extension_simple_choice():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i0  INTEGER,
            i1  INTEGER
        }
        '''
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
            NamedType('i1', IntegerType()),
        )
        componentType = rootComponent
    return MyChoice


def SCHEMA_reverse_no_extension_simple_choice():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i1  INTEGER,
            i0  INTEGER
        }
        '''
        rootComponent = AdditiveNamedTypes(
            NamedType('i1', IntegerType()),
            NamedType('i0', IntegerType()),
        )
        componentType = rootComponent
    return MyChoice


def SCHEMA_single_item_choice_with_extension():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i0  INTEGER,
            ...
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
        )
        componentType = rootComponent
    return MyChoice


def SCHEMA_with_extension_simple_choice():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i0  INTEGER,
            i1  INTEGER,
            ...
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
            NamedType('i1', IntegerType()),
        )
        componentType = rootComponent
    return MyChoice


def SCHEMA_reverse_with_extension_simple_choice():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i1  INTEGER,
            i0  INTEGER,
            ...
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('i1', IntegerType()),
            NamedType('i0', IntegerType()),
        )
        componentType = rootComponent
    return MyChoice


def SCHEMA_selected_choice_from_extension_addition_one_elem():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i0  INTEGER,
            ...
            i2  INTEGER,
            i3  INTEGER
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
        )
        extensionAddition = AdditiveNamedTypes(
            NamedType('i2', IntegerType()),
            NamedType('i3', IntegerType()),
        )
        componentType = rootComponent + extensionAddition
    return MyChoice


def SCHEMA_selected_choice_from_extension_addition_more_elems():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i0    INTEGER,
            i1    INTEGER,
            i2    INTEGER,
            i3    INTEGER,
            i4    INTEGER,
            i5    INTEGER,
            i6    INTEGER,
            i7    INTEGER,
            i8    INTEGER,
            i9    INTEGER,
            i10   INTEGER,
            i11   INTEGER,
            i12   INTEGER,
            i13   INTEGER,
            i14   INTEGER,
            i15   INTEGER,
            i16   INTEGER,
            ...,
            i17   INTEGER,
            i18   INTEGER,
            i19   INTEGER,
            i20   INTEGER,
            i21   INTEGER,
            i22   INTEGER,
            i23   INTEGER,
            i24   INTEGER,
            i25   INTEGER,
            i26   INTEGER,
            i27   INTEGER,
            i28   INTEGER,
            i29   INTEGER,
            i30   INTEGER,
            i31   INTEGER,
            i32   INTEGER,
            i33   INTEGER,
            i34   INTEGER,
            i35   INTEGER
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
            NamedType('i1', IntegerType()),
            NamedType('i2', IntegerType()),
            NamedType('i3', IntegerType()),
            NamedType('i4', IntegerType()),
            NamedType('i5', IntegerType()),
            NamedType('i6', IntegerType()),
            NamedType('i7', IntegerType()),
            NamedType('i8', IntegerType()),
            NamedType('i9', IntegerType()),
            NamedType('i10', IntegerType()),
            NamedType('i11', IntegerType()),
            NamedType('i12', IntegerType()),
            NamedType('i13', IntegerType()),
            NamedType('i14', IntegerType()),
            NamedType('i15', IntegerType()),
            NamedType('i16', IntegerType()),
        )
        extensionAddition = AdditiveNamedTypes(
            NamedType('i17', IntegerType()),
            NamedType('i18', IntegerType()),
            NamedType('i19', IntegerType()),
            NamedType('i20', IntegerType()),
            NamedType('i21', IntegerType()),
            NamedType('i22', IntegerType()),
            NamedType('i23', IntegerType()),
            NamedType('i24', IntegerType()),
            NamedType('i25', IntegerType()),
            NamedType('i26', IntegerType()),
            NamedType('i27', IntegerType()),
            NamedType('i28', IntegerType()),
            NamedType('i29', IntegerType()),
            NamedType('i30', IntegerType()),
            NamedType('i31', IntegerType()),
            NamedType('i32', IntegerType()),
            NamedType('i33', IntegerType()),
            NamedType('i34', IntegerType()),
            NamedType('i35', IntegerType()),
        )
        componentType = rootComponent + extensionAddition
    return MyChoice


def SCHEMA_selected_choice_from_extension_addition_groups_1():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i0    INTEGER,
            i1    INTEGER,
            ...,
            i2    INTEGER,
            i3    INTEGER,
            i4    INTEGER,
            [[
            i5    INTEGER,
            i6    INTEGER
            ]],
            [[
            i7    INTEGER,
            i8    INTEGER,
            i9    INTEGER
            ]]
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
            NamedType('i1', IntegerType()),
        )
        extensionAddition = AdditiveNamedTypes(
            NamedType('i2', IntegerType()),
            NamedType('i3', IntegerType()),
            NamedType('i4', IntegerType()),
        )
        extensionAdditionGroups = [
            AdditiveNamedTypes(
                NamedType('i5', IntegerType()),
                NamedType('i6', IntegerType()),
            ),
            AdditiveNamedTypes(
                NamedType('i7', IntegerType()),
                NamedType('i8', IntegerType()),
                NamedType('i9', IntegerType()),
            ),
        ]
        componentType = rootComponent + extensionAddition + extensionAdditionGroups
    return MyChoice


def SCHEMA_selected_choice_from_extension_addition_groups_2():
    class MyChoice(ChoiceType):
        '''
        MyChoice ::= CHOICE {
            i0    INTEGER,
            i1    INTEGER,
            ...,
            [[
            i5    INTEGER
            ]],
            [[
            i7    INTEGER,
            i8    INTEGER
            ]],
            [[
            i9    INTEGER
            ]]
        }
        '''
        subtypeSpec = ExtensionMarker(True)
        rootComponent = AdditiveNamedTypes(
            NamedType('i0', IntegerType()),
            NamedType('i1', IntegerType()),
        )
        extensionAdditionGroups = [
            AdditiveNamedTypes(
                NamedType('i5', IntegerType()),
            ),
            AdditiveNamedTypes(
                NamedType('i7', IntegerType()),
                NamedType('i8', IntegerType()),
            ),
            AdditiveNamedTypes(
                NamedType('i9', IntegerType()),
            ),
        ]
        componentType = rootComponent + extensionAdditionGroups
    return MyChoice



def DATA_choice(schema, identifier, value):
    myChoice = schema()
    myChoice[identifier] = value
    return myChoice


@pytest.mark.parametrize("choice, encoded", [
    (DATA_choice(SCHEMA_single_item_choice(), identifier='i0', value=10), '010A'),
    (DATA_choice(SCHEMA_single_item_choice(), identifier='i0', value=100000), '030186A0'),
    (DATA_choice(SCHEMA_no_extension_simple_choice(), identifier='i0', value=10), '00010A'),
    (DATA_choice(SCHEMA_no_extension_simple_choice(), identifier='i0', value=100000), '00030186A0'),
    (DATA_choice(SCHEMA_no_extension_simple_choice(), identifier='i1', value=10), '80010A'),
    (DATA_choice(SCHEMA_no_extension_simple_choice(), identifier='i1', value=100000), '80030186A0'),
    (DATA_choice(SCHEMA_reverse_no_extension_simple_choice(), identifier='i0', value=10), '80010A'),
    (DATA_choice(SCHEMA_reverse_no_extension_simple_choice(), identifier='i0', value=100000), '80030186A0'),
    (DATA_choice(SCHEMA_reverse_no_extension_simple_choice(), identifier='i1', value=10), '00010A'),
    (DATA_choice(SCHEMA_reverse_no_extension_simple_choice(), identifier='i1', value=100000), '00030186A0'),
])
def test_no_extension_marker_choice_can_be_encoded(choice, encoded):
    assert per_encoder(choice) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("choice, encoded", [
    (DATA_choice(SCHEMA_single_item_choice_with_extension(), identifier='i0', value=8), '000108'),
    (DATA_choice(SCHEMA_single_item_choice_with_extension(), identifier='i0', value=68496), '0003010B90'),
    (DATA_choice(SCHEMA_with_extension_simple_choice(), identifier='i0', value=-130), '0002FF7E'),
    (DATA_choice(SCHEMA_with_extension_simple_choice(), identifier='i0', value=23455), '00025B9F'),
    (DATA_choice(SCHEMA_with_extension_simple_choice(), identifier='i1', value=-1), '4001FF'),
    (DATA_choice(SCHEMA_with_extension_simple_choice(), identifier='i1', value=-100000), '4003FE7960'),
    (DATA_choice(SCHEMA_reverse_with_extension_simple_choice(), identifier='i0', value=10), '40010A'),
    (DATA_choice(SCHEMA_reverse_with_extension_simple_choice(), identifier='i0', value=100000), '40030186A0'),
    (DATA_choice(SCHEMA_reverse_with_extension_simple_choice(), identifier='i1', value=10), '00010A'),
    (DATA_choice(SCHEMA_reverse_with_extension_simple_choice(), identifier='i1', value=100000), '00030186A0'),
])
def test_only_extension_marker_preset_choice_can_be_encoded(choice, encoded):
    assert per_encoder(choice) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("choice, encoded", [
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i0', value=10), '00010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i1', value=10), '04010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i3', value=10), '0C010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i6', value=10), '18010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i9', value=10), '24010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i12', value=10), '30010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i15', value=10), '3C010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i16', value=10), '40010A'),
])
def test_extension_present_but_choice_from_root_can_be_encoded(choice, encoded):
    assert per_encoder(choice) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("choice, encoded", [
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_one_elem(), identifier='i2', value=10), '8002010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_one_elem(), identifier='i2', value=-2000), '800302F830'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_one_elem(), identifier='i3', value=10), '8102010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_one_elem(), identifier='i3', value=-2000), '810302F830'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i17', value=0), '80020100'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i17', value=10), '8002010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i18', value=-10), '810201F6'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i19', value=10), '8202010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i20', value=10), '8302010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i22', value=10), '8502010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i24', value=10), '8702010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i26', value=10), '8902010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i29', value=10), '8C02010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i33', value=10), '9002010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i34', value=10), '9102010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_more_elems(), identifier='i35', value=10), '9202010A'),
])
def test_choice_from_extension_addition_can_be_encoded(choice, encoded):
    assert per_encoder(choice) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("choice, encoded", [
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i0', value=10), '00010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i1', value=10), '40010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i2', value=10), '8002010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i3', value=10), '8102010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i4', value=10), '8202010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i5', value=10), '8302010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i6', value=10), '8402010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i7', value=10), '8502010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i8', value=10), '8602010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_1(), identifier='i9', value=10), '8702010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i0', value=10), '00010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i1', value=10), '40010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i5', value=10), '8002010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i7', value=10), '8102010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i8', value=10), '8202010A'),
    (DATA_choice(SCHEMA_selected_choice_from_extension_addition_groups_2(), identifier='i9', value=10), '8302010A'),
])
def test_choice_from_extension_addition_groups_can_be_encoded(choice, encoded):
    assert per_encoder(choice) == bytearray.fromhex(encoded)
