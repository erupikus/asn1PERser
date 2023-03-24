from pyparsing import oneOf, Word, ZeroOrMore, Regex, Literal, Empty
from .character_and_word_set import A_to_Z_latin, a_to_z_latin, \
    digits, hyphen_minus, non_breaking_hyphen, allowed_character_set, newline


'''
Rec. ITU-T X.680 (08/2015)
12.2 Type references
Page 17
'''
typereference = Word(A_to_Z_latin,
                     A_to_Z_latin + a_to_z_latin + digits +
                     hyphen_minus + non_breaking_hyphen)


'''
Rec. ITU-T X.680 (08/2015)
12.3 Identifiers
Page 17
'''
identifier = Word(a_to_z_latin,
                  a_to_z_latin + A_to_Z_latin + digits + hyphen_minus+ non_breaking_hyphen)


'''
Rec. ITU-T X.680 (08/2015)
12.4 Value references
Page 17
'''
valuereference = identifier

'''
Rec. ITU-T X.680 (08/2015)
12.5 Module references
Page 17
'''
modulereference = typereference


'''
Rec. ITU-T X.680 (08/2015)
12.6 Comments
Page 17
'''
# Missing comment for '/*' and '*/'
comment = hyphen_minus + \
          hyphen_minus + \
          ZeroOrMore(Word(allowed_character_set, allowed_character_set)) + \
          oneOf(hyphen_minus+ \
                hyphen_minus,
                newline)

'''
Rec. ITU-T X.680 (08/2015)
12.7 Empty lexical item
Page 18
'''
empty = Empty().suppress()

'''
Rec. ITU-T X.680 (08/2015)
12.8 Numbers
Page 18
'''
# number = Word(digits.replace('0', ''), digits, min=2) | \
#          Word(digits, max=1)
number = Regex(r'\d+')

'''
Rec. ITU-T X.680 (08/2015)
12.9 Real numbers
Page 18
'''
# This is a poor reflection of its definition but for time being will be enough
# realnumber = Word(digits, '.' + digits+ 'eE-')
realnumber = Regex(r'\d+\.\d+')

'''
Rec. ITU-T X.680 (08/2015)
12.10 Binary strings
Page 18
'''
# This is a poor reflection of its definition but for time being will be enough
# bstring = Word("'", "01B'")
bstring = Regex(r"\'[01\s]*\'B")


'''
Rec. ITU-T X.680 (08/2015)
12.12 Hexadecimal strings
Page 18/19
'''
# This is a poor reflection of its definition but for time being will be enough
# hstring = Word("'", digits + "ABCDEF'H")
hstring = Regex(r"\'[A-F0-9\s]*\'H")


'''
Rec. ITU-T X.680 (08/2015)
12.14 Character strings
Page 19
'''
# This is a poor reflection of its definition but for time being will be enough
# cstring = Word('"', digits + A_to_Z_latin + a_to_z_latin + '"')
cstring = Regex(r'\"[0-9A-Za-z\s]*\"')


'''
Rec. ITU-T X.680 (08/2015)
12.16 The simple character string lexical item
Page 22
'''
# This is a poor reflection of its definition but for time being will be enough
simplestring = cstring


'''
Rec. ITU-T X.680 (08/2015)
12.17 Time value character strings
Page 22
'''
tstring = Word('"', '0123456789+-:.,/CDHMRPSTWYZ"')


'''
Rec. ITU-T X.680 (08/2015)
12.19 The property and setting names lexical item
Page 22
'''
psname = simplestring


'''
Rec. ITU-T X.680 (08/2015)
12.20 Assignment lexical item
Page 22
'''
assignment = Literal('::=')


'''
Rec. ITU-T X.680 (08/2015)
12.21 Range separator
Page 22
'''
rangeseparator = Literal('..')


'''
Rec. ITU-T X.680 (08/2015)
12.22 Ellipsis
Page 22
'''
ellipsis = Literal('...')


'''
Rec. ITU-T X.680 (08/2015)
12.23 Left version brackets
Page 23
'''
leftversionbrackets = Literal('[[')


'''
Rec. ITU-T X.680 (08/2015)
12.24 Right version brackets
Page 23
'''
rightversionbrackets = Literal(']]')


'''
Rec. ITU-T X.680 (08/2015)
12.25 Encoding references
Page 23
'''
encodingreference = Word(A_to_Z_latin,
                    A_to_Z_latin + hyphen_minus+ non_breaking_hyphen)


# 12.37 Single character lexical items
LEFT_CURLY_BRACKET = Literal('{').suppress()
RIGHT_CURLY_BRACKET = Literal('}').suppress()
LESS_THAN_SIGN = Literal('<')
GREATER_THAN_SIGN = Literal('>')
COMMA = Literal(',').suppress()
FULL_STOP = Literal('.')
SOLIDUS = Literal('/')
LEFT_PARENTHESIS = Literal('(').suppress()
RIGHT_PARENTHESIS = Literal(')').suppress()
LEFT_SQUARE_BRACKET = Literal('[')
RIGHT_SQUARE_BRACKET = Literal(']')
HYPHEN_MINUS = Literal('-')
COLON = Literal(':')
EQUALS_SIGN = Literal('=')
QUOTATION_MARK = Literal('"')
APOSTROPHE = Literal("'")
SPACE = Literal(' ')
SEMICOLON = Literal(';')
COMMERCIAL_AT = Literal('@')
VERTICAL_LINE = Literal('|')
EXCLAMATION_MARK = Literal('!')
CIRCUMFLEX_ACCENT = Literal('^')


if __name__ == '__main__':
    s = "000'B"
    print(bstring.parseString(s, parseAll=True))