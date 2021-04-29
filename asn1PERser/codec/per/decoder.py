import binascii
from collections import deque
from .encoder import bit_field_size, get_bit_field_size, integer_range, get_range_octet_len, \
    is_constrained_whole_number, is_semi_constrained_whole_number, is_constant


__all__ = ['decode']


class Offset(object):
    def __init__(self, octets=0, bits=0):
        self.prev_octets = octets
        self.prev_bits = bits
        self.curr_octets = octets
        self.curr_bits = bits

    def __add__(self, other):
        self.prev_octets = self.curr_octets
        self.prev_bits = self.curr_bits
        self.curr_octets += other.octets
        self.curr_bits += other.bits
        if self.curr_bits >= 8:
            self.curr_octets += 1
            self.curr_bits = self.curr_bits - 8
        return self

    def align(self):
        if self.curr_bits > 0:
            self.prev_octets = self.curr_octets
            self.prev_bits = 0
            self.curr_octets += (self.curr_bits // 8 if self.curr_bits % 8 == 0 else (1 + self.curr_bits // 8))
            self.curr_bits = 0


class PerBytes(object):
    def __init__(self, byte_string):
        self.offset = Offset()
        self.binary_string = bin(int(byte_string, 16))[2:].zfill(len(byte_string) * 4)

    def next(self, size=bit_field_size(octets=1, bits=0), octet_align=False):
        if octet_align:
            self.offset.align()
        val = int(self[self.offset:self.offset + size], 2)
        return val


    def __getitem__(self, item):
        bits_start = (item.start.prev_octets * 8) + item.start.prev_bits
        bits_stop = (item.stop.curr_octets * 8) + item.stop.curr_bits
        if bits_start == bits_stop:
            return '0'
        return self.binary_string[bits_start:bits_stop]

    def __len__(self):
        return int(len(self.binary_string) / 8)


def decode(per_stream, asn1Spec):
    per_bytes = PerBytes(binascii.hexlify(per_stream))
    decoded = asn1Spec.create_field_list(per_bytes)
    if decoded == '':
        return asn1Spec.__class__('')
    return decoded


def decode_boolean(boolean, per_bytes):    # 12
    boolean_val = per_bytes.next(size=bit_field_size(octets=0, bits=1))
    if boolean_val:
        return boolean.__class__(True)
    else:
        return boolean.__class__(False)


def decode_integer(integer, per_bytes):
    if integer.subtypeSpec.extensionMarker:    # 13.1
        decoded_value_not_within_extension_root_bit = per_bytes.next(size=bit_field_size(octets=0, bits=1))
        if decoded_value_not_within_extension_root_bit:
            unconstrained_whole_number = decode_unconstrained_whole_number(per_bytes)
            return integer.__class__(unconstrained_whole_number)
        else:
            constrained_whole_number = decode_constrained_whole_number_from_field_list(per_bytes=per_bytes,
                                                                                       lowerEndpoint=integer.subtypeSpec.lowerEndpoint,
                                                                                       upperEndpoint=integer.subtypeSpec.upperEndpoint)
            return integer.__class__(constrained_whole_number)
    else:
        if is_constant(integer):
            raise NotImplemented
        elif is_constrained_whole_number(integer):
            if integer.subtypeSpec.lowerEndpoint == integer.subtypeSpec.upperEndpoint:    # 13.2.1
                return (integer.__class__(integer.subtypeSpec.lowerEndpoint))
            else:    # 13.2.2
                constrained_whole_number = decode_constrained_whole_number_from_field_list(per_bytes=per_bytes,
                                                                                           lowerEndpoint=integer.subtypeSpec.lowerEndpoint,
                                                                                           upperEndpoint=integer.subtypeSpec.upperEndpoint)
                return integer.__class__(constrained_whole_number)
        elif is_semi_constrained_whole_number(integer):
            semi_constrained_whole_number = decode_semi_constrained_whole_number_from_field_list(per_bytes=per_bytes,
                                                                                                 lowerBound=integer.subtypeSpec.lowerEndpoint)
            return integer.__class__(semi_constrained_whole_number)
        else:    # 13.2.4
            unconstrained_whole_number = decode_unconstrained_whole_number(per_bytes)
            return integer.__class__(unconstrained_whole_number)


def decode_enumerated(enumerated, per_bytes):
    if not enumerated.subtypeSpec.extensionMarker:    # 14.2
        enumeration_index = decode_constrained_whole_number(per_bytes, lowerBound=0, upperBound=len(list(enumerated.namedValues)) - 1)
        return enumerated.__class__(enumerated.namedValues.getName(enumeration_index))
    else:    # 14.3
        value_is_extension_addition = per_bytes.next(size=bit_field_size(octets=0, bits=1))
        if not value_is_extension_addition:
            enumeration_index = decode_constrained_whole_number(per_bytes, lowerBound=0,
                                                                upperBound=len(list(enumerated.enumerationRoot)) - 1)
            return enumerated.__class__(enumerated.namedValues.getName(enumeration_index))
        else:
            enumeration_index = decode_normally_small_non_negative_whole_number(per_bytes, lower_bound=0)
            enumeration_index += len(enumerated.enumerationRoot)
            return enumerated.__class__(enumerated.namedValues.getName(enumeration_index))


def decode_bitstring(bitstring, per_bytes):
    if bitstring.subtypeSpec.extensionMarker:    # 16.6
        extension_bit_field = per_bytes.next(size=bit_field_size(octets=0, bits=1))
        if not extension_bit_field:
            pass
        else:
            per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
            bitstring_length_determinant = decode_length_determinant(normally_small_length=False,
                                                                     constrained=False,
                                                                     n=per_bytes,
                                                                     lowerBound=0,
                                                                     upperBound=None)
            bitstring_val = per_bytes.next(size=bit_field_size(octets=0, bits=bitstring_length_determinant))
            per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
            return bitstring.__class__(bin(bitstring_val)[2:].zfill(bitstring_length_determinant))
    if bitstring.subtypeSpec.upperEndpoint == 0:    # 16.8
        return ''
    if (bitstring.subtypeSpec.lowerEndpoint is not None) and (bitstring.subtypeSpec.lowerEndpoint == bitstring.subtypeSpec.upperEndpoint):
        if bitstring.subtypeSpec.lowerEndpoint <= 16:    # 16.9
            bitstring_val = per_bytes.next(size=bit_field_size(octets=0, bits=bitstring.subtypeSpec.lowerEndpoint))
            return bitstring.__class__(bin(bitstring_val)[2:].zfill(bitstring.subtypeSpec.lowerEndpoint))
        elif 16 < bitstring.subtypeSpec.lowerEndpoint < 65536:    # 16.10
            per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
            bitstring_val = per_bytes.next(size=bit_field_size(octets=0, bits=bitstring.subtypeSpec.lowerEndpoint))
            bitstring_val = bin(bitstring_val)[2:].zfill(bitstring.subtypeSpec.lowerEndpoint)[:bitstring.subtypeSpec.lowerEndpoint]
            return bitstring.__class__(bitstring_val)
        else:
            raise NotImplemented
    else:    # 16.11
        if bitstring.subtypeSpec.upperEndpoint and bitstring.subtypeSpec.upperEndpoint < 65536:
            bitstring_length_determinant = decode_length_determinant(normally_small_length=False,
                                                                     constrained=True,
                                                                     n=per_bytes,
                                                                     lowerBound=bitstring.subtypeSpec.lowerEndpoint,
                                                                     upperBound=bitstring.subtypeSpec.upperEndpoint)
            bitstring_val = per_bytes.next(size=bit_field_size(octets=0, bits=bitstring_length_determinant), octet_align=True)
            return bitstring.__class__(bin(bitstring_val)[2:].zfill(bitstring_length_determinant))
        else:
            bitstring_length_determinant = decode_length_determinant(normally_small_length=False,
                                                                     constrained=False,
                                                                     n=per_bytes,
                                                                     lowerBound=0,
                                                                     upperBound=None)
            bitstring_val = per_bytes.next(size=bit_field_size(octets=0, bits=bitstring_length_determinant), octet_align=True)
            return bitstring.__class__(bin(bitstring_val)[2:].zfill(bitstring_length_determinant))


def decode_octetstring(octetstring, per_bytes):
    if octetstring.subtypeSpec.extensionMarker:  # 17.3
        extension_bit_field = per_bytes.next(size=bit_field_size(octets=0, bits=1))
        if not extension_bit_field:
            pass
        else:
            per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
            octetstring_length_determinant = decode_length_determinant(normally_small_length=False,
                                                                       constrained=False,
                                                                       n=per_bytes,
                                                                       lowerBound=0,
                                                                       upperBound=None)
            if octetstring_length_determinant == 0:
                return octetstring.__class__(octetstring.__class__.fromHexString(''))
            octetstring_val = per_bytes.next(size=bit_field_size(octets=octetstring_length_determinant, bits=0))
            return octetstring.__class__(octetstring.__class__.fromHexString(hex(octetstring_val)[2:].rstrip("L").zfill(octetstring_length_determinant * 2)))
    if octetstring.subtypeSpec.upperEndpoint == 0:  # 17.5
        return ''
    if (octetstring.subtypeSpec.lowerEndpoint is not None) and (octetstring.subtypeSpec.lowerEndpoint == octetstring.subtypeSpec.upperEndpoint):
        if octetstring.subtypeSpec.lowerEndpoint <= 2:    # 17.6
            octetstring_val  = per_bytes.next(size=bit_field_size(octets=octetstring.subtypeSpec.lowerEndpoint, bits=0))
            return octetstring.__class__(octetstring.__class__.fromHexString(hex(octetstring_val)[2:].rstrip("L").zfill(octetstring.subtypeSpec.lowerEndpoint * 2)))
        elif 2 < octetstring.subtypeSpec.lowerEndpoint < 65536:  # 17.7
            per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
            octetstring_val = per_bytes.next(size=bit_field_size(octets=octetstring.subtypeSpec.lowerEndpoint, bits=0))
            return octetstring.__class__(octetstring.__class__.fromHexString(hex(octetstring_val)[2:].rstrip("L").zfill(octetstring.subtypeSpec.lowerEndpoint * 2)))
        else:
            raise NotImplemented
    else:  # 17.8
        if octetstring.subtypeSpec.upperEndpoint:
            octetstring_length_determinant = decode_length_determinant(normally_small_length=False,
                                                                       constrained=True,
                                                                       n=per_bytes,
                                                                       lowerBound=octetstring.subtypeSpec.lowerEndpoint,
                                                                       upperBound=octetstring.subtypeSpec.upperEndpoint)
            if octetstring_length_determinant == 0:
                return octetstring.__class__(octetstring.__class__.fromHexString(''))
            octetstring_val = per_bytes.next(size=bit_field_size(octets=octetstring_length_determinant, bits=0), octet_align=True)
            return octetstring.__class__(octetstring.__class__.fromHexString(hex(octetstring_val)[2:].rstrip("L")))
        else:
            per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
            octetstring_length_determinant = decode_length_determinant(normally_small_length=False,
                                                                       constrained=False,
                                                                       n=per_bytes,
                                                                       lowerBound=0,
                                                                       upperBound=None)
            octetstring_val = per_bytes.next(size=bit_field_size(octets=octetstring_length_determinant, bits=0))
            return octetstring.__class__(octetstring.__class__.fromHexString(hex(octetstring_val)[2:].rstrip("L").zfill(octetstring_length_determinant * 2)))


def decode_sequence(sequence, per_bytes):
    new_seq = sequence.__class__()
    extension_bit = 0
    optional_default_bit_field_len = 0
    optional_default_bit_field_value = 0
    if sequence.subtypeSpec.extensionMarker:    # 19.1
        extension_bit = per_bytes.next(size=bit_field_size(octets=0, bits=1))
    for namedType in sequence.rootComponent.namedTypes:    # 19.2
        if namedType.isOptional or namedType.isDefaulted:
            optional_default_bit_field_len += 1
    if optional_default_bit_field_len:
        if optional_default_bit_field_len < 65536:    # 19.3
            optional_default_bit_field_value = per_bytes.next(size=bit_field_size(octets=0, bits=optional_default_bit_field_len))
            optional_default_bit_field_value = deque(bin(optional_default_bit_field_value)[2:].zfill(optional_default_bit_field_len))
        else:
            raise NotImplemented
    for namedType in sequence.rootComponent.namedTypes:
        if namedType.isOptional:
            is_present = int(optional_default_bit_field_value.popleft())
            if is_present:
                componentType = sequence.getComponentByName(namedType.name)
                decoded = componentType.create_field_list(per_bytes)
                new_seq[namedType.name] = decoded
            else:
                continue
        elif namedType.isDefaulted:    # CANONICAL-PER
            is_present = int(optional_default_bit_field_value.popleft())
            if is_present:
                componentType = sequence.getComponentByName(namedType.name)
                decoded = componentType.create_field_list(per_bytes)
                new_seq[namedType.name] = decoded
            else:
                continue
        else:
            componentType = sequence.getComponentByName(namedType.name)
            decoded = componentType.create_field_list(per_bytes)
            new_seq[namedType.name] = decoded
    if extension_bit:    # 19.7
        extension_addition_len = len(sequence.extensionAddition.namedTypes) if sequence.extensionAddition else 0
        extension_addition_group_len = len(sequence.extensionAdditionGroups)
        extension_addition_bit_field_len = extension_addition_len + extension_addition_group_len
        extension_addition_length_determinant = decode_length_determinant(normally_small_length=True,
                                                                          constrained=False,
                                                                          n=per_bytes,
                                                                          lowerBound=None,
                                                                          upperBound=None)
        extension_addition_bit_field_value = per_bytes.next(size=bit_field_size(octets=0, bits=extension_addition_length_determinant))
        extension_addition_bit_field_bits = bin(extension_addition_bit_field_value)[2:].zfill(extension_addition_bit_field_len)
        per_bytes.next(bit_field_size(octets=0, bits=0), octet_align=True)
        if sequence.extensionAddition:
            for extensionNamedType, is_present_bit in zip(sequence.extensionAddition.namedTypes,
                                                          extension_addition_bit_field_bits[:extension_addition_len]):
                if int(is_present_bit):
                    componentType = sequence.getComponentByName(extensionNamedType.name)
                    decoded = decode_open_type_field(componentType, per_bytes)
                    new_seq[extensionNamedType.name] = decoded
        if sequence.extensionAdditionGroups:
            for extensionAdditionGroup, is_present_bit in zip(sequence.extensionAdditionGroups,
                                                              extension_addition_bit_field_bits[extension_addition_len:]):
                if int(is_present_bit):
                    group_sequence = create_new_fake_empty_sequence(rootComponent=extensionAdditionGroup)
                    decoded = decode_open_type_field(group_sequence, per_bytes)
                    for type_name, type_value in decoded.named_types.items():
                        new_seq[type_name] = type_value
    return new_seq


def decode_sequence_of(sequence_of, per_bytes):
    new_seq_of = sequence_of.__class__()
    component_type = sequence_of.getComponentType()
    if sequence_of.subtypeSpec.extensionMarker:  # 20.4
        extension_bit_field = per_bytes.next(size=bit_field_size(octets=0, bits=1), octet_align=False)
        if not extension_bit_field:
            length_determinant = decode_length_determinant(normally_small_length=False,
                                                           constrained=True,
                                                           n=per_bytes,
                                                           lowerBound=sequence_of.subtypeSpec.lowerEndpoint,
                                                           upperBound=sequence_of.subtypeSpec.upperEndpoint)
            for index in range(length_determinant):
                val = component_type.create_field_list(per_bytes)
                new_seq_of.extend([val])
            return new_seq_of
        else:
            per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
            length_determinant = decode_length_determinant(normally_small_length=False,
                                                           constrained=False,
                                                           n=per_bytes,
                                                           lowerBound=0,
                                                           upperBound=None)
            for index in range(length_determinant):
                val = component_type.create_field_list(per_bytes)
                new_seq_of.extend([val])
            return new_seq_of
    elif (sequence_of.subtypeSpec.lowerEndpoint == sequence_of.subtypeSpec.upperEndpoint) and (sequence_of.subtypeSpec.upperEndpoint < 65536):    # 20.5
        for index in range(sequence_of.subtypeSpec.lowerEndpoint):
            val = component_type.create_field_list(per_bytes)
            new_seq_of.extend([val])
        return new_seq_of
    else:  # 20.6
        if sequence_of.subtypeSpec.upperEndpoint:
            length_determinant = decode_length_determinant(normally_small_length=False,
                                                           constrained=True,
                                                           n=per_bytes,
                                                           lowerBound=sequence_of.subtypeSpec.lowerEndpoint,
                                                           upperBound=sequence_of.subtypeSpec.upperEndpoint)
            for index in range(length_determinant):
                val = component_type.create_field_list(per_bytes)
                new_seq_of.extend([val])
            return new_seq_of
        else:
            length_determinant = decode_length_determinant(normally_small_length=False,
                                                           constrained=False,
                                                           n=per_bytes,
                                                           lowerBound=sequence_of.subtypeSpec.lowerEndpoint,
                                                           upperBound=None)
            for index in range(length_determinant):
                val = component_type.create_field_list(per_bytes)
                new_seq_of.extend([val])
            return new_seq_of


def decode_choice(choice, per_bytes):    # 23
    new_choice = choice.__class__()
    n = len(choice.rootComponent.namedTypes) - 1
    if not choice.subtypeSpec.extensionMarker:  # 23.6
        if len(choice.rootComponent.namedTypes) == 1:  # 23.4
            selected_type = choice.rootComponent.namedTypes[0]
            selected_component = choice.getComponentByName(selected_type.name)
            val = selected_component.create_field_list(per_bytes)
            new_choice[selected_type.name] = val
            return new_choice
        else:    # 23.6
            index = decode_constrained_whole_number_from_field_list(per_bytes, lowerEndpoint=0, upperEndpoint=n)
            namedType = choice.rootComponent.namedTypes[index]
            selected_component = choice.getComponentByPosition(index)
            val = selected_component.create_field_list(per_bytes)
            new_choice[namedType.name] = val
        return new_choice
    else:    # 23.5
        extension_bit = per_bytes.next(size=bit_field_size(octets=0, bits=1), octet_align=False)
        if not extension_bit:    # 23.7
            if len(choice.rootComponent.namedTypes) == 1:  # 23.4
                selected_type = choice.rootComponent.namedTypes[0]
                selected_component = choice.getComponentByName(selected_type.name)
                val = selected_component.create_field_list(per_bytes)
                new_choice[selected_type.name] = val
                return new_choice
            else:
                index = decode_constrained_whole_number_from_field_list(per_bytes, lowerEndpoint=0, upperEndpoint=n)
                namedType = choice.rootComponent.namedTypes[index]
                selected_component = choice.getComponentByPosition(index)
                val = selected_component.create_field_list(per_bytes)
                new_choice[namedType.name] = val
                return new_choice
        else:    # 23.8
            index = decode_normally_small_non_negative_whole_number(per_bytes, lower_bound=0)
            if choice.extensionAddition and not choice.extensionAdditionGroups:
                choice_extension = choice.extensionAddition
            elif not choice.extensionAddition and choice.extensionAdditionGroups:
                choice_extension = choice.extensionAdditionGroups[0].__class__(*[named_type for additive_named_types in choice.extensionAdditionGroups for
                                                                                 named_type in additive_named_types._NamedTypes__namedTypes])
            elif choice.extensionAddition and choice.extensionAdditionGroups:
                choice_extension = choice.extensionAddition + choice.extensionAdditionGroups
            namedType = choice_extension.namedTypes[index]
            selected_component = choice.getComponentByName(namedType.name)
            val = decode_open_type_field(selected_component, per_bytes)
            new_choice[namedType.name] = val
            return new_choice


def decode_constrained_whole_number_from_field_list(per_bytes, lowerEndpoint, upperEndpoint):
    if integer_range(lowerEndpoint, upperEndpoint) <= 65536:  # 13.2.5
        return decode_constrained_whole_number(per_bytes, lowerBound=lowerEndpoint, upperBound=upperEndpoint)
    else:    # 13.2.6
        upperBound = get_range_octet_len(upperEndpoint - lowerEndpoint)
        constrained_length_determinant = decode_length_determinant(normally_small_length=False,
                                                                   constrained=True,
                                                                   n=per_bytes,
                                                                   lowerBound=1,
                                                                   upperBound=upperBound)

        val = per_bytes.next(bit_field_size(octets=constrained_length_determinant, bits=0), octet_align=True)
        return lowerEndpoint + val


def decode_semi_constrained_whole_number_from_field_list(per_bytes, lowerBound):
    unconstrained_length_determinant = decode_length_determinant(normally_small_length=False,
                                                                 constrained=False,
                                                                 n=per_bytes,
                                                                 lowerBound=1,
                                                                 upperBound=None)
    val = per_bytes.next(bit_field_size(octets=unconstrained_length_determinant, bits=0))
    return lowerBound + val


def decode_open_type_field(type, per_bytes):
    unconstrained_length_determinant = decode_length_determinant(normally_small_length=False,
                                                                 constrained=False,
                                                                 n=per_bytes,
                                                                 lowerBound=None,
                                                                 upperBound=None)
    val = per_bytes.next(size=bit_field_size(octets=unconstrained_length_determinant, bits=0), octet_align=True)
    open_type_value = PerBytes(hex(val)[2:].rstrip("L").zfill(unconstrained_length_determinant * 2))
    decoded = type.create_field_list(open_type_value)
    return decoded


def decode_constrained_whole_number(per_bytes, lowerBound, upperBound):
    range = upperBound - lowerBound + 1
    field_size = get_bit_field_size(range)
    if range == 1:
        return 0
    elif range <= 255:
        non_negative_binary_integer = decode_non_negative_binary_integer(per_bytes, field_size, octet_align=False)
    elif range == 256:
        per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
        non_negative_binary_integer = decode_non_negative_binary_integer(per_bytes, field_size, octet_align=True)
    elif 257 <= range <= 65536:
        per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
        non_negative_binary_integer = decode_non_negative_binary_integer(per_bytes, field_size, octet_align=True)
    elif range > 65536:
        non_negative_binary_integer = decode_non_negative_binary_integer(per_bytes, field_size,
                                                                         octet_align=True,
                                                                         minimum_number_of_octets=True)
        return non_negative_binary_integer
    return lowerBound + non_negative_binary_integer


def decode_normally_small_non_negative_whole_number(per_bytes, lower_bound):    # 11.6
    single_bit_field = per_bytes.next(size=bit_field_size(octets=0, bits=1))
    if not single_bit_field:    # 11.6.1    # n <= 63
        normally_small_non_negative_whole_number = decode_non_negative_binary_integer(per_bytes=per_bytes,
                                                                                      field_size=bit_field_size(octets=0, bits=6),
                                                                                      octet_align=False)
        return normally_small_non_negative_whole_number
    else:    # 11.6.2
        per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
        semi_constrained_whole_number = decode_semi_constrained_whole_number_from_field_list(per_bytes, lowerBound=lower_bound)
        return semi_constrained_whole_number


def decode_unconstrained_whole_number(per_bytes):
    unconstrained_length_determinant = per_bytes.next(octet_align=True)
    unconstrained_whole_number = twos_comp(
        per_bytes=per_bytes.next(bit_field_size(octets=unconstrained_length_determinant, bits=0)),
        bits=8*unconstrained_length_determinant)
    return unconstrained_whole_number


def decode_non_negative_binary_integer(per_bytes, field_size, octet_align, minimum_number_of_octets=False):
    if minimum_number_of_octets:
        raise NotImplemented
    else:
        decoded = per_bytes.next(field_size)
        if octet_align:
            per_bytes.next(size=bit_field_size(octets=0, bits=0), octet_align=octet_align)
        return decoded


def twos_comp(per_bytes, bits):
    """compute the 2's complement of int value val"""
    if (per_bytes & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        per_bytes = per_bytes - (1 << bits)        # compute negative value
    return per_bytes


def decode_length_determinant(normally_small_length, constrained, n, lowerBound, upperBound):
    if normally_small_length:    # 11.9.3.4
        single_bit_field = n.next(size=bit_field_size(octets=0, bits=1))
        if not single_bit_field:    # n <= 64
            normally_small_length_determinant_size = decode_non_negative_binary_integer(per_bytes=n,
                                                                                        field_size=bit_field_size(octets=0, bits=6),
                                                                                        octet_align=False)
            return normally_small_length_determinant_size + 1
        else:    # n > 64
            raise NotImplemented
    elif constrained:
        constrained_length_determinant = decode_constrained_whole_number(per_bytes=n, lowerBound=lowerBound, upperBound=upperBound)
        return constrained_length_determinant
    else:
        n.next(size=bit_field_size(octets=0, bits=0), octet_align=True)
        first_bit = n.next(bit_field_size(octets=0, bits=1))
        if not first_bit:    # 11.9.3.6
            unconstrained_length_determinant = decode_non_negative_binary_integer(per_bytes=n,
                                                                                  field_size=bit_field_size(octets=0, bits=7),
                                                                                  octet_align=True)
            return unconstrained_length_determinant
        else:
            second_bit = n.next(bit_field_size(octets=0, bits=1))
            if not second_bit:    # 11.9.3.7
                unconstrained_length_determinant = decode_non_negative_binary_integer(per_bytes=n,
                                                                                      field_size=bit_field_size(
                                                                                      octets=1, bits=6),
                                                                                      octet_align=True)
                return unconstrained_length_determinant
            else:
                raise NotImplemented


def create_new_fake_empty_sequence(rootComponent):
    class FooConstraint(object):
        pass

    class FakeSequence(object):
        subtypeSpec = FooConstraint()
        def __init__(self):
            self.named_types = {}

        def create_field_list(self, per_bytes):
            return decode_sequence(self, per_bytes)

        def getComponentByName(self, name):
            idx = self.rootComponent.getPositionByName(name)
            return self.rootComponent.getTypeByPosition(idx)

        def __setitem__(self, key, value):
            self.named_types[key] = value

    FakeSequence.subtypeSpec.extensionMarker = False
    FakeSequence.subtypeSpec.lowerEndpoint= None
    FakeSequence.subtypeSpec.upperEndpoint= None
    FakeSequence.rootComponent = rootComponent
    FakeSequence.componentType = rootComponent
    FakeSequence.extensionAddition = None
    FakeSequence.extensionAdditionGroups = []
    return FakeSequence()
