from ..type import SimpleType


class NullType(SimpleType):
    def __init__(self):
        super().__init__()
        self.typereference = "NULL"

    def __repr__(self):
        return '\t' + super().__repr__() + '\n'
