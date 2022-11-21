import sys
import ply.yacc as yacc
from lexer import tokens
from literals import literal_repr

from emitter import (
    emit_function_header, 
    emit_literal,
    emit_function_footer, 
    emit_stack_header 
    )

from primitives import (
    if_consequent_expression, 
    primitives
    )

from utils import (
    create_unique_if_labels, 
    create_unique_func_labels, 
    save_in_memory,
    load_from_memory,
    typeof
    )

from environment import Environment_Stack, Environment, Global_Environment
from errors import EspyNameError, InvalidArgumentNumber
# import compiler

TEMP_DIR = -1000

asm = ""
asm += emit_function_header("entry_point")
asm += emit_stack_header("entry_point")
asm += "L_entry_point:\n"
asm_functions = []
environment = {}
global_operand_stack = []
global_operator_stack = []
cond_label_stack = []
cond_label_counter = 1
func_label_stack = []
func_label_counter = 1
memory_stack_index = 0  # Start at byte 0
environment_stack = Environment_Stack()
var_binding_stack = []
func_binding_stack = []
scope_counter = 0
func_call_stack = []
pointer_offset = 0
# param_queue = []
# evaluated_args = 0

def p_program(p):
    '''
    program : np_gbl_scope expr
            | np_gbl_scope '(' LETREC np_seen_letrec func_binding_list expr ')'
    '''
    global asm
    global global_operand_stack
    with open("espy.s", "w") as f:
        asm += emit_function_footer()
        if len(asm_functions) > 0:
            for func in asm_functions:
                asm += func
        f.write(asm)
        # Resetea el Assembly Code y el counter (esto para que se ejecuten correctamente los tests)
        asm = emit_function_header("entry_point")
        asm += emit_stack_header("entry_point")
        asm += "L_entry_point:\n"
        cond_label_counter = 1
    Global_Environment.set_instance(environment_stack.scope_pop())
    # environment_stack.scope_exit()  # Erase Global scope

    p[0] = "Parsed"

def p_np_gbl_scope(p):
    "np_gbl_scope :"
    global environment_stack
    global scope_counter
    global_env = Global_Environment.get_instance()
    # environment_stack.scope_enter(scope_counter)    # Global scope
    environment_stack.insert_environment(global_env)
    scope_counter += 1

def p_np_seen_letrec(p):
    "np_seen_letrec :"
    global environment_stack
    global memory_stack_index
    environment_stack.scope_enter(scope_counter)
    memory_stack_index -= 4

def p_func_binding_list(p):
    '''
    func_binding_list : '(' with_multiple_func_bindings ')'
                      | NULL
    '''

def p_with_multiple_func_bindings(p):
    '''
    with_multiple_func_bindings : '[' ID np_seen_func_name lambda ']' np_close_func_binding with_multiple_func_bindings
                                | '[' ID np_seen_func_name lambda ']' np_close_func_binding
    '''

#NP after function lecture
def p_np_seen_func_name(p):
    "np_seen_func_name :"
    global func_label_stack
    global func_label_counter
    global environment_stack
    global var_binding_stack
    global asm
    # Create a new label for the function
    function_label = create_unique_func_labels(func_label_counter)
    func_label_counter += 1
    func_label_stack.append(function_label)
    # Bind the function name into the current environment
    func_name = p[-1]
    environment_stack.function_bind(func_name, function_label)
    # Push the function name to the binding stack (for the parameters)
    func_binding_stack.append(func_name)
    # Start assembly for the function
    asm += function_label + ":\n"

def p_np_close_func_binding(p):
    "np_close_func_binding :"
    global asm
    global asm_functions
    global func_binding_stack
    global environment_stack
    global global_operand_stack
    func_name = func_binding_stack.pop()
    symbol = environment_stack.scope_func_lookup(func_name)
    indx = asm.find(symbol.label)
    func_asm = asm[indx:]
    asm = asm[:indx]
    func_asm += emit_function_footer()
    asm_functions.append(func_asm)
    global_operand_stack.clear()
    

def p_lambda(p):
    '''
    lambda : '(' LAMBDA '(' with_multiple_params ')' expr ')'
           | '(' LAMBDA NULL expr ')'
    '''

# def p_np_seen_lambda(p):
#     "np_seen_lambda :"
#     global memory_stack_index
#     memory_stack_index -= 4

def p_with_multiple_params(p):
    '''
    with_multiple_params : with_multiple_params ID np_seen_param
                         | ID np_seen_param
    '''
    global pointer_offset
    pointer_offset = -4 * (environment_stack.get_len_all_parameters())

def p_np_seen_param(p):
    "np_seen_param :"
    global environment_stack
    global memory_stack_index
    global var_binding_stack

    # Add parameter to the corresponding function
    func_name = func_binding_stack[-1]
    param_name = p[-1]
    environment_stack.parameter_bind(
        func_name=func_name, 
        param_name=param_name, 
        memory_idx=memory_stack_index
        )
    
    # Add parameter to the queue (this is to maintain the order when evaluating 
    # the expressions corresponding to the parameters)
    # param_queue.append(param_name)

    # Update memory index
    memory_stack_index -= 4

