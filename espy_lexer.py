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
    'display': 'DISPLAY'
}

tokens = ['ID', 'SQUOTE', 'UNDERSCORE', 'EQUALS', 'LPAREN', 'RPAREN',
          'LBRACK', 'RBRACK', 'LSQUAREBRACK', 'RSQUAREBRACK', 'GT', 'LT', 
          'NE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'CTEINT', 'CTEFLOAT', 
          'BANNER'] + list(reservadas.values())

# Tokens
t_SQUOTE = r'\''
t_UNDERSCORE = r'_'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\}'
t_RBRACK = r'\{'
t_LSQUAREBRACK = r'\['
t_RSQUAREBRACK = r'\]'
t_GT = r'>'
t_LT = r'<'
t_NE = r'!='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_BANNER = r'".*" | \'.*\''

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
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
    
        (define (fo+o)
            (+ (* 5.0 4.0) 2.0))
        
        (if (5 > 3))
        }

        (cond ((> 3 2) 'greater)
        ((< 3 2) 'less))

        (cond ((> 3 3) 'greater)
        ((< 3 3) 'less)
        (else 'equal))
        
        (if (> 3 2) 'yes 'no)
        
        (do ((vec (make-vector 5))
            (i 0 (+ i 1)))
            ((= i 5) vec)
        (vector-set! vec i i))
    
    )
    '''

    # Give the lexer the test data
    lexer.input(data)

    # Tokenize
    for tok in lexer:
        print(tok.type, tok.value, tok.lineno, tok.lexpos)
    

