import sys
import ply.yacc as yacc
from lexer import tokens
from literals import literal_repr
from emitter import emit_function_header, emit_literal, emit_function_footer, emit_stack_header
from primitives import if_consequent_expression, primitives
from utils import create_unique_if_labels, create_unique_func_labels

asm = ""
asm += emit_function_header("entry_point")
asm += emit_stack_header("entry_point")
asm += "L_entry_point:\n"
global_operand_stack = []
global_operator_stack = []
cond_label_stack = []
cond_label_counter = 1
func_label_stack = []
func_label_counter = 1
memory_stack_index = 0  # Start at byte 0


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
        cond_label_counter = 1
    p[0] = "Parsed"

def p_expr(p):
    '''
    expr : literal
         | unary_primitive
         | conditional_expr
         | arithmetic_primitive
         | comparison_primitive
         | definition
    '''

def p_literal(p):
    '''
    literal   : NUM
              | BOOLEAN
              | CHAR
              | NULL
              | ID
    '''
    global asm
    global global_operand_stack
    global memory_stack_index
    global_operand_stack.append(p[1])
    asm += emit_literal(global_operand_stack[-1])
    p[0] = p[1]

def p_unary_primitive(p):
    '''
    unary_primitive : '(' unary expr ')'
    '''
    global asm
    global global_operand_stack
    prim_name = p[2]
    prim_function = primitives[prim_name]
    temp, asm_temp = prim_function(global_operand_stack[-1])
    asm += asm_temp
    global_operand_stack.pop()
    global_operand_stack.append(temp)

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

def p_conditional_expr(p):
    '''
    conditional_expr : '(' IF np_create_if_labels test np_seen_test expr np_seen_consequent expr np_seen_alternate ')'
    '''
    # Pop labels of current if
    global cond_label_stack
    cond_label_stack.pop()
    cond_label_stack.pop()

#NP After IF lecture
def p_np_create_if_labels(p):
    "np_create_if_labels :"
    global cond_label_stack
    global cond_label_counter
    alt_label = create_unique_if_labels(cond_label_counter)
    cond_label_counter += 1
    end_label = create_unique_if_labels(cond_label_counter)
    cond_label_counter += 1
    cond_label_stack.append(alt_label)
    cond_label_stack.append(end_label)

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

def p_comparison_op(p):
    '''
    comparison_op : LESSEQUAL
                  | GREATEREQUAL
                  | LESSTHAN
                  | GREATERTHAN
                  | EQUAL
    '''
    p[0] = p[1]

#NP After IF conditional expression lecture
def p_np_seen_test(p):
    "np_seen_test :"
    global cond_label_stack
    global asm
    global global_operand_stack
    # Maybe take this from operands stack
    test = global_operand_stack[-1]
    global_operand_stack.pop()
    if_test_function = primitives["if_test"]
    asm += if_test_function(test, cond_label_stack)

#NP After IF first expression lecture
def p_np_seen_consequent(p):
    "np_seen_consequent :"
    global cond_label_stack
    global asm
    if_consequent_function = primitives["if_consequent"]
    asm += if_consequent_function(cond_label_stack)

#NP After IF alternate expression lecture
def p_np_seen_alternate(p):
    "np_seen_alternate :"
    global cond_label_stack
    global asm
    if_alternate_function = primitives["if_alternate"]
    asm += if_alternate_function(cond_label_stack)
def p_comparison_primitive(p):
    '''
    comparison_primitive : '(' np_compar_seen_paren comparison_op np_compar_seen_operator compar_operands ')'
    '''
    #NP End of comparison_primitive
    global asm
    global global_operator_stack
    global global_operand_stack
    global memory_stack_index

    global_operator_stack.pop()     # Pop the operator
    global_operator_stack.pop()     # Pop the operator flag ('(')
    global_operand_stack.pop(-2)    # Pop the operand flag ('(')
    asm += "\tmovl %s(%%esp), %%eax\n" % str(memory_stack_index)   # We must get the value from n-1(esp) to eax, so that we can continue working with it
    memory_stack_index += 4         # Reset the memory index to 0

#NP After parenthesis lecture
def p_np_compar_seen_paren(p):
    "np_compar_seen_paren :"
    global global_operator_stack
    global global_operand_stack
    global memory_stack_index
    global_operator_stack.append(p[-1])
    global_operand_stack.append(p[-1])
    memory_stack_index -= 4  

