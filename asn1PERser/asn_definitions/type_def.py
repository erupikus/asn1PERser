from pyparsing import Or, And, Forward, Literal, ZeroOrMore, OneOrMore, Optional, nestedExpr, Group
from asn1PERser.classes.parse_actions import parse_SequenceType, parse_ComponentType, \
    parse_ConstrainedType, parse_DateType, parse_TypeWithConstraint, \
    parse_RealType, parse_ChoiceType, parse_AlternativeTypeList, \
    parse_EnumeratedType, parse_OctetStringType, parse_BitStringType, parse_SequenceOfType, \
    parse_Constraint, parse_BooleanType, parse_IntegerType, parse_DefinedType, \
    parse_IA5String, parse_VisibleString, parse_NumericString, parse_UTF8String, parse_ExtensionAdditionAlternativesList
from .common_def import SignedNumber, NamedNumber, NamedNumberList, DefinedValue, NULL
from .lexical_items import identifier, LEFT_CURLY_BRACKET, RIGHT_CURLY_BRACKET, \
    COMMA, leftversionbrackets, rightversionbrackets, empty, \
    LEFT_PARENTHESIS, RIGHT_PARENTHESIS, EXCLAMATION_MARK, COLON, \
    CIRCUMFLEX_ACCENT, VERTICAL_LINE, LESS_THAN_SIGN, rangeseparator, \
    ellipsis, number, LEFT_SQUARE_BRACKET, RIGHT_SQUARE_BRACKET, \
    encodingreference, modulereference, typereference, FULL_STOP
from .value_def import Value


Type = Forward()
Constraint = nestedExpr(opener='(', closer=')').setParseAction(parse_Constraint)


BOOLEAN = Literal("BOOLEAN")
INTEGER = Literal("INTEGER")
OPTIONAL = Literal("OPTIONAL")
DEFAULT = Literal("DEFAULT")
COMPONENTS_OF = Literal("COMPONENTS OF")
BIT_STRING = Literal("BIT STRING")
ENUMERATED = Literal("ENUMERATED")
SEQUENCE = Literal("SEQUENCE")
SEQUENCE_OF = Literal("SEQUENCE OF")
CHOICE = Literal("CHOICE")
SET = Literal("SET")
OF = Literal("OF")
DATE = Literal("DATE")
IMPLICIT = Literal("IMPLICIT")
EXPLICIT = Literal("EXPLICIT")
UNIVERSAL = Literal("UNIVERSAL")
APPLICATION = Literal("APPLICATION")
PRIVATE = Literal("PRIVATE")

IA5String = Literal("IA5String").setParseAction(parse_IA5String)
VisibleString = Literal("VisibleString").setParseAction(parse_VisibleString)
NumericString = Literal("NumericString").setParseAction(parse_NumericString)
UTF8String = Literal("UTF8String").setParseAction(parse_UTF8String)



# 14.6
ExternalTypeReference = modulereference + FULL_STOP + typereference


# 14.1
DefinedType = Or([
    ExternalTypeReference,
    typereference,
    # ParameterizedType,         #  Rec. ITU-T X.683 | ISO/IEC 8824-4.
    # ParameterizedValueSetType  #  Rec. ITU-T X.683 | ISO/IEC 8824-4.
]).setParseAction(parse_DefinedType)


# 53.4
ExceptionIdentification = Or([
    SignedNumber,
    DefinedValue,
    Type + COLON + Value
])


# 53.4
ExceptionSpec = Or([
    EXCLAMATION_MARK + ExceptionIdentification,
    empty
])


# 21.1
RealType = Literal("REAL")
RealType.setParseAction(parse_RealType)


# 17.3
ReferencedType = Or([
    DefinedType,
    # UsefulType,
    # SelectionType,
    # TypeFromObject,        # ITU-T X.681 | ISO/IEC 8824-2, clause 15
    # ValueSetFromObjects    # ITU-T X.681 | ISO/IEC 8824-2, clause 15
])


# 17.5
NamedType = identifier + Type


# 18.1
BooleanType = BOOLEAN
BooleanType.setParseAction(parse_BooleanType)


# 19.1
IntegerType = Or([
    INTEGER,
    INTEGER + LEFT_CURLY_BRACKET + NamedNumberList + RIGHT_CURLY_BRACKET
]).setParseAction(parse_IntegerType)


# 20.1
EnumerationItem = Or([
    identifier,
    NamedNumber
])


# 20.1
Enumeration = Or([
    EnumerationItem + ZeroOrMore(COMMA + EnumerationItem)
    # EnumerationItem,    # ORIGINAL
    # EnumerationItem + COMMA + Enumeration    # ORIGINAL
])


