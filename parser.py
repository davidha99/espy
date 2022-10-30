import sys
import ply.yacc as yacc
from lexer import tokens
from immediates import immediate_repr
from emitter import emit_function_header, emit_immediate, emit_function_footer
from primitives import if_consequent_expression, primitives
from utils import create_unique_label

asm = ""
asm += emit_function_header("entry_point")
operands_stack = []
label_stack = []
label_counter = 1

def p_program(p):
    '''
    program : expr
    '''
    global asm
    with open("scheme.s", "w") as f:
        asm += emit_function_footer()
        f.write(asm)
        # Resetea el Assembly Code (esto para que se ejecuten correctamente los tests)
        asm = emit_function_header("entry_point")
    p[0] = "Parsed"

def p_expr(p):
    '''
    expr : immediate
         | unary_primitive
         | conditional_expr
    '''

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

def p_unary_primitive(p):
    '''
    unary_primitive : LPAREN unary expr RPAREN
    '''
    global asm
    global operands_stack
    prim_name = p[2]
    prim_function = primitives[prim_name]
    temp, asm_temp = prim_function(operands_stack[-1])
    asm += asm_temp
    operands_stack.pop()
    operands_stack.append(temp)

def p_unary(p):
    '''
    unary : FXADD1
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

# (if <test> <consequent> <alternate>)
def p_conditional_expr(p):
    '''
    conditional_expr : LPAREN IF create_if_labels test seen_test expr seen_consequent expr seen_alternate RPAREN
    '''
    # Pop labels of current if
    global label_stack
    label_stack.pop()
    label_stack.pop()

def p_create_if_labels(p):
    "create_if_labels :"
    global label_stack
    global label_counter
    alt_label = create_unique_label(label_counter)
    label_counter += 1
    end_label = create_unique_label(label_counter)
    label_counter += 1
    label_stack.append(alt_label)
    label_stack.append(end_label)

def p_test(p):
    '''
    test : LPAREN boolean_op expr expr with_multiple_expr RPAREN
         | expr
    '''

def p_with_multiple_expr(p):
    '''
    with_multiple_expr : with_multiple_expr expr
                       | empty
    '''

def p_boolean_op(p):
    '''
    boolean_op : AND
               | OR
    '''
    p[0] = p[1]

def p_seen_test(p):
    "seen_test :"
    global label_stack
    global asm
    global operands_stack
    # Maybe take this from operands stack
    test = operands_stack[-1]
    operands_stack.pop()
    if_test_function = primitives["if_test"]
    asm += if_test_function(test, label_stack)

def p_seen_consequent(p):
    "seen_consequent :"
    global label_stack
    global asm
    if_consequent_function = primitives["if_consequent"]
    asm += if_consequent_function(label_stack)

def p_seen_alternate(p):
    "seen_alternate :"
    global label_stack
    global asm
    if_alternate_function = primitives["if_alternate"]
    asm += if_alternate_function(label_stack)

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! - {}".format(p))

def p_empty(p):
    'empty :'
    pass

parser = yacc.yacc()

# For debugging parser just run while in this file
if __name__ == '__main__':

    data = "3"

    print(parser.parse(data))