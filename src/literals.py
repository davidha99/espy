num_shift = 2
num_mask = 3  # '%x' % int('00000011', 2)
num_tag = 0  # '%x' % int('00000000', 2)
bool_bit = 6  # '%x' % int('00000110', 2)
char_shift = 8
char_tag = 15  # '%x' % int('00001111', 2)
char_mask = 255  # int('11111111', 2)
bool_f = 47  # '%x' % int('00101111', 2)
bool_t = 111  # '%x' % int('01101111', 2)
empty_list = 63  # '%x' % int('00111111', 2)
wordsize = 4  # bytes
num_bits = (wordsize * 8) - num_shift
num_lower = -1 * pow(2, num_bits - 1)  # -2^29 = -536870912
num_upper = pow(2, num_bits - 1) - 1  # 2^29 - 1 = 536870911


def is_num(x):
    return isinstance(x, int) and num_lower <= x and x <= num_upper


def is_boolean(x):
    return is_boolean_t(x) or is_boolean_f(x)


def is_boolean_t(x):
    return x == "#t"


def is_boolean_f(x):
    return x == "#f"


def is_char(x):
    return "\#" in str(x)


def is_null(x):
    return x == "()"


def is_literal(x):
    return is_num(x) or is_boolean(x) or is_char(x) or is_null(x)


def compile_num(value):
    value = value << num_shift
    return value


def compile_boolean(value):
    if value == "#t":
        value = bool_t
    elif value == "#f":
        value = bool_f
    return value


def compile_char(value):
    # Make char int, and then shift 8 bits to the left
    char = value[2]
    to_int = ord(char)
    value = (to_int << char_shift) + char_tag
    return value


def compile_null(value):
    value = empty_list
    return value


def literal_repr(code):
    if is_num(code):
        return compile_num(code)
    elif is_boolean(code):
        return compile_boolean(code)
    elif is_char(code):
        return compile_char(code)
    elif is_null(code):
        return compile_null(code)
    else:
        print("Error")
        exit()
