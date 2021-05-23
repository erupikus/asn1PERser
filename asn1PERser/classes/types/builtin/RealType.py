from ..type import SimpleType


class RealType(SimpleType):
    def __init__(self):
        super(RealType, self).__init__()
        self.typereference = "REAL"
