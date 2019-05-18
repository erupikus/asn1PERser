from string import ascii_uppercase, ascii_lowercase, digits
from pyparsing import oneOf


RESERVED_WORDS = \
['ABSENT',
 'ENCODED',
 'INTERSECTION',
 'SEQUENCE',
 'ABSTRACT-SYNTAX',
 'ENCODING-CONTROL',
 'ISO646String',
 'SET',
 'ALL',
 'END',
 'MAX',
 'SETTINGS',
 'APPLICATION',
 'ENUMERATED',
 'MIN',
 'SIZE',
 'AUTOMATIC',
 'EXCEPT',
 'MINUS-INFINITY',
 'STRING',
 'BEGIN',
 'EXPLICIT',
 'NOT-A-NUMBER',
 'SYNTAX',
 'BIT',
 'EXPORTS',
 'NULL',
 'T61String',
 'BMPString',
 'EXTENSIBILITY',
 'NumericString',
 'TAGS',
 'BOOLEAN',
 'EXTERNAL',
 'OBJECT',
 'TeletexString',
 'BY',
 'FALSE',
 'ObjectDescriptor',
 'TIME',
 'CHARACTER',
 'FROM',
 'OCTET',
 'TIME-OF-DAY',
 'CHOICE',
 'GeneralizedTime',
 'OF',
 'TRUE',
 'CLASS',
 'GeneralString',
 'OID-IRI',
 'TYPE-IDENTIFIER',
 'COMPONENT',
 'GraphicString',
 'OPTIONAL',
 'UNION',
 'COMPONENTS',
 'IA5String',
 'PATTERN',
 'UNIQUE',
 'CONSTRAINED',
 'IDENTIFIER',
 'PDV',
 'UNIVERSAL',
 'CONTAINING',
 'IMPLICIT',
 'PLUS-INFINITY',
 'UniversalString',
 'DATE',
 'IMPLIED',
 'PRESENT',
 'UTCTime',
 'DATE-TIME',
 'IMPORTS',
 'PrintableString',
 'UTF8String',
 'DEFAULT',
 'INCLUDES',
 'PRIVATE',
 'VideotexString',
 'DEFINITIONS',
 'INSTANCE',
 'REAL',
 'VisibleString',
 'DURATION',
 'INSTRUCTIONS',
 'RELATIVE-OID',
 'WITH',
 'EMBEDDED',
 'INTEGER',
 'RELATIVE-OID-IRI']


'''
Rec. ITU-T X.680 (08/2015)
Table 2 - ASN.1 characters
Page 15
'''
A_to_Z_latin = ascii_uppercase
a_to_z_latin = ascii_lowercase
digits = digits
exclamation_mark = '!'
quotation_mark = '"'
ampersand = '&'
apostrophe = "'"
left_parenthesis = '('
right_parenthesis = ')'
asterisk = '*'
comma = ','
hyphen_minus = '-'
full_stop = '.'
solidus = '/'
colon = ':'
semicolon = ';'
less_than_sign = '<'
equals_sign = '='
greater_than_sign = '>'
commercial_at = '@'
left_square_bracket = '['
right_square_bracket = ']'
circumflex_accent = '^'
low_line = '_'
left_curly_bracket = '{'
vertical_line = '|'
right_curly_bracket = '}'
non_breaking_hyphen = chr(8211)

allowed_character_set = A_to_Z_latin + \
                        a_to_z_latin + \
                        digits + \
                        exclamation_mark + \
                        quotation_mark + \
                        ampersand + \
                        apostrophe + \
                        left_parenthesis + \
                        right_parenthesis + \
                        asterisk + \
                        comma + \
                        hyphen_minus + \
                        full_stop + \
                        solidus + \
                        colon + \
                        semicolon + \
                        less_than_sign + \
                        equals_sign + \
                        greater_than_sign + \
                        commercial_at + \
                        left_square_bracket + \
                        right_square_bracket + \
                        circumflex_accent + \
                        low_line + \
                        left_curly_bracket + \
                        vertical_line + \
                        right_curly_bracket + \
                        non_breaking_hyphen

'''
Rec. ITU-T X.680 (08/2015)
12.1.6
Page 16/17
'''
horizontal_tabulation = '\t'
line_feed = '\n'
vertical_tabulation = chr(11)
form_feed = chr(12)
carriage_return = '\r'
space = ' '
no_break_space = chr(255)

white_space = oneOf(horizontal_tabulation + \
                    line_feed + \
                    vertical_tabulation + \
                    form_feed + \
                    carriage_return + \
                    space + \
                    no_break_space
                    )

newline = oneOf(line_feed + \
                vertical_tabulation + \
                form_feed + \
                carriage_return
                )
