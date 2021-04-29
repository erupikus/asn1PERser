from collections import namedtuple
from collections import defaultdict
import codecs


__all__ = ['encode']


bit_field_size = namedtuple('bit_field_size', 'octets bits')
bit_field = namedtuple('bit_field', 'octet_align value')


class PerEncodingException(Exception):
    pass


class MandatoryExtensionFieldNotPresent(PerEncodingException):
    pass


class MandatoryFieldNotPresentInExtensionGroup(PerEncodingException):
    pass


class SizeConstrainViolated(PerEncodingException):
    pass


class InvalidComponentIndexIntoStructuredType(PerEncodingException):
    pass


def encode(asn1Spec):
    field_list = []
    asn1Spec.fill_field_list(field_list)
    complete_encoding = _produce_complete_encoding(field_list)
    return codecs.decode(_bin_to_hex(complete_encoding), 'hex_codec')


def _produce_complete_encoding(field_list):    # 11.1
    complete_encoding = ''
    for field in field_list:
        if field.octet_align:
            if len(complete_encoding) % 8 != 0:
                complete_encoding += ''.zfill(abs(len(complete_encoding) % 8 - 8))
            complete_encoding += field.value
            continue
        complete_encoding += field.value
        continue
    if (len(complete_encoding) % 8 != 0) or (len(complete_encoding) == 0):
        complete_encoding += ''.zfill(abs(len(complete_encoding) % 8 - 8))
    return complete_encoding


def _bin_to_hex(binary_str):
    dec_value = int(binary_str, 2)
    return "{value:0{byte_len}x}".format(value=dec_value, byte_len=int(len(binary_str) / 4)).upper()


def encode_boolean(boolean):    # 12
    if boolean._value == True:
        return [bit_field(octet_align=False, value='1')]
    elif boolean._value == False:
        return [bit_field(octet_align=False, value='0')]


def encode_integer(integer):
    if integer.subtypeSpec.extensionMarker:    # 13.1
        if integer.subtypeSpec.lowerEndpoint <= integer._value <= integer.subtypeSpec.upperEndpoint:
            constrained_whole_number_field_list = create_field_list_for_constrained_whole_number(n=integer._value,
                                                                                                 lowerEndpoint=integer.subtypeSpec.lowerEndpoint,
                                                                                                 upperEndpoint=integer.subtypeSpec.upperEndpoint)
            extension_bit_field = bit_field(octet_align=False, value='0')
            return [extension_bit_field] + constrained_whole_number_field_list
        else:
            extension_bit_field = bit_field(octet_align=False, value='1')
            unconstrained_whole_number_field_list = create_field_list_for_unconstrained_whole_number(integer)
            return [extension_bit_field] + unconstrained_whole_number_field_list
    else:
        if is_constant(integer):    # 13.2.1
            pass
        elif is_constrained_whole_number(integer):    # 13.2.2
            constrained_whole_number_field_list = create_field_list_for_constrained_whole_number(n=integer._value,
                                                                                                 lowerEndpoint=integer.subtypeSpec.lowerEndpoint,
                                                                                                 upperEndpoint=integer.subtypeSpec.upperEndpoint)
            return constrained_whole_number_field_list
        elif is_semi_constrained_whole_number(integer):    # 13.2.3
            semi_constrained_whole_number = encode_semi_constrained_whole_number(n=integer._value,
                                                                                 lower_bound=integer.subtypeSpec.lowerEndpoint)
            n = int(len(semi_constrained_whole_number.value) / 8)
            unconstrained_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                         constrained=False,
                                                                         n=n,
                                                                         lowerBound=1,
                                                                         upperBound=None)
            return unconstrained_length_determinant + [semi_constrained_whole_number]

        else:    # 13.2.4
            unconstrained_whole_number_field_list = create_field_list_for_unconstrained_whole_number(integer)
            return unconstrained_whole_number_field_list


