import ply.lex as lex

reserved = {
    'add1': 'ADD1',
    'sub1': 'SUB1',
    'char->num': 'CHARTONUM',
    'num->char': 'NUMTOCHAR',
    'zero?': 'ISZERO',
    'null?': 'ISNULL',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'num?': 'ISNUM',
    'boolean?': 'ISBOOLEAN',
    'char?': 'ISCHAR',
    'if': 'IF', 
    'define': 'DEFINE'
}

literals = ['(', ')', '+', '-', '*', '/', '>', '<']

tokens = ['ID', 'NUM', 'BOOLEAN', 'CHAR', 'NULL', 'LESSEQUAL', 'GREATEQUAL'] + list(reserved.values())

t_BOOLEAN = r'\#t | \#f'
t_CHAR = r'\\\#[a-zA-Z0-9]'
t_NULL = r'\(\)'
t_LESSEQUAL = r'\<\='
t_GREATEQUAL = r'\>\='


def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9<>\-\?]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUM(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"

# Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# For debugging lexer just run while in this file
if __name__ == "__main__":
    data = '''
    char->num
    num->char
    boolean?
    null?
    char?
    num?
    zero?
    not
    or
    and
    (if (> 2 1))
    *
    /
    +
    -
    '''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
