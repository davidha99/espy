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

def typeof(arg):
    if is_fixnum(arg):
        return "fixnum"
    elif is_boolean(arg):
        return "boolean"
    elif is_char(arg):
        return "char"
    elif is_null(arg):
        return "null"