# 20.1
AdditionalEnumeration = Enumeration


# 20.1
RootEnumeration = Enumeration


# 20.1
Enumerations = Or([
    RootEnumeration,
    RootEnumeration + COMMA + ellipsis + ExceptionSpec,
    RootEnumeration + COMMA + ellipsis + ExceptionSpec + COMMA + AdditionalEnumeration
])


# 20.1
EnumeratedType = (ENUMERATED + LEFT_CURLY_BRACKET +
                  Enumerations + RIGHT_CURLY_BRACKET).setParseAction(parse_EnumeratedType)


# 22.1
NamedBit = Or([
    identifier + LEFT_PARENTHESIS + number + RIGHT_PARENTHESIS,
    identifier + LEFT_PARENTHESIS + DefinedType + RIGHT_PARENTHESIS
])


# 22.1
NamedBitList = Or([
    NamedBit + ZeroOrMore(COMMA + NamedBit)
    # NamedBit,    # ORIGINAL
    # NamedBitList + COMMA + NamedBit    # ORIGINAL
])


# 22.1
BitStringType = Or([
    BIT_STRING,
    BIT_STRING + LEFT_CURLY_BRACKET + NamedBitList + RIGHT_CURLY_BRACKET
]).setParseAction(parse_BitStringType)


# 23.1
OctetStringType = Literal("OCTET STRING").setParseAction(parse_OctetStringType)


# 24.1
NullType = NULL


# 25.1
VersionNumber = Or([
    empty,
    number + COLON
])


# 25.1
ExtensionAndException = Or([
    ellipsis,
    ellipsis + ExceptionSpec
])


# 25.1
OptionalExtensionMarker = Or([
    COMMA + ellipsis,
    empty
])


# 25.1
ExtensionEndMarker = COMMA + ellipsis


# 25.1
ComponentType = Or([
    NamedType,
    NamedType + OPTIONAL,
    NamedType + DEFAULT + Value,
    # COMPONENTS_OF + Type
]).setParseAction(parse_ComponentType)


# 25.1
ComponentTypeList = Or([
    ComponentType + ZeroOrMore(COMMA + ComponentType)
    # ComponentType,
    # ComponentTypeList + COMMA + ComponentType,   #    Original from spec

])


# 25.1
RootComponentTypeList = ComponentTypeList


# 25.1
ExtensionAdditionGroup = And([
    leftversionbrackets,
    VersionNumber,
    ComponentTypeList,
    rightversionbrackets
])


# 25.1
ExtensionAddition = Or([
    ComponentType,
    ExtensionAdditionGroup
])


# 25.1
ExtensionAdditionList = Or([
    ExtensionAddition + ZeroOrMore(COMMA + ExtensionAddition),
    # ExtensionAddition,
    # ExtensionAdditionList + COMMA + ExtensionAddition    # ORIGINAL
])


# 25.1
ExtensionAdditions = Or([
    COMMA + ExtensionAdditionList,
    empty
])


# 25.1
ComponentTypeLists = Or([
    RootComponentTypeList,
    RootComponentTypeList + COMMA + ExtensionAndException +
        ExtensionAdditions + OptionalExtensionMarker,
    RootComponentTypeList + COMMA + ExtensionAndException +
        ExtensionAdditions + ExtensionEndMarker + COMMA +
        RootComponentTypeList,
    ExtensionAndException + ExtensionAdditions + ExtensionEndMarker +
        COMMA + RootComponentTypeList,
    ExtensionAndException + ExtensionAdditions + OptionalExtensionMarker
])


# 25.1
SequenceType = Or([
    SEQUENCE + LEFT_CURLY_BRACKET + RIGHT_CURLY_BRACKET,
    # SEQUENCE + LEFT_CURLY_BRACKET + ExtensionAndException +
    # OptionalExtensionMarker + RIGHT_CURLY_BRACKET,
    SEQUENCE + LEFT_CURLY_BRACKET + ComponentTypeLists + RIGHT_CURLY_BRACKET
]).setParseAction(parse_SequenceType)


# 26.1
SequenceOfType = Or([
    SEQUENCE_OF + Type,
    SEQUENCE_OF + NamedType
]).setParseAction(parse_SequenceOfType)


# 29.1
AlternativeTypeList = Or([
    NamedType + ZeroOrMore(COMMA + NamedType)
    # NamedType,    # ORIGINAL
    # AlternativeTypeList + COMMA + NamedType    # ORIGINAL
]).setParseAction(parse_AlternativeTypeList)