def encode_enumerated(enumerated):
    if not enumerated.subtypeSpec.extensionMarker:    # 14.2
        return create_field_list_for_constrained_whole_number(n=enumerated._value, lowerEndpoint=0,
                                                              upperEndpoint=len(list(enumerated.namedValues)) - 1)
    else:    # 14.3
        if enumerated._value in list(enumerated.enumerationRoot.values()):
            extension_bit_field = bit_field(octet_align=False, value='0')
            constrained_whole_number_field_list = create_field_list_for_constrained_whole_number(n=enumerated._value,
                                                                                                 lowerEndpoint=0,
                                                                                                 upperEndpoint=len(list(enumerated.enumerationRoot)) - 1)
            return [extension_bit_field] + constrained_whole_number_field_list
        else:
            n = list(enumerated.extensionAddition.values()).index(enumerated._value)
            extension_bit_field = bit_field(octet_align=False, value='1')
            normally_small_non_negative = encode_normally_small_non_negative_whole_number(n=n, lower_bound=0)
            return [extension_bit_field] + normally_small_non_negative


def encode_bitstring(bitstring):    # 16
    if bitstring.namedValues:    # 16.2, 16.3
        raise NotImplemented

    bitstring_value = bitstring.asBinary()
    bitstring_len = len(bitstring_value)
    extension_bit_field = None
    if bitstring.subtypeSpec.extensionMarker:    # 16.6
        if bitstring.subtypeSpec.lowerEndpoint <= bitstring_len <= bitstring.subtypeSpec.upperEndpoint:
            extension_bit_field = bit_field(octet_align=False, value='0')
        else:
            bitstring_bit_field = bit_field(octet_align=True, value=bitstring_value)
            extension_bit_field = bit_field(octet_align=False, value='1')
            bitstring_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                     constrained=False,
                                                                     n=bitstring_len,
                                                                     lowerBound=0,
                                                                     upperBound=None)
            return [extension_bit_field] + bitstring_length_determinant + [bitstring_bit_field]
    # else:    # 16.7
    if bitstring.subtypeSpec.upperEndpoint == 0:    # 16.8
        return
    if (bitstring.subtypeSpec.lowerEndpoint is not None) and (bitstring.subtypeSpec.lowerEndpoint == bitstring.subtypeSpec.upperEndpoint):
        if bitstring_len <= 16:    # 16.9
            bitstring_bit_field = bit_field(octet_align=False, value=bitstring_value)
            if extension_bit_field:
                return [extension_bit_field, bitstring_bit_field]
            return [bitstring_bit_field]
        elif 16 < bitstring_len < 65536:    # 16.10
            bitstring_bit_field = bit_field(octet_align=True, value=bitstring_value)
            if extension_bit_field:
                return [extension_bit_field, bitstring_bit_field]
            return [bitstring_bit_field]
        else:
            raise NotImplemented
    else:    # 16.11
        bitstring_bit_field = bit_field(octet_align=True, value=bitstring_value)
        if bitstring.subtypeSpec.upperEndpoint and bitstring.subtypeSpec.upperEndpoint < 65536:
            bitstring_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                     constrained=True,
                                                                     n=bitstring_len,
                                                                     lowerBound=bitstring.subtypeSpec.lowerEndpoint,
                                                                     upperBound=bitstring.subtypeSpec.upperEndpoint)
            if extension_bit_field:
                return [extension_bit_field] + bitstring_length_determinant + [bitstring_bit_field]
            return bitstring_length_determinant + [bitstring_bit_field]
        else:
            bitstring_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                     constrained=False,
                                                                     n=bitstring_len,
                                                                     lowerBound=0,
                                                                     upperBound=None)
            if extension_bit_field:
                return [extension_bit_field] + bitstring_length_determinant + [bitstring_bit_field]
            return bitstring_length_determinant + [bitstring_bit_field]


