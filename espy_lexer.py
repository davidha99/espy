# ESPY lexer

import ply.lex as lex

# palabras reservadas
reservadas = {
    'main' : 'MAIN',
    'define' : 'DEFINE',
    'set' : 'SET',
    'if' : 'IF',
    'cond' : 'COND',
    'else' : 'ELSE',
    'do' : 'DO',
    'quote' : 'QUOTE',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'display': 'DISPLAY',
    'lambda' : 'LAMBDA'
}

tokens = ['ID', 'SQUOTE', 'LPAREN', 'RPAREN', 'BOOLEAN', 'CTEINT', 
          'CTEFLOAT', 'CHAR', 'BANNER', 'COMMENT'] + list(reservadas.values())

# Tokens
t_SQUOTE = r'\'.*\n'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_BANNER = r'".*"'
t_CHAR = r'\'[a-zA-Z]\''

def t_BOOLEAN(t):
    r'true | false'
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]* | [+-/*><=] | !='
    t.type = reservadas.get(t.value,'ID')
    return t

def t_CTEFLOAT(t):
    r'[+-]?[0-9]*\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTEINT(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'%.*\n'
    pass

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

if __name__ == "__main__":
    # Test data
    data = '''
    (main 
        % Ignorar este mensaje
        !=
        >
        <
        +
        -
        /
        *
        (and true false)
        (+ 1 2 3 4.5)
        (display x)
        '(+ 1 2)
    )
    '''

    # Give the lexer the test data
    lexer.input(data)

    # Tokenize
    for tok in lexer:
        print(tok.type, tok.value, tok.lineno, tok.lexpos)
    

