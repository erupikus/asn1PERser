from ..type import Type


class DateType(Type):
    def __init__(self):
        super().__init__()
        self.typereference = "DATE"

    def __repr__(self):
        return '\t' + super().__repr__() + '\n'
