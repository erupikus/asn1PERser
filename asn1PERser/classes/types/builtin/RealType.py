from ..type import SimpleType


class RealType(SimpleType):
    def __init__(self):
        super().__init__()
        self.typereference = "REAL"

    def __repr__(self):
        return '\t' + super().__repr__() + '\n'