def encode_octetstring(octetstring):
    octetstring_value = ''
    for number in octetstring.asNumbers():
        octetstring_value += bin(number)[2:].zfill(8)
    octetstring_len = int(len(octetstring_value) / 8)

    extension_bit_field = None
    if octetstring.subtypeSpec.extensionMarker:    # 17.3
        if octetstring.subtypeSpec.lowerEndpoint <= octetstring_len <= octetstring.subtypeSpec.upperEndpoint:
            extension_bit_field = bit_field(octet_align=False, value='0')
        else:
            octetstring_bit_field = bit_field(octet_align=False, value=octetstring_value)
            extension_bit_field = bit_field(octet_align=False, value='1')
            octetstring_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                       constrained=False,
                                                                       n=octetstring_len,
                                                                       lowerBound=octetstring.subtypeSpec.lowerEndpoint,
                                                                       upperBound=None)
            return [extension_bit_field] + octetstring_length_determinant + [octetstring_bit_field]
    if octetstring.subtypeSpec.upperEndpoint == 0:    # 17.5
        return
    if (octetstring.subtypeSpec.lowerEndpoint is not None) and (octetstring.subtypeSpec.lowerEndpoint == octetstring.subtypeSpec.upperEndpoint):
        if octetstring_len <= 2:    # 17.6
            octetstring_bit_field = bit_field(octet_align=False, value=octetstring_value)
            if extension_bit_field:
                return [extension_bit_field, octetstring_bit_field]
            return [octetstring_bit_field]
        elif 2 < octetstring_len < 65536:    # 17.7
            octetstring_bit_field = bit_field(octet_align=True, value=octetstring_value)
            if extension_bit_field:
                return [extension_bit_field, octetstring_bit_field]
            return [octetstring_bit_field]
        else:
            raise NotImplemented
    else:    # 17.8
        octetstring_bit_field = bit_field(octet_align=True, value=octetstring_value)
        if octetstring.subtypeSpec.upperEndpoint:
            octetstring_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                       constrained=True,
                                                                       n=octetstring_len,
                                                                       lowerBound=octetstring.subtypeSpec.lowerEndpoint,
                                                                       upperBound=octetstring.subtypeSpec.upperEndpoint)
            if extension_bit_field:
                return [extension_bit_field] + octetstring_length_determinant + [octetstring_bit_field]
            return octetstring_length_determinant + [octetstring_bit_field]
        else:
            octetstring_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                       constrained=False,
                                                                       n=octetstring_len,
                                                                       lowerBound=0,
                                                                       upperBound=None)
            if extension_bit_field:
                return [extension_bit_field] + octetstring_length_determinant + [octetstring_bit_field]
            return octetstring_length_determinant + [octetstring_bit_field]


