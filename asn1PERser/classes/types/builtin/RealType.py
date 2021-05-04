from ..type import SimpleType


class RealType(SimpleType):
    def __init__(self):
        super(RealType, self).__init__()
        self.typereference = "REAL"

    def __repr__(self):
        return '\t' + super(RealType, self).__repr__() + '\n'
