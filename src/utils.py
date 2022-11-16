from errors import EspyTypeError, InvalidArgumentNumber, EspyNameError
from literals import is_boolean, is_char, is_null, is_num


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


def check_argument_type(function_name, given_arguments, function_argument_types):
    '''
    This functions receives the following parameters:
        function_name           : the name of the function as a str
        given_arguments         : the given arguments as a tuple
        function_argument_types : the types of every argument as a tuple

    It raises an exception if there is a type mismatch of any argument

    Example:

    check_argument_type('num->char', (arg1, arg2, arg3), (type1, type2, type3))

    The function checks the types as the following:
    arg1 -> type1
    arg2 -> type2
    arg3 -> type3

    The types should be specified as: "boolean", "num", "char", "null", so if you want to
    check if some argument is of type "boolean" you could do the following:

    check_argument_type('if', (test_expr,), ('boolean',))
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
    # Maybe here we need to add a check for platform support
    # MacOS or Windows
    return "_IF_L_%s" % n

def create_unique_func_labels(n):
    # Maybe here we need to add a check for platform support
    # MacOS or Windows
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


# def check_defined_variable(variable_name, environment):
#     if variable_name not in environment.keys():
#         raise EspyNameError("Variable %s is not defined" % variable_name)

    
# def load_from_memory(memory_idx=None, variable_name=None, environment=None):
#     if memory_idx is not None:
#         return "\tmovl %s(%%esp), %%eax\n" % memory_idx
#     elif variable_name is not None and environment is not None:
#         variable_index = environment[variable_name]
#         check_defined_variable(variable_name, environment)
#         return "\tmovl %s(%%esp), %%eax\n" % str(variable_index)

def save_in_memory(memory_idx):
    return "\tmovl %%eax, %s(%%esp)\n" % memory_idx
    
# def load_variable_from_memory(variable_name, environment):
#     variable_index = environment[variable_name]
#     check_defined_variable(variable_name, environment)
#     return "\tmovl %s(%%esp), %%eax\n" % str(variable_index)


# def is_variable(x):
#     return typeof(x) == "variable"