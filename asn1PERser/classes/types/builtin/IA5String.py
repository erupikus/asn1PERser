from ..type import SimpleType


class IA5String(SimpleType):
    def __init__(self):
        super(IA5String, self).__init__()
        self.typereference = "IA5String"

    def __repr__(self):
        return '\t' + super(IA5String, self).__repr__() + '\n'
