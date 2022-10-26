fxshift = 2
fxmask = '%x' % int('00000011', 2)
fxtag = '%x' % int('00000000', 2)
bool_bit = 6 # '%x' % int('00000110', 2)
boolshift = 7
charshift = 8
chartag = 15
bool_f = '%x' % int('00101111', 2)
bool_t = '%x' % int('01101111', 2)
empty_list = '%x' % int('00111111', 2)
wordsize = 4 # bytes


fixnum_bits = (wordsize * 8) - fxshift
fxlower = -1 * pow(2, fixnum_bits - 1) # -2^29 = -536870912
fxupper = pow(2, fixnum_bits - 1) - 1 # 2^29 - 1 = 536870911

def is_fixnum(x):
    return isinstance(x, int) and fxlower <= x and x <= fxupper

def is_boolean(x):
    return x == "#t" or x == "#f"

def is_char(x):
    return "\#" in x

def is_null(x):
    return x == "()"

def is_immediate(x):
    return is_fixnum(x) or is_boolean(x) or is_char(x) or is_null(x)

def compile_fixnum(value):
    value = value << fxshift
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
    value = (to_int << charshift) + chartag
    return value

def compile_null(value):
    value = empty_list
    return value

def immediate_repr(code):
    if is_fixnum(code):
        return compile_fixnum(code)
    elif is_boolean(code):
        return compile_boolean(code)
    elif is_char(code):
        return compile_char(code)
    elif is_null(code):
        return compile_null(code)
    else:
        print("Error")
        exit()