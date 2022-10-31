from errors import SchemeArityError
from immediates import is_boolean, is_char, is_null, is_fixnum

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
            raise SchemeArityError("%s requires exactly %d argument(s), but "
                                  "received %d." % (function_name,
                                                    min_arguments,
                                                    len(given_arguments)))
        else:
            if max_arguments:
                raise SchemeArityError("%s requires between %d and %d argument(s), but "
                                      "received %d." % (function_name,
                                                        min_arguments,
                                                        max_arguments,
                                                        len(given_arguments)))
            else:
                raise SchemeArityError("%s requires at least %d argument(s), but "
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

    check_argument_type('fixnum->char', (arg1, arg2, arg3), (type1, type2, type3))

    The function checks the types as the following:
    arg1 -> type1
    arg2 -> type2
    arg3 -> type3

    The types should be specified as: "boolean", "fixnum", "char", "null", so if you want to
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
        raise SchemeArityError("%s requires %s type arguments, but "
                               "received type %s" % (function_name,
                                                    required_arg_type,
                                                    given_arg_type))

def create_unique_label(n):
    # Maybe here we need to add a check for platform support
    # MacOS or Windows
    return "_L_%s" % n

def typeof(arg):
    if is_fixnum(arg):
        return "fixnum"
    elif is_boolean(arg):
        return "boolean"
    elif is_char(arg):
        return "char"
    elif is_null(arg):
        return "null"