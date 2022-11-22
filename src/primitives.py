from emitter import emit_literal
from literals import (
    compile_num,
    literal_repr,
    compile_char,
    is_num,
    is_boolean,
    is_boolean_t,
    is_boolean_f,
    is_char,
    is_null,
    empty_list,
    char_shift,
    num_shift,
    char_tag,
    char_mask,
    num_mask,
    num_tag,
    bool_f,
    bool_bit
    )

from utils import (
    check_argument_number, 
    check_argument_type, 
    typeof
    )

primitives = {}

TEMP_DIR = -1000

# a decorator for creating a primitive function object and giving it a name


def define_primitive(function_name):
    def define_primitive_decorator(function):
        primitives[function_name] = function

        # we return the function too, so we can use multiple decorators
        return function

    return define_primitive_decorator


@define_primitive('add1')
def add1(*argv):
    if argv[0] is not None:
        check_argument_number('add1', argv, 1, 1)
        check_argument_type('add1', argv, ('num',))
        temp = argv[0] + 1
    else:
        temp = None
    asm = "\taddl    $%s, %%eax\n" % (literal_repr(1))
    return temp, asm


@define_primitive('sub1')
def sub1(*argv):
    if argv[0] is not None:
        check_argument_number('sub1', argv, 1, 1)
        check_argument_type('sub1', argv, ('num',))
        temp = argv[0] - 1
    else:
        temp = None
    asm = "\tsubl   $%s, %%eax\n" % (literal_repr(1))
    return temp, asm


@define_primitive('char->num')
def char_to_num(*argv):
    if argv[0] is not None:
        check_argument_number('char->num', argv, 1, 1)
        check_argument_type('char->num', argv, ('char',))
        given_char = argv[0]
        temp = compile_char(given_char)
    else:
        temp = None
    # Shift to the right by 6, explanation:
    #   Num tag: b'      00'
    #   Char tag  : b'00001111'
    temp -= char_tag
    temp = temp >> (char_shift - num_shift)
    asm = "\torl   \t$%s, %%eax\n" % num_shift
    asm += "\tshrl\t$%s, %%eax\n" % (char_shift - num_shift)
    return temp, asm


@define_primitive('num->char')
def num_to_char(*argv):
    if argv[0] is not None:
        check_argument_number('num->char', argv, 1, 1)
        check_argument_type('num->char', argv, ('num',))
        given_num = argv[0]
        temp = "\#"
        temp += chr(given_num)
    else:
        temp = None
    asm = "\tshll\t$%s, %%eax\n" % (char_shift - num_shift)
    asm += "\torl   \t$%s, %%eax\n" % char_tag
    return temp, asm


@define_primitive('num?')
def num_(*argv):
    try:
        temp = argv[0]
        temp = "#t" if is_num(temp) else "#f"
    except:
        temp = None
    asm = ""
    asm += "\tand $%s, %%al\n" % num_mask  # Extracting lower 2 bits
    asm += "\tcmp  $%s, %%al\n" % num_tag  # Comparing lower two bits with num_tag
    asm += "\tsete  %al\n"
    asm += "\tmovzbl    %al, %eax\n"
    asm += "\tsal   $%s, %%al\n" % bool_bit
    asm += "\tor    $%s, %%al\n" % bool_f
    return temp, asm


@define_primitive('boolean?')
def boolean_(*argv):
    try:
        temp = argv[0]
        value = 111 if is_boolean_t(temp) else 47
        temp = "#t" if is_boolean(temp) else "#f"
    except:
        temp = None
    asm = ""
    asm += "\tcmp  $%s, %%al\n" % value  # Compare the true or false mask
    asm += "\tsete  %al\n"
    asm += "\tmovzbl    %al, %eax\n"
    asm += "\tsal   $%s, %%al\n" % bool_bit
    asm += "\tor    $%s, %%al\n" % 47
    return temp, asm


@define_primitive('char?')
def char_(*argv):
    try:
        temp = argv[0]
        temp = "#t" if is_char(temp) else "#f"
    except:
        temp = None
    asm = ""
    asm += "\tand $%s, %%al\n" % char_mask  # Extracting lower 8 bits
    asm += "\tcmp  $%s, %%al\n" % char_tag  # Comparing lower 8 bits with char tag
    asm += "\tsete  %al\n"
    asm += "\tmovzbl    %al, %eax\n"
    asm += "\tsal   $%s, %%al\n" % bool_bit
    asm += "\tor    $%s, %%al\n" % 47
    return temp, asm


