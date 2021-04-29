from ..type import Type


class DateType(Type):
    def __init__(self):
        super(DateType, self).__init__()
        self.typereference = "DATE"

    def __repr__(self):
        return '\t' + super(DateType, self).__repr__() + '\n'
