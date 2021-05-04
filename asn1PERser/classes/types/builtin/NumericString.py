from ..type import SimpleType


class NumericString(SimpleType):
    def __init__(self):
        super(NumericString, self).__init__()
        self.typereference = "NumericString"

    def __repr__(self):
        return '\t' + super(NumericString, self).__repr__() + '\n'
