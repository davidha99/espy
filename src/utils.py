from errors import EspyTypeError, InvalidArgumentNumber, EspyNameError, EspyIndexOutOfBounds
from literals import is_boolean, is_char, is_null, is_num, literal_repr
from environment import Environment, Symbol

'''
Utils.py
Descripción: Archivo dedicado a la generación de funciones que son útiles a través de los diferentes
métodos a lo largo del proyecto
Autores: David Hernández    |   A01383543
         Bernardo García    |   A00570682
'''

# Función que revisa el número de argumentos recibidos en alguna otra función
def check_argument_number(function_name, given_arguments,
                          min_arguments, max_arguments=None):
    assert max_arguments is None or min_arguments <= max_arguments

    right_argument_number = True

    if len(given_arguments) < min_arguments:
        right_argument_number = False

    if max_arguments and len(given_arguments) > max_arguments:
        right_argument_number = False

    if not right_argument_number:
        if min_arguments == max_arguments:
            raise InvalidArgumentNumber("%s requires exactly %d argument(s), but "
                                   "received %d." % (function_name,
                                                     min_arguments,
                                                     len(given_arguments)))
        else:
            if max_arguments:
                raise InvalidArgumentNumber("%s requires between %d and %d argument(s), but "
                                       "received %d." % (function_name,
                                                         min_arguments,
                                                         max_arguments,
                                                         len(given_arguments)))
            else:
                raise InvalidArgumentNumber("%s requires at least %d argument(s), but "
                                       "received %d." % (function_name,
                                                         min_arguments,
                                                         len(given_arguments)))

# Función que revisa el tipo de argumentos recibidos en alguna otra función
def check_argument_type(function_name, given_arguments, function_argument_types):
    '''
    La función recibe los siguientes parámetros:
        function_name           : el nombre de la función a analizar
        given_arguments         : los argumentos que recibe
        function_argument_types : los tipos de datos de los argumentos recibidos

    Levanta un Error de excepción en caso de que los tipos de datos no coincidan (Type mismatch)

    '''
    right_argument_type = True

    i = 0
    for i in range(len(given_arguments)):
        if typeof(given_arguments[i]) != function_argument_types[i]:
            right_argument_type = False
            break

    if not right_argument_type:
        required_arg_type = function_argument_types[i]
        given_arg_type = typeof(given_arguments[i])
        raise EspyTypeError("%s requires %s type arguments, but "
                               "received type %s" % (function_name,
                                                     required_arg_type,
                                                     given_arg_type))


def create_unique_if_labels(n):
    return "_IF_L_%s" % n

def create_unique_func_labels(n):
    return "_FUNC_L_%s" % n


def typeof(arg):
    if is_num(arg):
        return "num"
    elif is_boolean(arg):
        return "boolean"
    elif is_char(arg):
        return "char"
    elif is_null(arg):
        return "null"
    else:
        return "variable"


# Función que regresa la instrucción de assembly para guardar en memoria
def save_in_memory(memory_idx):
    return "\tmovl %%eax, %s(%%esp)\n" % memory_idx

# Función que regresa la instrucción de assembly para obtener un dato desde la memoria
def load_from_memory(memory_idx):
    return "\tmovl %s(%%esp), %%eax\n" % memory_idx

# Función para obtener el stack index de un dato dentro de una lista
def get_list_element_mem_idx(symbol, i):
    if i == symbol.size:
        raise EspyIndexOutOfBounds(f"Index {i} out of bounds")
    if(symbol.size != None or symbol.size == 0):
        return symbol.memory_idx - (4 * i)
    else:
        return symbol.memory_idx
        

# Función que restaura las variables globales al usar el interpretador
def restore_glb_var_to_memory(environment, mem_var_idx, mem_list_idx):
    asm = ""
    for var in environment.environment.values():
        if var.value != None:
            idx = var.memory_idx
            if(var.size != None or var.size == 0):
                temp_list = var.value
                for x in temp_list:
                    asm += "\tmovl	$%s, %s(%%esp)\n" % (literal_repr(x), idx)
                    idx -= 4
                    mem_list_idx -= 4
            else:
                value = var.value
                asm += "\tmovl	$%s, %s(%%esp)\n" % (literal_repr(value), idx)
                mem_var_idx -= 4    
    return asm, mem_var_idx, mem_list_idx