def encode_sequence(sequence):    # 19
    sequence_field_list = []
    rootComponentFieldList = []
    optional_default_bit_field_value = ''
    for namedType in sequence.rootComponent.namedTypes:
        componentType = sequence.getComponentByName(namedType.name)
        if namedType.isOptional:    # 19.2
            if componentType.isValue:
                if not hasattr(componentType, '_componentValues'):
                    optional_default_bit_field_value += '1'
                    componentType.fill_field_list(rootComponentFieldList)
                else:
                    if len(componentType._componentValues) > 0:
                        optional_default_bit_field_value += '1'
                        componentType.fill_field_list(rootComponentFieldList)
                    else:
                        optional_default_bit_field_value += '0'
            else:
                optional_default_bit_field_value += '0'
        elif namedType.isDefaulted:    # 19.2
            # if isDefaulted, default value must have been initiated when defining asn1 Schema,
            # if default value is different than value passed when filling schema, assume component
            # is present
            if namedType._NamedType__type._value != componentType._value:    # hacky...:) no other way for now
                optional_default_bit_field_value += '1'
                componentType.fill_field_list(rootComponentFieldList)
            else:
                optional_default_bit_field_value += '0'
        else:
            componentType.fill_field_list(rootComponentFieldList)
    if optional_default_bit_field_value:
        if len(optional_default_bit_field_value) < 65536:    # 19.3
            optional_default_bit_field = bit_field(octet_align=False, value=optional_default_bit_field_value)
            rootComponentFieldList = [optional_default_bit_field] + rootComponentFieldList
        else:
            raise NotImplemented
    if sequence.subtypeSpec.extensionMarker:    # 19.1
        extension_bit = bit_field(octet_align=False, value='0')
        if (not sequence.extensionAddition) and (not sequence.extensionAdditionGroups):
            return [extension_bit] + rootComponentFieldList
        if sequence.extensionAddition or sequence.extensionAdditionGroups:    # 19.7
            extension_addition_bit_field_value = ''
            extension_addition_field_list = []
            encoded_extension_addition_groups = []
            extension_group_components = defaultdict(list)
            if sequence.extensionAddition:
                for index, namedType in enumerate(sequence.extensionAddition.namedTypes, start=1):
                    extensionComponentType = sequence.getComponentByName(namedType.name)
                    if extensionComponentType.isValue:
                        if (index > 1) and (not previous_extensionComponent['present']) and (not previous_extensionComponent['optional']):
                            raise MandatoryExtensionFieldNotPresent(previous_extensionComponent['name'])

                        if not hasattr(extensionComponentType, '_componentValues'):
                            extension_addition_bit_field_value += '1'
                            open_type_field_list = encode_open_type_field(extensionComponentType)
                            extension_addition_field_list.extend(open_type_field_list)
                        else:
                            if len(extensionComponentType._componentValues) > 0:
                                extension_addition_bit_field_value += '1'
                                open_type_field_list = encode_open_type_field(extensionComponentType)
                                extension_addition_field_list.extend(open_type_field_list)
                            else:
                                extension_addition_bit_field_value += '0'
                    else:
                        extension_addition_bit_field_value += '0'
                    previous_extensionComponent = {'name': namedType.name,
                                                   'present': bool(int(extension_addition_bit_field_value[-1])),
                                                   'optional': namedType.isOptional}
            if sequence.extensionAdditionGroups:
                for index_group, extensionAdditionGroup in enumerate(sequence.extensionAdditionGroups, start=1):
                    extension_addition_group_present = False
                    previous_extensionGroupComponent = {}
                    for index, namedType in enumerate(extensionAdditionGroup.namedTypes, start=1):
                        previous_extension_addition_group_component_present = False
                        extensionComponentType = sequence.getComponentByName(namedType.name)
                        if extensionComponentType.isValue:
                            if (index > 1) and (not previous_extensionGroupComponent['present']) and (not previous_extensionGroupComponent['optional']):
                                raise MandatoryFieldNotPresentInExtensionGroup(previous_extensionGroupComponent['name'])
                            if not hasattr(extensionComponentType, '_componentValues'):
                                extension_addition_group_present = True
                                previous_extension_addition_group_component_present = True
                            else:
                                if len(extensionComponentType._componentValues) > 0:
                                    extension_addition_group_present = True
                                    previous_extension_addition_group_component_present = True
                        previous_extensionGroupComponent = {'name': namedType.name,
                                                            'present': previous_extension_addition_group_component_present,
                                                            'optional': namedType.isOptional}
                        extension_group_components[index_group].append(previous_extensionGroupComponent)
                    if not extension_addition_group_present:
                        extension_addition_bit_field_value += '0'
                    else:
                        if (index_group > 1):
                            for previous_extension_group_component in extension_group_components[index_group - 1]:
                                if previous_extension_group_component['present'] or previous_extension_group_component['optional']:
                                    break
                            else:
                                raise MandatoryExtensionFieldNotPresent(extension_group_components[index_group - 1][0]['name'])
                        extension_addition_bit_field_value += '1'
                        group_sequence = create_new_fake_empty_sequence(rootComponent=extensionAdditionGroup)
                        for namedType in extensionAdditionGroup.namedTypes:
                            componentType = sequence.getComponentByName(namedType.name)
                            group_sequence._componentValues.append(componentType)
                        encoded = encode_open_type_field(group_sequence)
                        encoded_extension_addition_groups.extend(encoded)
            extension_addition_bit_field = bit_field(octet_align=False, value=extension_addition_bit_field_value)
            if int(extension_addition_bit_field_value, 2) > 0:    # any extensionAddition is present in encoding
                extension_bit = bit_field(octet_align=False, value='1')
                extension_addition_length_determinant = encode_length_determinant(normally_small_length=True,
                                                                                  constrained=False,
                                                                                  n=len(extension_addition_bit_field_value),
                                                                                  lowerBound=None,
                                                                                  upperBound=None)
                sequence_field_list.extend(
                    [extension_bit] + rootComponentFieldList + extension_addition_length_determinant +
                     [extension_addition_bit_field] + extension_addition_field_list + encoded_extension_addition_groups)
            else:
                extension_bit = bit_field(octet_align=False, value='0')
                sequence_field_list.extend([extension_bit] + rootComponentFieldList)
        return sequence_field_list
    return rootComponentFieldList


