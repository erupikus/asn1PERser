from ..type import Type


class VisibleString(Type):
    def __init__(self):
        super(VisibleString, self).__init__()
        self.typereference = "VisibleString"

    def __repr__(self):
        return '\t' + super(VisibleString, self).__repr__() + '\n'
