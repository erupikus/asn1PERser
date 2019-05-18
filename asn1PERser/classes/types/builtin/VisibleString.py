from ..type import Type


class VisibleString(Type):
    def __init__(self):
        super().__init__()
        self.typereference = "VisibleString"

    def __repr__(self):
        return '\t' + super().__repr__() + '\n'
