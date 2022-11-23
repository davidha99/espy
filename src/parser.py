import sys
import ply.yacc as yacc
from lexer import tokens
from literals import literal_repr
from environment import Environment_Stack, Environment, Global_Environment
from errors import EspyNameError, InvalidArgumentNumber

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
    typeof, 
    restore_glb_var_to_memory, 
    get_list_element_mem_idx
    )

'''
    Parser.py
    Descripción: Clase que define las reglas sintácticas del lenguaje. Extensión de ply.yacc
    Este archivo contiene la definición de la sintaxis y la semántica de espy, es el archivo más importante
    para la funcionalidad del programa.
    Autores: David Hernández    |   A01383543
             Bernardo García    |   A00570682
'''

# Dirección de memoria en ejecución de distintos tipos de estucturas y variables
# Las variables temporales se guardan a partir de la dirección 1000
TEMP_DIR = -1000
# Las variables declaradas se guardan a partir de la dirección 2000, independientemente de su tipo de dato
VAR_DIR = -2000
# Las variables dentro de una lista se guardan a partir de la dirección 3000, independientemente de su tipo de dato
LISTS_DIR = -3000

# Declaración de diferentes variables y estructuras globales usadas en el programa
environment_stack = Environment_Stack()     # Tipo stack de Environments (scopes). Principal estructura de memoria en 
environment = {}                            # Diccionario de Environments
global_operand_stack = []                   # Stack de operandos
global_operator_stack = []                  # Stack de operadores
var_binding_stack = []                      # Stack de variables: usado para la declaración de variables y listas
func_binding_stack = []                     # Stack de funciones: usado para la declaración de funciones
func_call_stack = []                        # Stack de funciones en proceso: usado para la recursión o el llamado de múltiples funciones
cond_label_stack = []                       # Stack de cond_labels
cond_label_counter = 1                      # Contador global de cond_labels
func_label_stack = []                       # Stack de cond_labels
func_label_counter = 1                      # Contador global de cond_labels
scope_counter = 0                           # Contador de contextos (scope): útil para múltiples operaciones en línea
pointer_offset = 0                          # Offset del pointer de la memoria de ejecución: usado para la llamada de funciones y variables
memory_stack_index = 0  # Start at byte 0   # Index del stack de memoria
memory_var_index = VAR_DIR                  # Index de variables declaradas empezará en esa dirección
memory_lists_index = LISTS_DIR              # Index de listas empezará en esa dirección
general_temp = None                         # Helper temporal

asm = ""                                    # Constructor string de las instrucciones de assembly
asm += emit_function_header("entry_point")
asm += emit_stack_header("entry_point")
asm += "L_entry_point:\n"
asm_functions = []                          # Stack de instrucciones de cada función

def p_program(p):
    '''
    program : np_gbl_scope expr
            | np_gbl_scope '(' DEF np_seen_def func_binding_list expr ')'
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

    p[0] = "Parsed"

def p_np_gbl_scope(p):
    "np_gbl_scope :"
    global environment_stack
    global scope_counter
    global asm
    global memory_var_index
    global memory_lists_index
    global_env = Global_Environment.get_instance()
    environment_stack.insert_environment(global_env)
    temp, memory_var_index, memory_stack_index = restore_glb_var_to_memory(global_env, memory_var_index, memory_lists_index)
    asm += temp
    scope_counter += 1

def p_np_seen_def(p):
    "np_seen_def :"
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

# Punto neurálgico: after function lecture
def p_np_seen_func_name(p):
    "np_seen_func_name :"
    global func_label_stack
    global func_label_counter
    global environment_stack
    global var_binding_stack
    global asm
    # Crear un nuevo label para la función
    function_label = create_unique_func_labels(func_label_counter)
    func_label_counter += 1
    func_label_stack.append(function_label)
    # Ingresar el nombre de la función en el Environment actual
    func_name = p[-1]
    environment_stack.function_bind(func_name, function_label)
    # Ingresar el nombre de la función al binding stack (para agregar después los parámetros)
    func_binding_stack.append(func_name)
    # Iniciar la redacción de las instrucciones de assembly para la función
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

    # Agregar el parámetro a la función correspondiente
    func_name = func_binding_stack[-1]
    param_name = p[-1]
    environment_stack.parameter_bind(
        func_name=func_name, 
        param_name=param_name, 
        memory_idx=memory_stack_index
        )

    # Actualizar el memory_index
    memory_stack_index -= 4

def p_expr(p):
    '''
    expr : literal
         | variable
         | list_variable
         | unary_primitive
         | conditional_expr
         | arithmetic_primitive
         | comparison_primitive
         | let_binding
         | function_call
         | list_declaration         
         | variable_declaration
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
    # Al hablar de variables hacemos referencia a variables declaradas, lo cuál sólo básicamentes es strings. Ejempli: suma = 10
    global global_operand_stack
    global environment_stack
    global asm
    var = p[1]

    # Revisar si la variable está en el stack de scopes
    symbol = environment_stack.scope_lookup(var)

    # Si existe, agregar su valor al stack de operandos
    if symbol is not None:
        global_operand_stack.append(var)
        asm += load_from_memory(symbol.memory_idx)
    else:
        # Si no existe, revisar si es una variable de una función
        mem_idx = environment_stack.func_lookup_param(func_binding_stack[-1], var)[0]
        if mem_idx is not None:
            # Si ya está declarada, agregar su valor al stack de operandos
            global_operand_stack.append(var)
            asm += load_from_memory(str(mem_idx))
        else:
            #Si no, la variable no existe
            raise EspyNameError("Variable '%s' is not defined" % var)

    
    p[0] = p[1]

