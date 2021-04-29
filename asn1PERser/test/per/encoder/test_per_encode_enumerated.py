import pytest
from pyasn1.type.namedval import NamedValues
from asn1PERser.codec.per.encoder import encode as per_encoder
from asn1PERser.classes.data.builtin.EnumeratedType import EnumeratedType
from asn1PERser.classes.types.constraint import ExtensionMarker


def SCHEMA_my_enum(enumerationRoot_list, extensionMarker_value=False):
    class MyEnum(EnumeratedType):
        '''
        MyEnum ::= ENUMERATED {
            e0,
            e1,
            .
            .
            .
            eN-1
            eN
        }
        '''
        subtypeSpec = ExtensionMarker(extensionMarker_value)
        enumerationRoot = NamedValues(
            *[(item, index) for index, item in enumerate(enumerationRoot_list)]
        )
        extensionAddition = NamedValues(
        )
        namedValues = enumerationRoot + extensionAddition
    return MyEnum


def SCHEMA_my_ext_enum(enumerationRoot_list, extensionAddition_list, extensionMarker_value=False):
    class MyEnum(EnumeratedType):
        '''
        MyEnum::= ENUMERATED
        {
            e0,
            e1,
            .
            .
            .
            eN - 1
            eN,
            ...,
            eN+1
            .
            .
            .
            eM-1,
            eM
        }
        '''
        subtypeSpec = ExtensionMarker(extensionMarker_value)
        enumerationRoot = NamedValues(
            *[(item, index) for index, item in enumerate(enumerationRoot_list)]
        )
        extensionAddition = NamedValues(
            *[(item, index) for index, item in enumerate(extensionAddition_list, start=len(enumerationRoot_list))]
        )
        namedValues = enumerationRoot + extensionAddition
    return MyEnum


def DATA_my_enum(enum, value):
    return enum(value)


short_enum = ['a0', 'a1']
enumeration_list = ['e0',   'e1',   'e2',   'e3',   'e4',   'e5',   'e6',   'e7',   'e8',   'e9',
                    'e10',  'e11',  'e12',  'e13',  'e14',  'e15',  'e16',  'e17',  'e18',  'e19',
                    'e20',  'e21',  'e22',  'e23',  'e24',  'e25',  'e26',  'e27',  'e28',  'e29',
                    'e30',  'e31',  'e32',  'e33',  'e34',  'e35',  'e36',  'e37',  'e38',  'e39',
                    'e40',  'e41',  'e42',  'e43',  'e44',  'e45',  'e46',  'e47',  'e48',  'e49',
                    'e50',  'e51',  'e52',  'e53',  'e54',  'e55',  'e56',  'e57',  'e58',  'e59',
                    'e60',  'e61',  'e62',  'e63',  'e64',  'e65',  'e66',  'e67',  'e68',  'e69',
                    'e70',  'e71',  'e72',  'e73',  'e74',  'e75',  'e76',  'e77',  'e78',  'e79',
                    'e80',  'e81',  'e82',  'e83',  'e84',  'e85',  'e86',  'e87',  'e88',  'e89',
                    'e90',  'e91',  'e92',  'e93',  'e94',  'e95',  'e96',  'e97',  'e98',  'e99',
                    'e100', 'e101', 'e102', 'e103', 'e104', 'e105', 'e106', 'e107', 'e108', 'e109',
                    'e110', 'e111', 'e112', 'e113', 'e114', 'e115', 'e116', 'e117', 'e118', 'e119',
                    'e120', 'e121', 'e122', 'e123', 'e124', 'e125', 'e126', 'e127', 'e128', 'e129',
                    'e130', 'e131', 'e132', 'e133', 'e134', 'e135', 'e136', 'e137', 'e138', 'e139',
                    'e140', 'e141', 'e142', 'e143', 'e144', 'e145', 'e146', 'e147', 'e148', 'e149',
                    'e150', 'e151', 'e152', 'e153', 'e154', 'e155', 'e156', 'e157', 'e158', 'e159',
                    'e160', 'e161', 'e162', 'e163', 'e164', 'e165', 'e166', 'e167', 'e168', 'e169',
                    'e170', 'e171', 'e172', 'e173', 'e174', 'e175', 'e176', 'e177', 'e178', 'e179',
                    'e180', 'e181', 'e182', 'e183', 'e184', 'e185', 'e186', 'e187', 'e188', 'e189',
                    'e190', 'e191', 'e192', 'e193', 'e194', 'e195', 'e196', 'e197', 'e198', 'e199',
                    'e200', 'e201', 'e202', 'e203', 'e204', 'e205', 'e206', 'e207', 'e208', 'e209',
                    'e210', 'e211', 'e212', 'e213', 'e214', 'e215', 'e216', 'e217', 'e218', 'e219',
                    'e220', 'e221', 'e222', 'e223', 'e224', 'e225', 'e226', 'e227', 'e228', 'e229',
                    'e230', 'e231', 'e232', 'e233', 'e234', 'e235', 'e236', 'e237', 'e238', 'e239',
                    'e240', 'e241', 'e242', 'e243', 'e244', 'e245', 'e246', 'e247', 'e248', 'e249',
                    'e250', 'e251', 'e252', 'e253', 'e254', 'e255', 'e256', 'e257', 'e258', 'e259']


