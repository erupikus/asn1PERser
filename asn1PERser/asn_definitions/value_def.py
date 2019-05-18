from pyparsing import Or, Forward, Literal, ZeroOrMore
from .common_def import SignedNumber, DefinedValue, NULL, CharacterStringList, Quadruple, Tuple
from .lexical_items import identifier, realnumber, HYPHEN_MINUS, COMMA, \
    LEFT_CURLY_BRACKET, RIGHT_CURLY_BRACKET, bstring, hstring, cstring


TRUE = Literal("TRUE")
FALSE = Literal("FALSE")
PLUS_INFINITY = Literal("PLUS-INFINITY")
MINUS_INFINITY = Literal("MINUS-INFINITY")
NOT_A_NUMBER = Literal("NOT-A-NUMBER")
CONTAINING = Literal("CONTAINING")


Value = Forward()
# ComponentValueList = Forward()


# 17.13
NamedValue = identifier + Value


# 25.18
ComponentValueList = Or([
    NamedValue + ZeroOrMore(COMMA + NamedValue),
    # NamedValue,
    # ComponentValueList + COMMA + NamedValue    # ORIGINAL
])


# 25.18
SequenceValue = Or([
    LEFT_CURLY_BRACKET + ComponentValueList + RIGHT_CURLY_BRACKET,
    LEFT_CURLY_BRACKET + RIGHT_CURLY_BRACKET
])


# 21.6
SpecialRealValue = Or([
    PLUS_INFINITY,
    MINUS_INFINITY,
    NOT_A_NUMBER
])


# 21.6
NumericRealValue = Or([
    realnumber,
    HYPHEN_MINUS + realnumber,
    SequenceValue
])


# 21.6
RealValue = Or([
    NumericRealValue,
    SpecialRealValue
])


# 17.11
ReferencedValue = Or([
    DefinedValue,
    # ValueFromObject    # Rec. ITU-T X.681 | ISO/IEC 8824-2, clause 15
])


# 19.9
IntegerValue = Or([
    SignedNumber,
    identifier
])


# 23.3
OctetStringValue = Or([
    bstring,
    hstring,
    CONTAINING + Value
])


# 18.3
BooleanValue = Or([
    TRUE,
    FALSE
])


# 24.3
NullValue = NULL


# 41.8
RestrictedCharacterStringValue = Or([
    cstring,
    CharacterStringList,
    Quadruple,
    Tuple
])


# 40.3
CharacterStringValue = Or([
    RestrictedCharacterStringValue,
    # UnrestrictedCharacterStringValue,
])


# 17.9
BuiltinValue = Or([
    # BitStringValue,
    BooleanValue,
    CharacterStringValue,
    # ChoiceValue,
    # EmbeddedPDVValue,
    # EnumeratedValue,
    # ExternalValue,
    # InstanceOfValue,
    IntegerValue,
    # IRIValue,
    NullValue,
    # ObjectIdentifierValue,
    OctetStringValue,
    RealValue,
    # RelativeIRIValue,
    # RelativeOIDValue,
    SequenceValue,
    # SequenceOfValue,
    # SetValue,
    # SetOfValue,
    # PrefixedValue,
    # TimeValue
])


# 17.7
Value << Or([
    BuiltinValue,
    ReferencedValue,
    # ObjectClassFieldValue    # Rec. ITU-T X.681 | ISO/IEC 8824-2, 14.6.
])