def p_list_variable(p):
    '''
    list_variable : ID '[' expr ']'
    '''
    global asm
    global global_operand_stack
    global environment_stack
    var = p[1]
    index = p[3]
    symbol = environment_stack.scope_lookup(var)

    if symbol is not None:
        global_operand_stack.append(var)
        asm += load_from_memory(get_list_element_mem_idx(symbol, index))


def p_variable_declaration(p):
    '''
    variable_declaration : '(' VAR '[' np_seen_var_bracket ID np_seen_variable expr np_seen_var_expr ']' ')'
    '''
    global environment_stack
    global asm
    global var_binding_stack
    global memory_var_index
    global memory_stack_index
    global general_temp
    global global_operand_stack
    
    # Guardar el index de variables y actualizar el memory index a su valor anterior
    memory_var_index = memory_stack_index         
    memory_stack_index = general_temp               
    

def p_np_seen_var_bracket(p):
    "np_seen_var_bracket :"
    global memory_stack_index
    global global_operand_stack
    global memory_var_index
    global general_temp

    # Guardar el memory index para saber a donde regresar, y usar el index de declaracion de variables
    general_temp = memory_stack_index       
    memory_stack_index = memory_var_index   


def p_list_declaration(p):
    '''
    list_declaration : '(' LIST '[' np_seen_list_bracket ID np_seen_variable expr np_seen_list_expr with_multiple_list_expr ']' ')'
    '''
    global memory_lists_index
    global memory_stack_index
    global general_temp
    global global_operand_stack
    
    # Guardar el index de variables y actualizar el memory index a su valor anterior
    memory_lists_index = memory_stack_index         
    memory_stack_index = general_temp               

    var_binding_stack.pop()                         
    global_operand_stack.pop()                      # Pop fondo falso ('[')

    
    
def p_np_seen_list_bracket(p):
    "np_seen_list_bracket :"
    global memory_stack_index
    global global_operand_stack
    global memory_lists_index
    global general_temp
    
    # Guardar el memory index para saber a donde regresar, y usar el index de declaracion de variables
    general_temp = memory_stack_index       
    memory_stack_index = memory_lists_index
    global_operand_stack.append('[')      # Agregar un fondo falso para reconocer el scope


def p_np_seen_list_expr(p):
    "np_seen_list_expr :"
    global global_operand_stack
    global environment_stack
    global var_binding_stack
    global memory_stack_index
    global asm
    var = var_binding_stack[-1]       # Variable's name has been saved before to update its value in Environment stack
    symbol = environment_stack.scope_lookup_current(var)
    if symbol.value == None:      
        list_content = []
    else:
        list_content = symbol.value
    list_content.append(global_operand_stack.pop())     
    symbol.value = list_content                             # Update the Symbol content
    symbol.size = len(list_content)                         # Update the Symbol size
    asm += save_in_memory(memory_stack_index)               # Generate intel assembly instruction to move list value to its corresponding mem space
    memory_stack_index -= 4                                 # Update Memory index to next space available


