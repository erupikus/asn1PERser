from ..type import SimpleType


class NumericString(SimpleType):
    def __init__(self):
        super(NumericString, self).__init__()
        self.typereference = "NumericString"
