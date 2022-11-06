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
    bool_bit)
from utils import check_argument_number, check_argument_type

primitives = {}

# a decorator for creating a primitive function object and giving it a name


def define_primitive(function_name):
    def define_primitive_decorator(function):
        primitives[function_name] = function

        # we return the function too, so we can use multiple decorators
        return function

    return define_primitive_decorator


@define_primitive('add1')
def add1(*argv):
    check_argument_number('add1', argv, 1, 1)
    check_argument_type('add1', argv, ('num',))
    temp = argv[0] + 1
    asm = "\taddl    $%s, %%eax\n" % (literal_repr(1))
    return temp, asm


@define_primitive('sub1')
def sub1(*argv):
    check_argument_number('sub1', argv, 1, 1)
    check_argument_type('sub1', argv, ('num',))
    temp = argv[0] - 1
    asm = "\tsubl   $%s, %%eax\n" % (literal_repr(1))
    return temp, asm


@define_primitive('char->num')
def char_to_num(*argv):
    check_argument_number('char->num', argv, 1, 1)
    check_argument_type('char->num', argv, ('char',))
    given_char = argv[0]
    temp = compile_char(given_char)
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
    check_argument_number('num->char', argv, 1, 1)
    check_argument_type('num->char', argv, ('num',))
    given_num = argv[0]
    temp = "\#"
    temp += chr(given_num)
    asm = "\tshll\t$%s, %%eax\n" % (char_shift - num_shift)
    asm += "\torl   \t$%s, %%eax\n" % char_tag
    return temp, asm


@define_primitive('num?')
def num_(*argv):
    temp = argv[0]
    temp = "#t" if is_num(temp) else "#f"
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
    temp = argv[0]
    value = 111 if is_boolean_t(temp) else 47
    temp = "#t" if is_boolean(temp) else "#f"
    asm = ""
    asm += "\tcmp  $%s, %%al\n" % value  # Compare the true or false mask
    asm += "\tsete  %al\n"
    asm += "\tmovzbl    %al, %eax\n"
    asm += "\tsal   $%s, %%al\n" % bool_bit
    asm += "\tor    $%s, %%al\n" % 47
    return temp, asm


@define_primitive('char?')
def char_(*argv):
    temp = argv[0]
    temp = "#t" if is_char(temp) else "#f"
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
    temp = argv[0]
    temp = "#t" if is_null(temp) else "#f"
    asm = ""
    asm += "\tcmp  $%s, %%al\n" % 63  # Compare Empty list binary mask
    asm += "\tsete  %al\n"
    asm += "\tmovzbl    %al, %eax\n"
    asm += "\tsal   $%s, %%al\n" % bool_bit
    asm += "\tor    $%s, %%al\n" % 47
    return temp, asm


@define_primitive('not')
def not_primitive(*argv):
    temp = argv[0]
    temp = "#t" if temp == "#f" or temp == 0 or temp == "()" else "#f"
    asm = ""
    asm += "\tcmp  $%s, %%al\n" % bool_f
    asm += "\tsete  %al\n"
    asm += "\tmovzbl    %al, %eax\n"
    asm += "\tsal   $%s, %%al\n" % bool_bit
    asm += "\tor    $%s, %%al\n" % bool_f
    return temp, asm


@define_primitive('zero?')
def is_zero(*argv):
    check_argument_number('zero?', argv, 1, 1)
    check_argument_type('zero?', argv, ('num',))
    temp = argv[0]
    temp = "#t" if temp == 0 else "#f"
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
    
    if len(operands) == 1:
        temp = operands[0]
        asm = "\tmovl %%eax, %s(%%esp)\n" % str(si)
        return temp, asm
    else:
        temp = operands[0] + operands[1]
        asm = "\taddl %s(%%esp), %%eax\n" % str(si)
        return temp, asm