def encode_sequence_of(sequence_of):    # 20
    sequence_of_field_list = []
    n = len(sequence_of)
    for component in sequence_of:
        component.fill_field_list(sequence_of_field_list)
    if sequence_of.subtypeSpec.extensionMarker:    #20.4
        if sequence_of.subtypeSpec.lowerEndpoint <= n <= sequence_of.subtypeSpec.upperEndpoint:
            extension_bit_field = bit_field(octet_align=False, value='0')
            length_determinant = encode_length_determinant(normally_small_length=False, constrained=True,
                                                           n=n, lowerBound=sequence_of.subtypeSpec.lowerEndpoint,
                                                           upperBound=sequence_of.subtypeSpec.upperEndpoint)
            return [extension_bit_field] + length_determinant + sequence_of_field_list
        else:
            extension_bit_field = bit_field(octet_align=False, value='1')
            length_determinant = encode_length_determinant(normally_small_length=False, constrained=False,
                                                           n=n, lowerBound=0,    # not certain but it works lb=0
                                                           upperBound=None)
            return [extension_bit_field] + length_determinant + sequence_of_field_list
    elif n < sequence_of.subtypeSpec.lowerEndpoint:
        raise SizeConstrainViolated("Number of SET OF/SEQUENCE OF {} components = {}".format(sequence_of.__class__, n))
    elif sequence_of.subtypeSpec.upperEndpoint and (n > sequence_of.subtypeSpec.upperEndpoint):
        raise InvalidComponentIndexIntoStructuredType('invalid index: {}'.format(sequence_of.subtypeSpec.upperEndpoint + 1))
    elif (sequence_of.subtypeSpec.lowerEndpoint == sequence_of.subtypeSpec.upperEndpoint) and (sequence_of.subtypeSpec.upperEndpoint < 65536):    # 20.5
        return sequence_of_field_list
    else:    # 20.6
        if sequence_of.subtypeSpec.upperEndpoint:
            length_determinant = encode_length_determinant(normally_small_length=False, constrained=True,
                                                           n=n, lowerBound=sequence_of.subtypeSpec.lowerEndpoint,
                                                           upperBound=sequence_of.subtypeSpec.upperEndpoint)
            return [] + length_determinant + sequence_of_field_list
        else:
            length_determinant = encode_length_determinant(normally_small_length=False, constrained=False,
                                                           n=n, lowerBound=sequence_of.subtypeSpec.lowerEndpoint, upperBound=None)
            return [] + length_determinant + sequence_of_field_list


