from pyasn1.type.namedtype import NamedTypes
from asn1PERser.classes.templates import Template
from asn1PERser.classes.types.constraint import NoConstraint


class Type(Template):
    def __init__(self):
        self._typereference = ''
        self._identifier = ''
        self._valuereference = ''
        self._Value = None
        self._optional = False
        self._default = None
        self._constraint = NoConstraint()

    def fill_template(self):
        raise NotImplemented

    def parse_value(self, value):
        return value

    def is_constrained(self):
        if isinstance(self.constraint, NoConstraint):
            return False
        return True

    @property
    def typereference(self):
        return self._typereference

    @typereference.setter
    def typereference(self, typereference):
        self._typereference = typereference

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def valuereference(self):
        return self._valuereference

    @valuereference.setter
    def valuereference(self, valuereference):
        self._valuereference = valuereference.replace('-', '_')

    @property
    def Value(self):
        return self._Value

    @Value.setter
    def Value(self, value):
        self._Value = self.parse_value(value)

    @property
    def optional(self):
        return self._optional

    @optional.setter
    def optional(self, optional):
        self._optional = optional

    @property
    def default(self):
        if self._default:
            return self.parse_value(self._default)
        return self._default

    @default.setter
    def default(self, default):
        self._default = default

    @property
    def constraint(self):
        return self._constraint

    @constraint.setter
    def constraint(self, constrain):
        self._constraint = constrain

    def __repr__(self):
        type = 'TYPE: {}'.format(self.__class__.__name__)
        typereference = 'typeref: {}'.format(self.typereference)
        identifier = 'id: {}'.format(self.identifier if self.identifier else None)
        valuereference = 'valueref: {}'.format(self.valuereference if self.valuereference else None)
        value = 'val: {}'.format(str(self.Value))
        constrain = 'con: {}'.format(str(self.constraint))
        optional = 'OPT: {}'.format(str(self.optional))
        default = 'DEF: {}'.format(self.default)
        return '(' + ', '.join([type, typereference, identifier, valuereference,
                                value, constrain, optional, default]) + ')'


class SimpleType(Type):
    pass


class ComponentType(Type):
    pass


class DefType(Type):
    pass


class AdditiveNamedTypes(NamedTypes):
    def __init__(self, *named_types):
        self.additive_named_types = list(named_types)
        super(AdditiveNamedTypes, self).__init__(*self.additive_named_types)

    def __add__(self, other):
        if isinstance(other, list):
            all_named_types = []
            for additive_named_type_element in other:
                all_named_types.extend(additive_named_type_element.additive_named_types)
            return AdditiveNamedTypes(*(self.additive_named_types + all_named_types))
        else:
            return AdditiveNamedTypes(*(self.additive_named_types + other.additive_named_types))