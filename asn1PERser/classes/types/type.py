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


class AdditiveNamedTypes(NamedTypes):
    def __add__(self, other):
        if isinstance(other, list):
            other = AdditiveNamedTypes(*[named_type for additive_named_types in other for
                                         named_type in additive_named_types._NamedTypes__namedTypes])
        return self.__class__(*(self._NamedTypes__namedTypes + other._NamedTypes__namedTypes))