def encode_choice(choice):    # 23
    choice_field_list = []
    n = len(choice.rootComponent.namedTypes) - 1
    selected_component = choice.getComponent()
    selected_name = choice.getName()
    selected_component.fill_field_list(choice_field_list)
    if not choice.subtypeSpec.extensionMarker:    # 23.6
        if len(choice.rootComponent.namedTypes) == 1:    # 23.4
            return choice_field_list
        for index, namedType in enumerate(choice.rootComponent.namedTypes):    # 23.6
            if namedType.name == selected_name:
                encoded_choice_index_bit_field = create_field_list_for_constrained_whole_number(n=index,
                                                                                                lowerEndpoint=0,
                                                                                                upperEndpoint=n)
                return [] + encoded_choice_index_bit_field + choice_field_list
    else:    # 23.5
        for index, namedType in enumerate(choice.rootComponent.namedTypes):
            if namedType.name == selected_name:    # 23.7
                extension_bit_bit_field = bit_field(octet_align=False, value='0')
                if len(choice.rootComponent.namedTypes) == 1:
                    return [extension_bit_bit_field] + choice_field_list
                else:
                    encoded_choice_index_bit_field = create_field_list_for_constrained_whole_number(n=index,
                                                                                                    lowerEndpoint=0,
                                                                                                    upperEndpoint=n)
                    return [extension_bit_bit_field] + encoded_choice_index_bit_field + choice_field_list
        else:
            if choice.extensionAddition and not choice.extensionAdditionGroups:
                choice_extension = choice.extensionAddition
            elif not choice.extensionAddition and choice.extensionAdditionGroups:
                choice_extension = choice.extensionAdditionGroups[0].__class__(*[named_type for additive_named_types in choice.extensionAdditionGroups for
                                                                                 named_type in additive_named_types._NamedTypes__namedTypes])
            elif choice.extensionAddition and choice.extensionAdditionGroups:
                choice_extension = choice.extensionAddition + choice.extensionAdditionGroups
            for index, namedType in enumerate(choice_extension.namedTypes):
                if namedType.name == selected_name:
                    extension_bit_bit_field = bit_field(octet_align=False, value='1')
                    encoded_choice_index_bit_field = encode_normally_small_non_negative_whole_number(n=index,
                                                                                                     lower_bound=0)
                    choice_field_list = encode_open_type_field(type=selected_component)
                    return [extension_bit_bit_field] + encoded_choice_index_bit_field + choice_field_list


def create_field_list_for_constrained_whole_number(n, lowerEndpoint, upperEndpoint):
    constrained_whole_number = encode_constrained_whole_number(n=n,
                                                               lowerBound=lowerEndpoint,
                                                               upperBound=upperEndpoint)
    if integer_range(lowerEndpoint, upperEndpoint) <= 65536:  # 13.2.5
        return [constrained_whole_number]
    else:  # 13.2.6
        n = int(len(constrained_whole_number.value) / 8)
        upperBound = get_range_octet_len(upperEndpoint - lowerEndpoint)
        constrained_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                   constrained=True,
                                                                   n=n,
                                                                   lowerBound=1,
                                                                   upperBound=upperBound)
        return constrained_length_determinant + [constrained_whole_number]


def encode_open_type_field(type):    # 11.2
    type_field_list = []
    type.fill_field_list(type_field_list)
    octet_string = _produce_complete_encoding(type_field_list)
    octet_string_len = int(len(octet_string) / 8)
    unconstrained_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                 constrained=False, n=octet_string_len,
                                                                 lowerBound=None, upperBound=None)
    octet_string_bit_field = bit_field(octet_align=True, value=octet_string)
    return unconstrained_length_determinant + [octet_string_bit_field]


def encode_constrained_whole_number(n, lowerBound, upperBound):    # 11.5
    range = upperBound - lowerBound + 1
    bit_field_size = get_bit_field_size(range)
    value = n - lowerBound
    if range == 1:    # 11.5.4
        return bit_field(octet_align=False, value='')
    elif range <= 255:    # 11.5.7.1
        non_negative_binary_integer = encode_non_negative_binary_integer(value, bit_field_size, octet_align=False)
        return non_negative_binary_integer
    elif range == 256:    # 11.5.7.2
        non_negative_binary_integer = encode_non_negative_binary_integer(value, bit_field_size, octet_align=True)
        return non_negative_binary_integer
    elif 257 <= range <= 65536:    # 11.5.7.3
        non_negative_binary_integer = encode_non_negative_binary_integer(value, bit_field_size, octet_align=True)
        return non_negative_binary_integer
    elif range > 65536:    # 11.5.7.4
        non_negative_binary_integer = encode_non_negative_binary_integer(value, bit_field_size,
                                                                         octet_align=True,
                                                                         minimum_number_of_octets=True)
        return non_negative_binary_integer


