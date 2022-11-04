from literals import is_num, is_boolean, is_char, is_null, is_literal, literal_repr
from platform import system
# from primitives import is_primitive


def emit_function_header(func):
    if system() == "Darwin":
        function_header = """	.text
	.globl	_%s
_%s:
""" % (func, func)
    elif system() == "Windows":
        function_header = """	.text
        .globl	%s
        .def	%s;	.scl	2;	.type	32;	.endef
        .seh_proc	%s
    %s:
        .seh_endprologue
    """ % (func, func, func, func)

    return function_header


def emit_function_footer():
    if system() == "Darwin":
        function_footer = " ret\n"
    elif system() == "Windows":
        function_footer = """     ret
        .seh_endproc
        """
    return function_footer


def emit_stack_header(func):
    asm = '''_%s:
    movl    %%esp, %%ecx
    movl    4(%%esp), %%esp
    call    _L_entry_point
    movl    %%ecx, %%esp
    ret
    ''' % func
    return asm

# .file	"ctest.c"
# 	.text
# 	.globl	entry_point
# 	.def	entry_point;	.scl	2;	.type	32;	.endef
# 	.seh_proc	entry_point


def emit_literal(expr):
    asm = ""
    value = literal_repr(expr)
    if is_num(expr):
        asm += "\tmovl	$%s, %%eax\n" % value
    elif is_boolean(expr):
        asm += "\tmovl	$%s, %%eax\n" % value
    elif is_char(expr):
        asm += "\tmovl	$%s, %%eax\n" % value
    elif is_null(expr):
        asm += "\tmovl	$%s, %%eax\n" % value
    else:
        print("Error")
        exit()
    return asm


def emit_primcall(expr):
    pass


def emit_conditional_expr(expr):
    pass
