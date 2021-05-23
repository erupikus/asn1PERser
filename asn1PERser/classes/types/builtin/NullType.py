from ..type import SimpleType


class NullType(SimpleType):
    def __init__(self):
        super(NullType, self).__init__()
        self.typereference = "NULL"
