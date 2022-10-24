import ply.lex as lex

primitives = {
    'fxadd1' : 'PRIMITIVE'
}

tokens = ['ID', 'LPAREN', 'RPAREN', 'FIXNUM', 'BOOLEAN', 'CHAR', 'NULL'] + list(primitives.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_BOOLEAN = r'\#t | \#f'
t_CHAR = r'\\\#[a-zA-Z0-9]'
t_NULL = r'\(\)'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]* | [+-/*><=] | !='
    t.type = primitives.get(t.value,'ID')
    return t

def t_FIXNUM(t):
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
    data = "fxadd1"

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)