def p_with_multiple_list_expr(p):
    '''
    with_multiple_list_expr : with_multiple_list_expr expr np_seen_list_expr
                       | empty
    '''
    

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
    # Pop de labels del IF actual
    global cond_label_stack
    cond_label_stack.pop()
    cond_label_stack.pop()

# Punto neurálgico: After IF lecture
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

# Punto neurálgico: After IF conditional expression lecture
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

# Punto neurálgico: After IF first expression lecture
def p_np_seen_consequent(p):
    "np_seen_consequent :"
    global cond_label_stack
    global asm
    if_consequent_function = primitives["if_consequent"]
    asm += if_consequent_function(cond_label_stack)

# Punto neurálgico: After IF alternate expression lecture
def p_np_seen_alternate(p):
    "np_seen_alternate :"
    global cond_label_stack
    global asm
    if_alternate_function = primitives["if_alternate"]
    asm += if_alternate_function(cond_label_stack)

# Punto neurálgico: End of comparison_primitive
def p_comparison_primitive(p):
    '''
    comparison_primitive : '(' np_compar_seen_paren comparison_op np_compar_seen_operator compar_operands ')'
    '''
    global asm
    global global_operator_stack
    global global_operand_stack
    global memory_stack_index

    global_operator_stack.pop()     # Pop the operator
    global_operator_stack.pop()     # Pop the operator flag ('(')
    global_operand_stack.pop(-2)    # Pop the operand flag ('(')
    asm += "\tmovl %s(%%esp), %%eax\n" % str(memory_stack_index + TEMP_DIR)   # We must get the value from n-1(esp) to eax, so that we can continue working with it
    memory_stack_index += 4         # Reset the memory index to 0

# Punto neurálgico: After parenthesis lecture
def p_np_compar_seen_paren(p):
    "np_compar_seen_paren :"
    global global_operator_stack
    global global_operand_stack
    global memory_stack_index
    global_operator_stack.append(p[-1])
    global_operand_stack.append(p[-1])
    memory_stack_index -= 4  

# Punto neurálgico: After operator lecture
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
    # Punto neurálgico: End of arithmetic_primitive
    global asm
    global global_operator_stack
    global global_operand_stack
    global memory_stack_index

    global_operator_stack.pop()     # Pop the operator
    global_operator_stack.pop()     # Pop the operator flag ('(')
    global_operand_stack.pop(-2)        # Pop the operand flag ('(')
    asm += "\tmovl %s(%%esp), %%eax\n" % str(memory_stack_index + TEMP_DIR)   # We must get the value from n-1(esp) to eax, so that we can continue working with it
    memory_stack_index += 4         # Update the asm stack index every time we close a \paren

# Punto neurálgico: After parenthesis lecture
def p_np_arithm_seen_paren(p):
    "np_arithm_seen_paren :"
    global global_operator_stack
    global global_operand_stack
    global memory_stack_index
    global_operator_stack.append(p[-1])
    global_operand_stack.append(p[-1])
    memory_stack_index -= 4

# Punto neurálgico: After operator lecture
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

# Punto neurálgico: After operand lecture
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

# Punto neurálgico: After LET lecture
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
    with_multiple_bindings : with_multiple_bindings '[' np_seen_bracket ID np_seen_variable expr np_seen_var_expr ']'
                           | '[' np_seen_bracket ID np_seen_variable expr np_seen_var_expr ']'
    '''
    global environment_stack
    global asm
    if len(p) == 8:
        var = p[3]
    else:
        var = p[4]
    symbol = environment_stack.scope_lookup(var)
    asm += save_in_memory(symbol.memory_idx)

# Punto neurálgico: After expression lecture in let binding
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

# Punto neurálgico: After '[' lecture inside let_binding
def p_np_seen_bracket(p):
    "np_seen_bracket :"
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
    where = func_params.parameters[param_name][0] + ((pointer_offset - 4) * len(func_call_stack))
    asm += save_in_memory(where)
    p[0] = global_operand_stack[-1]


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