def p_expr(p):
    '''
    expr : literal
         | variable
         | unary_primitive
         | conditional_expr
         | arithmetic_primitive
         | comparison_primitive
         | let_binding
         | global_var_declaration
         | function_call
    '''
    p[0] = p[1]

def p_literal(p):
    '''
    literal   : NUM
              | BOOLEAN
              | CHAR
              | NULL
    '''
    global asm
    global global_operand_stack
    global_operand_stack.append(p[1])
    asm += emit_literal(global_operand_stack[-1])
    p[0] = p[1]

def p_variable(p):
    '''
    variable : ID
    '''
    global global_operand_stack
    global environment_stack
    global asm
    var = p[1]

    # Check if variable is in the environment
    # .scope_lookup() returns all information of the variable (the symbol)
    symbol = environment_stack.scope_lookup(var)

    # If it is, push the value of the variable to the operand stack
    if symbol is not None:
        # global_operand_stack.append(symbol.value)
        global_operand_stack.append(var)
        # asm += emit_literal(symbol.value) # TODO: load_from_memory instead of literal
        asm += load_from_memory(symbol.memory_idx)
    else:
        mem_idx = environment_stack.func_lookup_param(func_binding_stack[-1], var)[0]
        if mem_idx is not None:
            # Get memory index of the variable and load it to the register
            global_operand_stack.append(var)
            asm += load_from_memory(str(mem_idx))
        else:
            raise EspyNameError("Variable '%s' is not defined" % var)

    
    p[0] = p[1]

def p_global_var_declaration(p):
    '''
    global_var_declaration : '(' VAR '[' np_let_seen_bracket ID np_seen_variable expr np_seen_var_expr ']' ')'
    '''
    global environment_stack
    global asm
    var = p[5]
    symbol = environment_stack.scope_lookup(var)
    asm += save_in_memory(symbol.memory_idx)

def p_unary_primitive(p):
    '''
    unary_primitive : '(' unary expr ')'
    '''
    global asm
    global global_operand_stack
    global memory_stack_index
    global environment_stack
    prim_name = p[2]
    prim_function = primitives[prim_name]
    operand = global_operand_stack[-1]

    # Check if yielding of expression is a variable or a literal
    if typeof(operand) == "variable":
        # Check if it is a variable in the current scope
        symbol = environment_stack.scope_lookup(operand)
        if symbol is None:
            # Check if it is a parameter of the current function
            param = environment_stack.func_lookup_param(func_binding_stack[-1], operand)[1]
            temp, asm_temp = prim_function(param)
        else:
            temp, asm_temp = prim_function(symbol.value)
    else:
        temp, asm_temp = prim_function(operand)

    asm += asm_temp
    global_operand_stack.pop()
    global_operand_stack.append(temp)

    p[0] = temp

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
    asm += "\tmovl %s(%%esp), %%eax\n" % str(memory_stack_index + TEMP_DIR)   # We must get the value from n-1(esp) to eax, so that we can continue working with it
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
    asm += "\tmovl %s(%%esp), %%eax\n" % str(memory_stack_index + TEMP_DIR)   # We must get the value from n-1(esp) to eax, so that we can continue working with it
    memory_stack_index += 4         # Update the asm stack index every time we close a \paren

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
        _, asm_temp = operation(
            memory_stack_index, 
            tuple(global_operand_stack), 
            indv_operand)
        asm += asm_temp
    else:
        temp, asm_temp = operation(
            memory_stack_index, 
            tuple(global_operand_stack), 
            indv_operand)
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

# def p_definition(p):
#     '''
#     definition : '(' DEFINE def_definition expr with_multiple_expr ')' 
#     '''

# def p_def_definition(p):
#     '''
#     def_definition : '(' ID np_seen_func_name with_arguments ')'
#     '''

# def p_with_arguments(p):
#     '''
#     with_arguments : with_multiple_chars
#     '''

# def p_with_multiple_chars(p):
#     '''
#     with_multiple_chars : ID with_multiple_chars
#                         | empty
#     '''

def p_let_binding(p):
    '''
    let_binding : '(' LET np_seen_let binding_list expr ')'
    '''
    global environment_stack
    global memory_stack_index
    global scope_counter
    memory_stack_index = 0
    environment_stack.scope_exit()
    scope_counter -= 1

#NP After LET lecture
def p_np_seen_let(p):
    "np_seen_let :"
    global environment_stack
    global scope_counter
    environment_stack.scope_enter(scope_counter)
    scope_counter += 1

def p_binding_list(p):
    '''
    binding_list : '(' with_multiple_bindings ')'
    '''
    
def p_with_multiple_bindings(p):
    '''
    with_multiple_bindings : with_multiple_bindings '[' np_let_seen_bracket ID np_seen_variable expr np_seen_var_expr ']'
                           | '[' np_let_seen_bracket ID np_seen_variable expr np_seen_var_expr ']'
    '''
    global environment_stack
    global asm
    if len(p) == 8:
        var = p[3]
    else:
        var = p[4]
    symbol = environment_stack.scope_lookup(var)
    asm += save_in_memory(symbol.memory_idx)

