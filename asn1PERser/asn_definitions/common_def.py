from pyparsing import Or, Group, ZeroOrMore, Literal
from .lexical_items import number, HYPHEN_MINUS, identifier, LEFT_PARENTHESIS, RIGHT_PARENTHESIS, \
    COMMA, modulereference, FULL_STOP, valuereference, RIGHT_CURLY_BRACKET, LEFT_CURLY_BRACKET, \
    cstring


NULL = Literal("NULL")


# 19.1
SignedNumber = Or([
    number,
    HYPHEN_MINUS + number
]).setParseAction(lambda toks: ''.join(toks))


# 14.6
ExternalValueReference = modulereference + FULL_STOP + valuereference


# 14.1
DefinedValue = Or([
    ExternalValueReference,
    valuereference,
    # ParameterizedValue
])


# 19.1
NamedNumber = Or([
    Group(identifier + LEFT_PARENTHESIS + SignedNumber + RIGHT_PARENTHESIS),
    Group(identifier + LEFT_PARENTHESIS + DefinedValue + RIGHT_PARENTHESIS)
])


# 19.1
NamedNumberList = Or([
    NamedNumber + ZeroOrMore(COMMA + NamedNumber),
    # NamedNumber,
    # NamedNumberList + COMMA + NamedNumber    # ORIGINAL
])


# 41.8
TableRow = number


# 41.8
TableColumn = number


# 41.8
Tuple = LEFT_CURLY_BRACKET + TableColumn + COMMA + TableRow + RIGHT_CURLY_BRACKET


# 41.8
Cell = number


# 41.8
Row = number


# 41.8
Plane = number


# 41.8
Group = number


# 41.8
Quadruple = LEFT_CURLY_BRACKET + Group + COMMA + Plane + COMMA + Row + COMMA + Cell + RIGHT_CURLY_BRACKET


# 41.8
CharsDefn = Or([
    cstring,
    Quadruple,
    Tuple,
    DefinedValue
])


# 41.8
CharSyms = Or([
    CharsDefn + ZeroOrMore(COMMA + CharsDefn),
    # CharsDefn,
    # CharSyms + COMMA + CharsDefn    # ORIGINAL
])


# 41.8
CharacterStringList = LEFT_CURLY_BRACKET + CharSyms + RIGHT_CURLY_BRACKET

