from ..type import SimpleType


class NumericString(SimpleType):
    def __init__(self):
        super().__init__()
        self.typereference = "NumericString"

    def __repr__(self):
        return '\t' + super().__repr__() + '\n'