#NP After expression lecture in let binding
def p_np_seen_var_expr(p):
    "np_seen_var_expr :"
    global global_operand_stack
    global environment_stack
    global var_binding_stack
    global asm
    var = var_binding_stack.pop()       # Variable's name has been saved before to update its value in Environment stack
    symbol = environment_stack.scope_lookup_current(var)
    symbol.value = global_operand_stack.pop()

    # Save result in the memory
    asm += save_in_memory(symbol.memory_idx)

#NP After '[' lecture inside let_binding
def p_np_let_seen_bracket(p):
    "np_let_seen_bracket :"
    global memory_stack_index
    memory_stack_index -= 4

def p_np_seen_variable(p):
    "np_seen_variable :"
    global environment_stack
    global memory_stack_index
    global var_binding_stack
    variable = p[-1]        
    var_binding_stack.append(variable)    #  Save variable name to later update its value
    environment_stack.scope_bind(
        name=variable, 
        memory_idx=memory_stack_index
        )

# Function call stack
# [[funcname, num_args, evaluated_args, param_queue], [], ...]

def p_function_call(p):
    '''
    function_call : '(' function_name function_arguments ')'
    '''
    # global evaluated_args
    # global param_queue
    global environment_stack
    global func_call_stack
    global asm
    global global_operand_stack
    global pointer_offset

    topmost_function = func_call_stack[-1]
    func_name = topmost_function[0]
    n_params = topmost_function[1]
    evaluated_args = topmost_function[2]

    # Check if number of arguments isn´t less than the number of parameters
    if evaluated_args != n_params:
        raise InvalidArgumentNumber("Invalid number of arguments")

    # pointer_offset = -4 * (environment_stack.get_all_parameters())
    func_label = environment_stack.scope_func_lookup(func_name).label
    pointer_mov = (pointer_offset * len(func_call_stack) - (len(func_call_stack) - 1) * 4)
    asm += "\taddl $%s, %%esp\n" % pointer_mov
    asm += "\tcall %s\n" % func_label
    t_pointer_offset = -1 * pointer_mov
    asm += "\taddl $%s, %%esp\n" % t_pointer_offset
    global_operand_stack.append(func_name)
    # Pop the function from the call stack
    func_call_stack.pop()

def p_function_name(p):
    '''
    function_name : ID
    '''
    global environment_stack
    global func_call_stack
    # global evaluated_args
    # global param_queue
    
    # Check if function name is defined
    func_name = p[1]
    symbol = environment_stack.scope_func_lookup(func_name)
    if symbol is None:
        raise EspyNameError(f"Function '{func_name}' is not defined")
    
    # Add function to function call stack
    # func_call_stack.append(func_name)

    # Get the paramters of the function
    try:
        parameters = environment_stack.scope_func_lookup(func_name).params.parameters
        # Reset param queue and evaluated args counter
        param_queue = list(parameters.keys()) # May be append? because (f f(x))
        evaluated_args = 0
    except:
        parameters = {}
        param_queue = []
        evaluated_args = 0
    
    # Add functions information to function call stack
    func_call_stack.append([func_name, len(parameters), evaluated_args, param_queue])

    

def p_function_arguments(p):
    '''
    function_arguments : empty
                       | with_multiple_args
    '''
    p[0] = p[1]

def p_with_multiple_args(p):
    '''
    with_multiple_args : with_multiple_args expr
                       | expr
    '''
    global global_operand_stack
    global environment_stack
    # global param_queue
    # global evaluated_args
    global func_call_stack
    global memory_stack_index
    global asm

    topmost_func = func_call_stack[-1]

    # Get function info for which we are evaluating arguments
    func_name = topmost_func[0]
    # n_params = topmost_func[1]
    evaluated_args = topmost_func[2]
    param_queue = topmost_func[3]

    # Check if number of arguments isnt greater than the number of parameters
    # if evaluated_args >= len(param_queue):
    #     raise InvalidArgumentNumber("Invalid number of arguments")

    # Get parameter name for which we are evaluating argument
    param_name = param_queue[evaluated_args]
    
    # Update the evaluated arguments counter of the current function
    evaluated_args += 1
    func_call_stack[-1][2] = evaluated_args

    # Get symbol for parameter
    func_params = environment_stack.scope_func_lookup(func_name).params

    # Set parameter value
    func_params.set_parameter_value(param_name, global_operand_stack[-1])

    # Generate asm instructions for function call
    # mem_idx = environment_stack.func_lookup_param(func_name, param_name)
    # offset_idx =  mem_idx - 4 *(len(func_params) + 1)
    # total_evaluated_args = 0
    # for x in func_call_stack:
    #     if x[2] > 0:
    #         total_evaluated_args += x[2]
    where = func_params.parameters[param_name][0] + ((pointer_offset - 4) * len(func_call_stack))
    asm += save_in_memory(where)
    # memory_stack_index -= 4
    # asm += "\tmovl %s(%%esp), %s(%%esp)\n" % mem_idx
    p[0] = global_operand_stack[-1]



# def p_np_seen_arg_expr(p):
#     "np_seen_arg_expr :"


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
