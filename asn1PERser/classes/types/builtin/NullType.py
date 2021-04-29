from ..type import SimpleType


class NullType(SimpleType):
    def __init__(self):
        super(NullType, self).__init__()
        self.typereference = "NULL"

    def __repr__(self):
        return '\t' + super(NullType, self).__repr__() + '\n'
