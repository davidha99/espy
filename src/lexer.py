import ply.lex as lex

'''
    Lexer.py
    Descripción: Clase que define las reglas léxicas del lenguaje. Extensión de ply.lex
    Autores: David Hernández    |   A01383543
             Bernardo García    |   A00570682
'''

# Las palabras reservadas del lenguaje
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
    'let': 'LET',
    'var': 'VAR',
    'def' : 'DEF',
    'lambda': 'LAMBDA',
    'list': 'LIST'
}

# Carácteres literales del lenguaje, útliles para la definición sintáctica
literals = ['(', ')', '+', '-', '*', '/', '[', ']', '>', '<']

# Lista de tokens únicos que son definidos más adelante
tokens = ['ID', 'NUM', 'BOOLEAN', 'CHAR', 'NULL', 'LESSEQUAL', 'GREATEREQUAL', 'LESSTHAN', 'GREATERTHAN', 'EQUAL'] + list(reserved.values())

t_BOOLEAN = r'\#t | \#f'
t_CHAR = r'\\\#[a-zA-Z0-9]'
t_NULL = r'\(\)'
t_LESSTHAN = r'\<'
t_GREATERTHAN = r'\>'
t_EQUAL = r'\=\='
t_LESSEQUAL = r'\<\='
t_GREATEREQUAL = r'\>\='

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9<>\-\?]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUM(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Ignored characters
t_ignore = " \t"

# Manejo de errores léxicos
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Construcción del lexer
lexer = lex.lex()

# Función main para pruebas del lexer
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
    let
    [
    ]
    '''
    
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      
        print(tok)