@pytest.mark.parametrize("enumerated, encoded", [
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:2]), 'e0'), '00'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:2]), 'e1'), '80'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:10]), 'e9'), '90'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:17]), 'e9'), '48'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:33]), 'e9'), '24'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:33]), 'e32'), '80'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:100]), 'e98'), 'C4'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:130]), 'e126'), '7E'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:130]), 'e127'), '7F'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:130]), 'e128'), '80'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:260]), 'e128'), '0080'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:260]), 'e254'), '00FE'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:260]), 'e255'), '00FF'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:260]), 'e256'), '0100'),
])
def test_no_extension_marker_enumerated_can_be_encoded(enumerated, encoded):
    assert per_encoder(enumerated) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("enumerated, encoded", [
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:2], extensionMarker_value=True), 'e0'), '00'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:2], extensionMarker_value=True), 'e1'), '40'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:10], extensionMarker_value=True), 'e9'), '48'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:17], extensionMarker_value=True), 'e9'), '24'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:33], extensionMarker_value=True), 'e9'), '12'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:33], extensionMarker_value=True), 'e32'), '40'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:100], extensionMarker_value=True), 'e98'), '62'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:130], extensionMarker_value=True), 'e126'), '3F00'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:130], extensionMarker_value=True), 'e127'), '3F80'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:130], extensionMarker_value=True), 'e128'), '4000'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:260], extensionMarker_value=True), 'e128'), '000080'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:260], extensionMarker_value=True), 'e254'), '0000FE'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:260], extensionMarker_value=True), 'e255'), '0000FF'),
    (DATA_my_enum(SCHEMA_my_enum(enumerationRoot_list=enumeration_list[0:260], extensionMarker_value=True), 'e256'), '000100'),
])
def test_extension_marker_is_present_and_extension_addition_is_empty_but_value_is_from_root_can_be_encoded(enumerated, encoded):
    assert per_encoder(enumerated) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("enumerated, encoded", [
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:2], extensionAddition_list=short_enum, extensionMarker_value=True), 'e0'), '00'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:2], extensionAddition_list=short_enum, extensionMarker_value=True), 'e1'), '40'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:10], extensionAddition_list=short_enum, extensionMarker_value=True), 'e9'), '48'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:17], extensionAddition_list=short_enum, extensionMarker_value=True), 'e9'), '24'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:33], extensionAddition_list=short_enum, extensionMarker_value=True), 'e9'), '12'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:33], extensionAddition_list=short_enum, extensionMarker_value=True), 'e32'), '40'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:100], extensionAddition_list=short_enum, extensionMarker_value=True), 'e98'), '62'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:130], extensionAddition_list=short_enum, extensionMarker_value=True), 'e126'), '3F00'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:130], extensionAddition_list=short_enum, extensionMarker_value=True), 'e127'), '3F80'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:130], extensionAddition_list=short_enum, extensionMarker_value=True), 'e128'), '4000'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:260], extensionAddition_list=short_enum, extensionMarker_value=True), 'e128'), '000080'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:260], extensionAddition_list=short_enum, extensionMarker_value=True), 'e254'), '0000FE'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:260], extensionAddition_list=short_enum, extensionMarker_value=True), 'e255'), '0000FF'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=enumeration_list[0:260], extensionAddition_list=short_enum, extensionMarker_value=True), 'e256'), '000100'),
])
def test_extension_marker_is_present_and_extension_addition_is_not_empty_but_value_is_from_root_can_be_encoded(enumerated, encoded):
    assert per_encoder(enumerated) == bytearray.fromhex(encoded)


@pytest.mark.parametrize("enumerated, encoded", [
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:2], extensionMarker_value=True), 'e0'), '80'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:2], extensionMarker_value=True), 'e1'), '81'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:10], extensionMarker_value=True), 'e9'), '89'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:17], extensionMarker_value=True), 'e9'), '89'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:33], extensionMarker_value=True), 'e9'), '89'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:33], extensionMarker_value=True), 'e32'), 'A0'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:100], extensionMarker_value=True), 'e98'), 'C00162'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:130], extensionMarker_value=True), 'e126'), 'C0017E'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:130], extensionMarker_value=True), 'e127'), 'C0017F'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:130], extensionMarker_value=True), 'e128'), 'C00180'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:260], extensionMarker_value=True), 'e128'), 'C00180'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:260], extensionMarker_value=True), 'e254'), 'C001FE'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:260], extensionMarker_value=True), 'e255'), 'C001FF'),
    (DATA_my_enum(SCHEMA_my_ext_enum(enumerationRoot_list=short_enum, extensionAddition_list=enumeration_list[0:260], extensionMarker_value=True), 'e256'), 'C0020100'),
])
def test_extension_marker_is_present_and_value_is_from_extension_can_be_encoded(enumerated, encoded):
    assert per_encoder(enumerated) == bytearray.fromhex(encoded)



