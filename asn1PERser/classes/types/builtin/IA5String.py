from ..type import SimpleType


class IA5String(SimpleType):
    def __init__(self):
        super().__init__()
        self.typereference = "IA5String"

    def __repr__(self):
        return '\t' + super().__repr__() + '\n'