def encode_normally_small_non_negative_whole_number(n, lower_bound):    # 11.6
    if n <= 63:    # 11.6.1
        single_bit_field = bit_field(octet_align=False, value='0')
        normally_small_non_negative_whole_number = encode_non_negative_binary_integer(value=n,
                                                                                      size=bit_field_size(octets=0, bits=6),
                                                                                      octet_align=False)
        return [single_bit_field, normally_small_non_negative_whole_number]
    else:    # 11.6.2
        single_bit_field = bit_field(octet_align=False, value='1')
        normally_small_non_negative_whole_number = encode_semi_constrained_whole_number(n=n, lower_bound=lower_bound)
        octet_len = int(len(normally_small_non_negative_whole_number.value) / 8)
        unconstrained_length_determinant = encode_length_determinant(normally_small_length=False,
                                                                     constrained=False,
                                                                     n=octet_len,
                                                                     lowerBound=1,
                                                                     upperBound=None)

        return [single_bit_field] + unconstrained_length_determinant + [normally_small_non_negative_whole_number]


def encode_non_negative_binary_integer(value, size, octet_align, minimum_number_of_octets=False):    # 11.3
    if minimum_number_of_octets:    # 11.3.6
        encoded = bin(value)[2:]
        if len(encoded) % 8 != 0:
            encoded = ''.zfill(abs(len(encoded)%8-8)) + encoded
        return bit_field(octet_align=octet_align, value=encoded)
    else:
        encoded = '{value:0{bit_len}b}'.format(value=value, bit_len=size.octets*8 + size.bits)
        return bit_field(octet_align=octet_align, value=encoded)


def encode_semi_constrained_whole_number(n, lower_bound):    # 11.7
    value = n - lower_bound
    semi_constrained_whole_number = encode_non_negative_binary_integer(value=value, size=None, octet_align=True,
                                                                       minimum_number_of_octets=True)
    return semi_constrained_whole_number


def create_field_list_for_unconstrained_whole_number(integer):
    unconstrained_length_determinant = get_twos_complement_octet_len(integer)
    unconstrained_whole_number = encode_unconstrained_whole_number(integer, unconstrained_length_determinant)
    unconstrained_length_determinant = '{0:08b}'.format(unconstrained_length_determinant)
    return [bit_field(octet_align=True, value=unconstrained_length_determinant + unconstrained_whole_number.value)]


def encode_unconstrained_whole_number(integer, unconstrained_length_determinant):    # 11.8
    unconstrained_whole_number = encode_twos_complement_binary_integer(integer,
                                                                       width=8*unconstrained_length_determinant)
    return bit_field(octet_align=True, value=unconstrained_whole_number)


def encode_twos_complement_binary_integer(integer, width):
    if integer._value == 0:
        return '0' * width
    elif integer._value > 0:
        return bin(integer._value)[2:].zfill(width)
    else:
        xored = (abs(integer._value) - 1) ^ int('1' * width, 2)
        return bin(xored)[2:]


def encode_length_determinant(normally_small_length, constrained, n, lowerBound, upperBound):    # 11.9
    if normally_small_length:    # 11.9.3.4
        if n <= 64:
            single_bit_field = bit_field(octet_align=False, value='0')
            normally_small_length_determinant_size = bit_field_size(octets=0, bits=6)
            normally_small_length_determinant = encode_non_negative_binary_integer(value=n - 1,
                                                                                   size=normally_small_length_determinant_size,
                                                                                   octet_align=False)
            return [single_bit_field, normally_small_length_determinant]
        else:
            raise NotImplemented
    elif constrained:    # 11.9.3.3
        constrained_length_determinant = encode_constrained_whole_number(n=n, lowerBound=lowerBound, upperBound=upperBound)
        return [constrained_length_determinant]
    else:    # 11.9.3.5
        if n <= 127:    # 11.9.3.6
            determinant_size = bit_field_size(octets=0, bits=7)
            encoded_length_determinant = encode_non_negative_binary_integer(value=n, size=determinant_size,
                                                                            octet_align=True)
            encoded_length_determinant_with_8th_bit_zero = bit_field(octet_align=encoded_length_determinant.octet_align,
                                                                     value= '0' + encoded_length_determinant.value)
            return [encoded_length_determinant_with_8th_bit_zero]
        elif 127 < n <= 16384:    # 11.9.3.7
            determinant_size = bit_field_size(octets=1, bits=6)
            encoded_length_determinant = encode_non_negative_binary_integer(value=n, size=determinant_size,
                                                                            octet_align=True)
            encoded_length_determinant_with_8th_bit_one_7th_bit_zero = bit_field(octet_align=encoded_length_determinant.octet_align,
                                                                                 value='10' + encoded_length_determinant.value)
            return [encoded_length_determinant_with_8th_bit_one_7th_bit_zero]
        else:
            raise NotImplemented