# This is not in ASN.1 spec but is needed to distinguish parsing of root vs extension types
ExtensionAdditionAlternativeTypeList = Or([
    NamedType + ZeroOrMore(COMMA + NamedType)
    # NamedType,    # ORIGINAL
    # AlternativeTypeList + COMMA + NamedType    # ORIGINAL
])


# 29.1
ExtensionAdditionAlternativesGroup = leftversionbrackets + VersionNumber + \
                                     ExtensionAdditionAlternativeTypeList + rightversionbrackets


# 29.1
ExtensionAdditionAlternative = Or([
    ExtensionAdditionAlternativesGroup,
    NamedType
]).setParseAction(parse_ExtensionAdditionAlternativesList)


# 29.1
ExtensionAdditionAlternativesList = Or([
    ExtensionAdditionAlternative + ZeroOrMore(COMMA + ExtensionAdditionAlternative)
    # ExtensionAdditionAlternative,    # ORIGINAL
    # ExtensionAdditionAlternativesList + COMMA + ExtensionAdditionAlternative    # ORIGINAL
])


# 29.1
ExtensionAdditionAlternatives = Or([
    COMMA + ExtensionAdditionAlternativesList,
    empty
])


# 29.1
RootAlternativeTypeList = AlternativeTypeList


# 29.1
AlternativeTypeLists = Or([
    RootAlternativeTypeList,
    RootAlternativeTypeList + COMMA + ExtensionAndException +
        ExtensionAdditionAlternatives + OptionalExtensionMarker
])


# 29.1
ChoiceType = (CHOICE + LEFT_CURLY_BRACKET +
              AlternativeTypeLists + RIGHT_CURLY_BRACKET).setParseAction(parse_ChoiceType)


# 38.4.1
DateType = DATE
DateType.setParseAction(parse_DateType)


# 31.2.1
Class = Or([
    UNIVERSAL,
    APPLICATION,
    PRIVATE,
    empty
])


# 31.2.1
ClassNumber = Or([
    number,
    DefinedValue
])


# 31.2.1
EncodingReference = Or([
    encodingreference + COLON,
    empty
])


# 31.2.1
Tag = LEFT_SQUARE_BRACKET + EncodingReference + Class + ClassNumber + RIGHT_SQUARE_BRACKET


# 31.2.1
TaggedType = Or([
    Tag + Type,
    Tag + IMPLICIT + Type,
    Tag + EXPLICIT + Type
])


# 31.1.5
PrefixedType = Or([
    TaggedType,
    # EncodingPrefixedType
])


# 41
RestrictedCharacterStringType = Or([
    # BMPString,
    # GeneralString,
    # GraphicString,
    IA5String,
    # ISO646String,
    NumericString,
    # PrintableString,
    # TeletexString,
    # T61String,
    # UniversalString,
    UTF8String,
    # VideotexString,
    VisibleString
])


# 40.1
CharacterStringType = Or([
    RestrictedCharacterStringType,
    # UnrestrictedCharacterStringType
])


# 17.2
BuiltinType = Or([
    BitStringType,
    BooleanType,
    CharacterStringType,
    ChoiceType,
    DateType,
    # DateTimeType,
    # DurationType ,
    # EmbeddedPDVType,
    EnumeratedType,
    # ExternalType,
    # InstanceOfType,
    IntegerType,
    # IRIType,
    NullType,
    # ObjectClassFieldType,
    # ObjectIdentifierType,
    OctetStringType,
    RealType,
    # RelativeIRIType,
    # RelativeOIDType,
    SequenceType,
    SequenceOfType,
    # SetType,
    # SetOfType,
    PrefixedType,
    # TimeType,
    # TimeOfDayType
])


# 49.5
TypeWithConstraint = Or([
    SET + Constraint + OF + Type,
    # SET + SizeConstraint + OF + Type,    # Present in original
    SEQUENCE + Constraint + OF + Type,
    # SEQUENCE + SizeConstraint + OF + Type,    # Present in original
    SET + Constraint + OF + NamedType,
    # SET + SizeConstraint + OF + NamedType,    # Present in original
    SEQUENCE + Constraint + OF + NamedType,
    # SEQUENCE + SizeConstraint + OF + NamedType    # Present in original
]).setParseAction(parse_TypeWithConstraint)


# 49.1
ConstrainedType = Or([
    BuiltinType + Constraint,
    TypeWithConstraint,
    # Type + Constraint,
    # Type + TypeWithConstraint    # ORIGINAL
]).setParseAction(parse_ConstrainedType)


# 17.1
Type << Or([
    Group(BuiltinType),
    Group(ReferencedType),
    Group(ConstrainedType)
])
