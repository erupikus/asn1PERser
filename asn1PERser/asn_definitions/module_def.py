from pyparsing import Or, And, Forward, Literal, ZeroOrMore, Group
from asn1PERser.classes.parse_actions import parse_ModuleDefinition
from .assignment_def import TypeAssignment, ValueAssignment
from .common_def import DefinedValue
from .lexical_items import COMMA, LEFT_CURLY_BRACKET, RIGHT_CURLY_BRACKET, \
    assignment, typereference, valuereference, empty, modulereference, \
    number, identifier


FROM = Literal("FROM")
EXPLICIT_TAGS = Literal("EXPLICIT TAGS")
IMPLICIT_TAGS = Literal("IMPLICIT TAGS")
AUTOMATIC_TAGS = Literal("AUTOMATIC TAGS")
DEFINITIONS = Literal("DEFINITIONS").setResultsName("DEFINITIONS")
BEGIN = Literal("BEGIN").setResultsName("BEGIN")
END = Literal("END").setResultsName("END")


# 13.1
Assignment = Or([
    TypeAssignment,
    ValueAssignment,
    # XMLValueAssignment,
    # ValueSetTypeAssignment,
    # ObjectClassAssignment,    # Rec. ITU-T X.681 | ISO/IEC 8824-2, 9.1
    # ObjectAssignment,         # Rec. ITU-T X.681 | ISO/IEC 8824-2, 11.1
    # ObjectSetAssignment,      # Rec. ITU-T X.681 | ISO/IEC 8824-2, 12.1
    # ParameterizedAssignment   # Rec. ITU-T X.683 | ISO/IEC 8824-4, 8.1
])


# 13.1
# AssignmentList = Forward()
# AssignmentList << Or([
#                       Assignment,
#                       AssignmentList + Assignment
# ])
AssignmentList = ZeroOrMore(Assignment)


# 13.1
Reference = Or([
    typereference,
    valuereference,
    # objectclassreference,
    # objectreference,
    # objectsetreference
])


# 13.1
Symbol = Or([
    Reference,
    # ParameterizedReference
])


# 13.1
SymbolList = Forward()
SymbolList << Or([
    Symbol,
    SymbolList + COMMA + Symbol
])


# 13.1
AssignedIdentifier = Or([
    # ObjectIdentifierValue,
    DefinedValue,
    empty
])


# 13.1
GlobalModuleReference = modulereference + AssignedIdentifier


# 13.1
SymbolsFromModule = SymbolList + FROM + GlobalModuleReference


# 13.1
SymbolsFromModuleList = Or([
    SymbolsFromModule,
    # SymbolsFromModuleList + SymbolsFromModule
])


# 13.1
SymbolsImported = Or([
    SymbolsFromModuleList,
    empty
])


# 13.1
Imports = Or([
    # "IMPORTS" + SymbolsImported + ";",
    empty
])


# 13.1
SymbolsExported = Or([
    SymbolList,
    empty
])


# 13.1
Exports = Or([
    # "EXPORTS" + SymbolsExported + ";",
    # "EXPORTS ALL" + ";",
    empty
])


# 13.1
ModuleBody = Or([
    Exports + Imports + AssignmentList,
    empty
])

# 13.1
ExtensionDefault = Or([
    # "EXTENSIBILITY IMPLIED",
    empty
])


# 13.1
TagDefault = Or([
    # EXPLICIT_TAGS,
    # IMPLICIT_TAGS,
    AUTOMATIC_TAGS,
    empty
])


# 13.1
EncodingReferenceDefault = Or([
    # encodingreference + "INSTRUCTIONS",
    empty
])


# 13.1
DefinitiveNumberForm = number


# 13.1
DefinitiveNameAndNumberForm = identifier + LEFT_CURLY_BRACKET + DefinitiveNumberForm + RIGHT_CURLY_BRACKET


# 13.1
DefinitiveObjIdComponent = Or([
    # NameForm,
    DefinitiveNumberForm,
    DefinitiveNameAndNumberForm
])


# 13.1
# DefinitiveObjIdComponentList = Or([
#                                    DefinitiveObjIdComponent,
#                                    DefinitiveObjIdComponent + DefinitiveObjIdComponentList
#                                  ])


# 13.1
# DefinitiveOIDandIRI = And([
#                            DefinitiveOID,
#                            IRIValue
#                          ])


# 13.1
# DefinitiveOID = "{" + DefinitiveObjIdComponentList + "}"


# 13.1
DefinitiveIdentification = Or([
    # DefinitiveOID,
    # DefinitiveOIDandIRI,
    empty
])


# 13.1
ModuleIdentifier = And([
    modulereference,
    # DefinitiveIdentification
])


# 13.1
ModuleDefinition = And([
    ModuleIdentifier.setResultsName("ModuleIdentifier"),
    DEFINITIONS,
    EncodingReferenceDefault.setResultsName("EncodingReferenceDefault"),
    TagDefault.setResultsName("TagDefault"),
    ExtensionDefault.setResultsName("ExtensionDefault"),
    assignment,
    BEGIN,
    Group(ModuleBody).setResultsName("ModuleBody"),
    # EncodingControlSection + \
    END
]).setParseAction(parse_ModuleDefinition)