@define_primitive('null?')
def null_(*argv):
    try:
        temp = argv[0]
        temp = "#t" if is_null(temp) else "#f"
    except:
        temp = None
    asm = ""
    asm += "\tcmp  $%s, %%al\n" % 63  # Compare Empty list binary mask
    asm += "\tsete  %al\n"
    asm += "\tmovzbl    %al, %eax\n"
    asm += "\tsal   $%s, %%al\n" % bool_bit
    asm += "\tor    $%s, %%al\n" % 47
    return temp, asm


@define_primitive('not')
def not_primitive(*argv):
    try:
        temp = argv[0]
        temp = "#t" if temp == "#f" or temp == 0 or temp == "()" else "#f"
    except:
        temp = None
    asm = ""
    asm += "\tcmp  $%s, %%al\n" % bool_f
    asm += "\tsete  %al\n"
    asm += "\tmovzbl    %al, %eax\n"
    asm += "\tsal   $%s, %%al\n" % bool_bit
    asm += "\tor    $%s, %%al\n" % bool_f
    return temp, asm


@define_primitive('zero?')
def is_zero(*argv):
    if argv[0] is not None:
        check_argument_number('zero?', argv, 1, 1)
        check_argument_type('zero?', argv, ('num',))
        temp = argv[0]
        temp = "#t" if temp == 0 else "#f"
    else:
        temp = None
    asm = ""
    asm += "\tcmp   $%s, %%al\n" % 0
    asm += "\tsete  %al\n"
    asm += "\tmovzbl    %al, %eax\n"
    asm += "\tsal   $%s, %%al\n" % bool_bit
    asm += "\tor    $%s, %%al\n" % bool_f
    return temp, asm


@define_primitive('if_test')
def if_test_expression(test_expr, labels):
    # Aquí tenemos la opción de que los IFs sólo acepten booleanos o
    # que acepte cualquier otra cosa que no sea #f como verdadero.

    # check_argument_type('if_test', (test_expr,), ('boolean',))
    alt_label = labels[-2]
    asm = ""
    asm += "\tcmp $%s, %%al\n" % bool_f
    asm += "\tje %s\n" % alt_label

    return asm


@define_primitive('if_consequent')
def if_consequent_expression(labels):
    alt_label = labels[-2]
    end_label = labels[-1]
    asm = ""
    asm += "\t jmp %s\n" % end_label
    asm += "%s:" % alt_label
    asm += "\n"
    return asm


@define_primitive('if_alternate')
def if_alterante_expression(labels):
    end_label = labels[-1]
    asm = "%s:" % end_label
    asm += "\n"
    return asm