#NP After operator lecture
def p_np_compar_seen_operator(p):
    "np_compar_seen_operator :"
    global global_operator_stack
    global_operator_stack.append(p[-1])

def p_compar_operands(p):
    '''
    compar_operands : expr np_operands_seen_operand expr np_operands_seen_operand
    '''

def p_arithmetic_primitive(p):
    '''
    arithmetic_primitive : '(' np_arithm_seen_paren operator np_arithm_seen_operator operands ')'
    '''
    #NP End of arithmetic_primitive
    global asm
    global global_operator_stack
    global global_operand_stack
    global memory_stack_index

    global_operator_stack.pop()     # Pop the operator
    global_operator_stack.pop()     # Pop the operator flag ('(')
    global_operand_stack.pop(-2)        # Pop the operand flag ('(')
    asm += "\tmovl %s(%%esp), %%eax\n" % str(memory_stack_index)   # We must get the value from n-1(esp) to eax, so that we can continue working with it
    memory_stack_index += 4         # Reset the memory index to 0                                     # Update the asm stack index every time we close a \paren

#NP After parenthesis lecture
def p_np_arithm_seen_paren(p):
    "np_arithm_seen_paren :"
    global global_operator_stack
    global global_operand_stack
    global memory_stack_index
    global_operator_stack.append(p[-1])
    global_operand_stack.append(p[-1])
    memory_stack_index -= 4

#NP After operator lecture
def p_np_arithm_seen_operator(p):
    "np_arithm_seen_operator :"
    global global_operator_stack
    global_operator_stack.append(p[-1])

def p_operands(p):
    '''
    operands : expr np_operands_seen_operand expr np_operands_seen_operand more_expr
    '''

def p_more_expr(p):
    '''
    more_expr : more_expr expr np_operands_seen_operand
              | empty
    '''

#NP After operand lecture
def p_np_operands_seen_operand(p):
    "np_operands_seen_operand :"
    global asm
    global global_operator_stack
    global global_operand_stack
    global memory_stack_index

    #The first condition for the operand to be a literal representation is that there's a flag ('(') in the operand stack
    indv_operand = True if global_operand_stack[-2] == '(' else False

    op = global_operator_stack[-1]
    
    if op == '+':
        operation = primitives["addition"]
    elif op == '-':
        operation = primitives["substraction"]
    elif op == '*':
        operation = primitives["multiplication"]
    elif op == '/':
        operation = primitives["division"]
    elif op == 'and':
        operation = primitives["and"]
    elif op == 'or':
        operation = primitives["or"]
    elif op == '<=':
        operation = primitives["lessequal"]
    elif op == '>=':
        operation = primitives["greaterequal"]
    elif op == '==':
        operation = primitives["equal"]
    elif op == '<':
        operation = primitives["lessthan"]
    elif op == '>':
        operation = primitives["greaterthan"]
    

    #If is a indvidual operand, we just evaluate it as a literal value and move it to memory_stack_index(esp)
    if indv_operand:
        _, asm_temp = operation(memory_stack_index, tuple(global_operand_stack), indv_operand)
        asm += asm_temp
    else:
        temp, asm_temp = operation(memory_stack_index, tuple(global_operand_stack), indv_operand)
        asm += asm_temp
        global_operand_stack.pop()
        global_operand_stack.pop()
        global_operand_stack.append(temp)

def p_operator(p):
    '''
    operator : '+'
             | '-'
             | '*'
             | '/'
             | boolean_op
    '''
    p[0] = p[1]

def p_definition(p):
    '''
    definition : '(' DEFINE def_definition expr with_multiple_expr ')' 
    '''

#NP After IF lecture
def p_np_create_func_labels(p):
    "np_create_func_labels :"
    global func_label_stack
    global func_label_counter
    function_label = create_unique_func_labels(func_label_counter)
    func_label_counter += 1
    func_label_stack.append(function_label)

def p_def_definition(p):
    '''
    def_definition : '(' ID np_create_func_labels with_arguments ')'
    '''

def p_with_arguments(p):
    '''
    with_arguments : with_multiple_chars
    '''

def p_with_multiple_chars(p):
    '''
    with_multiple_chars : ID with_multiple_chars
                        | empty
    '''


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! - {}".format(p))


def p_empty(p):
    'empty :'
    pass


parser = yacc.yacc()

# For debugging parser just run while in this file
if __name__ == '__main__':

    data = "(define (sum x y) (+ 2 3))"

    print(parser.parse(data))
