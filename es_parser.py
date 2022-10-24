import sys
import ply.yacc as yacc
from lexer import tokens
from immediates import immediate_repr
from emitter import emit_function_header, emit_immediate
from primitives import primitives

asm = ""
asm += emit_function_header("entry_point")
operands_stack = []

def p_program(p):
    '''
    program : expr
    '''
    global asm
    # p[0] = p[1]
    with open("scheme.s", "w") as f:
        asm += "    ret"
        f.write(asm)

def p_expr(p):
    '''
    expr : immediate
         | LPAREN unary_primitive expr RPAREN
    '''
    global asm
    global operands_stack
    if len(p) > 2:
        prim_name = p[2]
        prim_function = primitives[prim_name]
        temp, asm_temp = prim_function(operands_stack[-1])
        asm += asm_temp
        operands_stack.pop()
        operands_stack.append(temp)

def p_unary_primitive(p):
    '''
    unary_primitive : FXADD1
                    | FXSUB1
                    | CHARTOFIXNUM
                    | FIXNUMTOCHAR
                    | ISFXZERO
                    | ISNULL
                    | NOT
                    | ISFIXNUM
                    | ISBOOLEAN
                    | ISCHAR
    '''
    p[0] = p[1]


def p_immediate(p):
    '''
    immediate : FIXNUM
              | BOOLEAN
              | CHAR
              | NULL
    '''
    global asm
    global operands_stack
    operands_stack.append(p[1])
    asm += emit_immediate(operands_stack[-1])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! - {}".format(p))

parser = yacc.yacc()

# For debugging parser just run while in this file
if __name__ == '__main__':

    data = "1"

    print(parser.parse(data))