@define_primitive('addition')
def addition(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = int(operands[-2]) + int(operands[-1])
        except:
            temp = 0
        asm = "\taddl %%eax, %s(%%esp) \n" % str(si + TEMP_DIR)    # This means si(esp) = n(esp) + eax
        return temp, asm

@define_primitive('substraction')
def substraction(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] - operands[-1]
        except:
            temp = 0
        asm = "\tsubl %%eax, %s(%%esp) \n" % str(si + TEMP_DIR)    # This means si(esp) = n(esp) - eax
        return temp, asm

@define_primitive('multiplication')
def multiplication(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] * operands[-1]
        except:
            temp = 0
        asm = ""
        asm += "\tmovl %s(%%esp), %%edx\n" % str(si + TEMP_DIR)
        asm += "\tsar $%s, %%edx\n" % num_shift
        asm += "\tsar $%s, %%eax\n" % num_shift
        asm += "\timul %edx, %eax\n"                    # This means eax *= ebx
        asm += "\tsal   $%s, %%eax\n" % num_shift       # Shift to the left the byte answer
        asm += "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)

        return temp, asm

@define_primitive('division')
def division(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] / operands[-1]
        except:
            temp = 0
        asm = ""
        asm += "\tmovl %eax, %ebx\n"                        # Divisor
        # asm += "\tsar $%s, %%ebx\n" % num_shift
        asm += "\tmovl $0, %edx\n"                           # Clear remainder
        asm += "\tmovl %s(%%esp), %%eax\n" % str(si + TEMP_DIR)        # Dividend
        # asm += "\tsar $%s, %%eax\n" % num_shift
        asm += "\tdiv %ebx\n"                    # This means eax /= ebx, the remainder is set in edx
        asm += "\tsal   $%s, %%eax\n" % num_shift   # Shift to the left the byte answer
        asm += "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)

        return temp, asm


@define_primitive('and')
def and_expression(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] and operands[-1]
        except:
            temp = 0
        asm = "\tand %s(%%esp), %%eax\n" % str(si + TEMP_DIR)
        asm += "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)
        return temp, asm

@define_primitive('or')
def or_expression(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] and operands[-1]
        except:
            temp = 0
        asm = "\tor %s(%%esp), %%eax\n" % str(si + TEMP_DIR)
        asm += "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)
        return temp, asm

@define_primitive('lessequal')
def less_equal(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] <= operands[-1]
        except:
            temp = 0
        asm = ""
        asm += "\tmovl %s(%%esp), %%ebx\n" % str(si + TEMP_DIR)
        asm += "\tcmp %eax, %ebx\n"     # Compare operands as: 'ebx <= eax'
        asm += "\tsetle %al\n"          # After comparing, the result is safed in 'al', memory section that safes #t or #f as 8 bits (1 byte)
        asm += "\tmovzbl    %al, %eax\n"
        asm += "\tsal   $%s, %%al\n" % bool_bit     # Shift the 0/1 byte value to its representation as boolean #f/#t
        asm += "\tor    $%s, %%al\n" % bool_f       
        asm += "\tmov %%al, %s(%%esp)\n" % str(si + TEMP_DIR)     # Save the boolean in memory stack
        return temp, asm

@define_primitive('greaterequal')
def greater_equal(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] >= operands[-1]
        except:
            temp = 0
        asm = ""
        asm += "\tmovl %s(%%esp), %%ebx\n" % str(si + TEMP_DIR)
        asm += "\tcmp %ebx, %eax\n"     # Compare operands as: 'ebx >= eax'
        asm += "\tsetle %al\n"          # After comparing, the result is safed in 'al', memory section that safes #t or #f as 8 bits (1 byte)
        asm += "\tmovzbl    %al, %eax\n"
        asm += "\tsal   $%s, %%al\n" % bool_bit     # Shift the 0/1 byte value to its representation as boolean #f/#t
        asm += "\tor    $%s, %%al\n" % bool_f       
        asm += "\tmov %%al, %s(%%esp)\n" % str(si + TEMP_DIR)     # Save the boolean in memory stack
        return temp, asm

@define_primitive('equal')
def equal(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] == operands[-1]
        except:
            temp = 0
        asm = ""
        asm += "\tmovl %s(%%esp), %%ebx\n" % str(si + TEMP_DIR)
        asm += "\tcmp %ebx, %eax\n"     # Compare operands as: 'ebx == eax'
        asm += "\tsete %al\n"          # After comparing, the result is safed in 'al', memory section that safes #t or #f as 8 bits (1 byte)
        asm += "\tmovzbl    %al, %eax\n"
        asm += "\tsal   $%s, %%al\n" % bool_bit     # Shift the 0/1 byte value to its representation as boolean #f/#t
        asm += "\tor    $%s, %%al\n" % bool_f       
        asm += "\tmov %%al, %s(%%esp)\n" % str(si + TEMP_DIR)    # Save the boolean in memory stack
        return temp, asm

@define_primitive('lessthan')
def less_than(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] < operands[-1]
        except:
            temp = 0
        asm = ""
        asm += "\tmovl %s(%%esp), %%ebx\n" % str(si + TEMP_DIR)
        asm += "\tcmp %eax, %ebx\n"     # Compare operands as: 'ebx < eax'
        asm += "\tsetl %al\n"          # After comparing, the result is safed in 'al', memory section that safes #t or #f as 8 bits (1 byte)
        asm += "\tmovzbl    %al, %eax\n"
        asm += "\tsal   $%s, %%al\n" % bool_bit     # Shift the 0/1 byte value to its representation as boolean #f/#t
        asm += "\tor    $%s, %%al\n" % bool_f       
        asm += "\tmov %%al, %s(%%esp)\n" % str(si + TEMP_DIR)     # Save the boolean in memory stack
        return temp, asm

@define_primitive('greaterthan')
def greater_than(*argv):
    si = argv[0]  # stack index
    operands = argv[1]
    indv_operand = argv[2]
    
    if indv_operand:
        temp = operands[-1]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si + TEMP_DIR)     # This means si(esp) = eax
        return temp, asm
    else:
        try: 
            temp = operands[-2] > operands[-1]
        except:
            temp = 0
        asm = ""
        asm += "\tmovl %s(%%esp), %%ebx\n" % str(si + TEMP_DIR)
        asm += "\tcmp %ebx, %eax\n"     # Compare operands as: 'ebx > eax'
        asm += "\tsetl %al\n"          # After comparing, the result is safed in 'al', memory section that safes #t or #f as 8 bits (1 byte)
        asm += "\tmovzbl    %al, %eax\n"
        asm += "\tsal   $%s, %%al\n" % bool_bit     # Shift the 0/1 byte value to its representation as boolean #f/#t
        asm += "\tor    $%s, %%al\n" % bool_f       
        asm += "\tmov %%al, %s(%%esp)\n" % str(si + TEMP_DIR)    # Save the boolean in memory stack
        return temp, asm