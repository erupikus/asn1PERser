from pyparsing import Or, Literal, nestedExpr, Optional, OneOrMore, Forward
from .value_def import Value
# from .type_def import Type
from .common_def import SignedNumber, NamedNumber, NamedNumberList, DefinedValue, NULL
from .lexical_items import identifier, LEFT_CURLY_BRACKET, RIGHT_CURLY_BRACKET, \
    COMMA, leftversionbrackets, rightversionbrackets, empty, \
    LEFT_PARENTHESIS, RIGHT_PARENTHESIS, EXCLAMATION_MARK, COLON, \
    CIRCUMFLEX_ACCENT, VERTICAL_LINE, LESS_THAN_SIGN, rangeseparator, \
    ellipsis, number, LEFT_SQUARE_BRACKET, RIGHT_SQUARE_BRACKET, \
    encodingreference, modulereference, typereference, FULL_STOP


INTERSECTION = Literal("INTERSECTION")
UNION = Literal("UNION")
EXCEPT = Literal("EXCEPT")
ALL = Literal("ALL")
MAX = Literal("MAX")
MIN = Literal("MIN")
SIZE = Literal("SIZE")
FROM = Literal("FROM")


ElementSetSpec = Forward()
ElementSetSpecs = Forward()
Constraint = Forward()


# -------------------------------------------
# 51 Subtype elements
# 51.4.4
UpperEndValue = Or([
    Value,
    MAX
])


# 51.4.4
LowerEndValue = Or([
    Value,
    MIN
])

# 51.4.3
UpperEndpoint = Or([
    UpperEndValue,
    LESS_THAN_SIGN + UpperEndValue
])


# 51.4.3
LowerEndpoint = Or([
    LowerEndValue,
    LowerEndValue + LESS_THAN_SIGN
])


# 51.2.1
SingleValue = Value


# 51.4.1
ValueRange = LowerEndpoint + rangeseparator + UpperEndpoint


# 51.5.1
SizeConstraint = SIZE + Constraint


# 51.6.1
# TypeConstraint = Type


# 51.7.1
PermittedAlphabet = FROM + Constraint


# 51.1
SubtypeElements = Or([
    SingleValue,
    # ContainedSubtype,
    ValueRange,
    # PermittedAlphabet,
    SizeConstraint,
    # TypeConstraint,
    # InnerTypeConstraints,
    # PatternConstraint,
    # PropertySettings,
    # DurationRange,
    # TimePointRange,
    # RecurrenceRange
])

# -------------------------------------------

# 50.5
Elements = Or([
    SubtypeElements,
    # ObjectSetElements,
    LEFT_PARENTHESIS + ElementSetSpec + RIGHT_PARENTHESIS
])


# 50.1
IntersectionMark = Or([
    CIRCUMFLEX_ACCENT,
    INTERSECTION
])


# 50.1
UnionMark = Or([
    VERTICAL_LINE,
    UNION
])


# 50.1
Exclusions = EXCEPT + Elements


# 50.1
IntersectionElements = Or([
    Elements + Optional(Exclusions),
    # Elems + Exclusions    # ORIGINAL
])


# 50.1
# Elems << Elements


# 50.1
Intersections = Or([
    OneOrMore(IntersectionElements + Optional(IntersectionMark + IntersectionElements)),
    # IntersectionElements,    # ORIGINAL
    # IElems + IntersectionMark + IntersectionElements    # ORIGINAL
])

# 50.1
# IElems << Intersections


# 50.1
Unions = Or([
    OneOrMore(Intersections + Optional(UnionMark)),
    # Intersections,    # ORIGINAL
    # UElems + UnionMark + Intersections    # ORIGINAL
])


# 50.1
# UElems << Unions


# 50.1
ElementSetSpec << Or([
    Unions,
    ALL + Exclusions
])


# 50.1
AdditionalElementSetSpec = ElementSetSpec


# 50.1
RootElementSetSpec = ElementSetSpec


# 50.1
ElementSetSpecs << Or([
    RootElementSetSpec,
    RootElementSetSpec + COMMA + ellipsis,
    RootElementSetSpec + COMMA + ellipsis + COMMA + AdditionalElementSetSpec
])



# 53.4
ExceptionIdentification = Or([
    SignedNumber,
    DefinedValue,
    # Type + COLON + Value
])


# 53.4
ExceptionSpec = Or([
    # EXCLAMATION_MARK + ExceptionIdentification,
    empty
])


# 49.7
SubtypeConstraint = ElementSetSpecs


# 49.6
ConstraintSpec = Or([
    SubtypeConstraint,
    # GeneralConstraint
])


# 49.6
Constraint << LEFT_PARENTHESIS + ConstraintSpec + ExceptionSpec + RIGHT_PARENTHESIS
