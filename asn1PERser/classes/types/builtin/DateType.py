from ..type import Type


class DateType(Type):
    def __init__(self):
        super(DateType, self).__init__()
        self.typereference = "DATE"
