import sys
import ply.yacc as yacc
from lexer import tokens
from emitter import emit_program

def p_program(p):
    '''
    program : expr
    '''
    # p[0] = p[1]
    with open("scheme.s", "w") as f:
        f.write(emit_program(p[1]))

def p_expr(p):
    '''
    expr : immediate
    '''
    p[0] = p[1]

def p_immediate(p):
    '''
    immediate : FIXNUM
              | BOOLEAN
              | CHAR
              | NULL
    '''
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! - {}".format(p))

parser = yacc.yacc()

# For debugging parser just run while in this file
if __name__ == '__main__':

    data = "32"

    print(parser.parse(data))