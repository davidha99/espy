import sys
import ply.yacc as yacc
from lexer import tokens
from literals import literal_repr
from emitter import emit_function_header, emit_literal, emit_function_footer, emit_stack_header
from primitives import if_consequent_expression, primitives
from utils import create_unique_label

asm = ""
asm += emit_function_header("entry_point")
asm += emit_stack_header("entry_point")
asm += "L_entry_point:\n"
operand_stack = []
operator_stack = []
label_stack = []
label_counter = 1
stack_index = 0  # Start at byte 0


def p_program(p):
    '''
    program : expr
    '''
    global asm
    with open("espy.s", "w") as f:
        asm += emit_function_footer()
        f.write(asm)
        # Resetea el Assembly Code y el counter (esto para que se ejecuten correctamente los tests)
        asm = emit_function_header("entry_point")
        asm += emit_stack_header("entry_point")
        asm += "L_entry_point:\n"
        label_counter = 1
    p[0] = "Parsed"


def p_expr(p):
    '''
    expr : literal
         | unary_primitive
         | conditional_expr
         | arithmetic_primitive
    '''


def p_literal(p):
    '''
    literal   : NUM
              | BOOLEAN
              | CHAR
              | NULL
    '''
    global asm
    global operand_stack
    global stack_index
    operand_stack.append(p[1])
    asm += emit_literal(operand_stack[-1])
    p[0] = p[1]


def p_unary_primitive(p):
    '''
    unary_primitive : '(' unary expr ')'
    '''
    global asm
    global operand_stack
    prim_name = p[2]
    prim_function = primitives[prim_name]
    temp, asm_temp = prim_function(operand_stack[-1])
    asm += asm_temp
    operand_stack.pop()
    operand_stack.append(temp)


def p_unary(p):
    '''
    unary : ADD1
          | SUB1
          | CHARTONUM
          | NUMTOCHAR
          | ISZERO
          | ISNULL
          | NOT
          | ISNUM
          | ISBOOLEAN
          | ISCHAR
    '''
    p[0] = p[1]

# (if <test> <consequent> <alternate>)


def p_conditional_expr(p):
    '''
    conditional_expr : '(' IF create_if_labels test seen_test expr seen_consequent expr seen_alternate ')'
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
    test : '(' boolean_op expr expr with_multiple_expr ')'
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
    global operand_stack
    # Maybe take this from operands stack
    test = operand_stack[-1]
    operand_stack.pop()
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


def p_arithmetic_primitive(p):
    '''
    arithmetic_primitive : '(' seen_paren operator seen_operator operands ')'
    '''
    global asm
    global operator_stack
    global operand_stack
    global stack_index

    operator_stack.pop()
    operator_stack.pop()
    asm += "\tmovl %s(%%esp), %%eax\n" % str(stack_index)   # We must get the value from n-1(esp) to eax, so that we can continue working with it
    stack_index += 4                                        # Update the asm stack index every time we close a \paren

    # operand_stack.pop()

def p_seen_paren(p):
    "seen_paren :"
    global operator_stack
    global stack_index
    operator_stack.append(p[-1])
    stack_index -= 4

# def p_remove_paren(p):
#     "remove_paren :"
#     global operator_stack
#     global stack_index
#     # operator_stack.pop()

def p_seen_operator(p):
    "seen_operator :"
    global operator_stack
    operator_stack.append(p[-1])

def p_operands(p):
    '''
    operands : expr seen_operand expr seen_operand more_expr
    '''

def p_more_expr(p):
    '''
    more_expr : more_expr expr seen_operand
              | empty
    '''

def p_seen_operand(p):
    "seen_operand :"
    global asm
    global operator_stack
    global operand_stack
    global stack_index

    indv_operand = False

    n_operands = len(operand_stack)
    n_operators = len(operator_stack)
    
    #The first condition for the operand to be a literal representation is that the n_operands and n_operators are in a relation 2:1
    indv_condition_index_1 = n_operands/(n_operators/2)
    #The second condition for the operand to be a literal representation is a nested operation, which will be related by the stack level and n_operators
    indv_condition_index_2 = (-1 * stack_index / n_operators)

    if(indv_condition_index_1 == 1 or (n_operands == indv_condition_index_2 and n_operators > 2)):
        indv_operand = True

    op = operator_stack[-1]
    
    if op == '+':
        operation = primitives["addition"]
    elif op == '-':
        operation = primitives["substraction"]
    elif op == '*':
        operation = primitives["multiplication"]
    elif op == '/':
        operation = primitives["division"]

    #If is a indvidual operand, we just evaluate it as a literal value and move it to stack_index(esp)
    if indv_operand:
        _, asm_temp = operation(stack_index, tuple(operand_stack), indv_operand)
        asm += asm_temp
    else:
        temp, asm_temp = operation(stack_index, tuple(operand_stack), indv_operand)
        asm += asm_temp
        operand_stack.pop()
        operand_stack.pop()
        operand_stack.append(temp)

def p_operator(p):
    '''
    operator : '+'
             | '-'
             | '*'
             | '/'
             | boolean_op
    '''
    p[0] = p[1]

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