def get_bit_field_size(range):
    if range == 1:
        return bit_field_size(octets=0, bits=0)
    elif range == 2:
        return bit_field_size(octets=0, bits=1)
    elif 3 <= range <= 4:
        return bit_field_size(octets=0, bits=2)
    elif 5 <= range <= 8:
        return bit_field_size(octets=0, bits=3)
    elif 9 <= range <= 16:
        return bit_field_size(octets=0, bits=4)
    elif 17 <= range <= 32:
        return bit_field_size(octets=0, bits=5)
    elif 33 <= range <= 64:
        return bit_field_size(octets=0, bits=6)
    elif 65 <= range <= 128:
        return bit_field_size(octets=0, bits=7)
    elif 129 <= range <= 255:
        return bit_field_size(octets=0, bits=8)
    elif range == 256:
        return bit_field_size(octets=1, bits=0)
    elif 256 < range <= 65536:
        return bit_field_size(octets=2, bits=0)
    elif range > 65536:
        range_octet_len = get_range_octet_len(range)
        return bit_field_size(octets=range_octet_len, bits=0)


def integer_range(lb, ub):
    return ub - lb + 1


def get_range_octet_len(range):
    base_power = 8
    power_multiplier = 3
    while True:
        if range < 2 ** ((power_multiplier * base_power)):
            return power_multiplier
        else:
            power_multiplier += 1


def get_twos_complement_octet_len(integer):
    base_power = 8
    power_multiplier = 1
    while True:
        if integer._value >= 0:
            if integer._value < 2 ** ((power_multiplier * base_power) - 1):
                return power_multiplier
            else:
                power_multiplier += 1
        else:
            if integer._value >= -(2 ** ((power_multiplier * base_power - 1))):
                return power_multiplier
            else:
                power_multiplier += 1


def is_constrained_whole_number(integer):
    if (integer.subtypeSpec.lowerEndpoint is not None) and (integer.subtypeSpec.upperEndpoint is not None):
        return True
    return False


def is_semi_constrained_whole_number(integer):
    if (integer.subtypeSpec.lowerEndpoint is not None) and (integer.subtypeSpec.upperEndpoint is None):
        return True
    return False


def is_constant(integer):
    return False


def create_new_fake_empty_sequence(rootComponent):
    class FooConstraint(object):
        pass

    class FakeSequence(object):
        subtypeSpec = FooConstraint()
        def __init__(self):
            self.named_types = {}

        def fill_field_list(self, field_list):
            sequence_field_list = encode_sequence(self)
            if sequence_field_list:
                field_list.extend(sequence_field_list)

        def getComponentByName(self, name):
            idx = self.rootComponent.getPositionByName(name)
            return self._componentValues[idx]

        def __setitem__(self, key, value):
            self.named_types[key] = value

    FakeSequence._componentValues = []
    FakeSequence.subtypeSpec.extensionMarker = False
    FakeSequence.subtypeSpec.lowerEndpoint= None
    FakeSequence.subtypeSpec.upperEndpoint= None
    FakeSequence.rootComponent = rootComponent
    FakeSequence.componentType = rootComponent
    FakeSequence.extensionAddition = None
    FakeSequence.extensionAdditionGroups = []
    return FakeSequence()
