from immediates import is_fixnum, is_boolean, is_char, is_null, is_immediate, immediate_repr
from platform import system
# from primitives import is_primitive

def emit_function_header(func):
    if system() == "Darwin":
        function_header = """	.text
	.globl	_%s
_%s:
LFB0:
""" % (func,func)
    elif system() == "Windows":
        function_header = """	.text
        .globl	%s
        .def	%s;	.scl	2;	.type	32;	.endef
        .seh_proc	%s
    %s:
        .seh_endprologue
    """ % (func,func, func, func)

    return function_header

def emit_function_footer():
    if system() == "Darwin":
        function_footer = " ret"
    elif system() == "Windows":
        function_footer = """     ret
        .seh_endproc
        """
    return function_footer

# .file	"ctest.c"
# 	.text
# 	.globl	entry_point
# 	.def	entry_point;	.scl	2;	.type	32;	.endef
# 	.seh_proc	entry_point

def emit_immediate(expr):
    asm = ""
    value = immediate_repr(expr)
    if is_fixnum(expr):
        asm += "\tmovl	$%s, %%eax\n" % value
    elif is_boolean(expr):
        asm += "\tmovl	$%s, %%eax\n" % int(value, 16)
    elif is_char(expr):
        asm += "\tmovl	$%s, %%eax\n" % value
    elif is_null(expr):
        asm += "\tmovl	$%s, %%eax\n" % int(value, 16)
    else:
        print("Error")
        exit()
    return asm

def emit_primcall(expr):
    pass

# def emit_expr(expr):
#     if is_immediate(expr):
#         return emit_immediate(expr)
#     elif is_primitive(expr):
#         return emit_primcall(expr)
#     else:
#         print("Error")
#         exit()

# def emit_program(expr):
#     asm = ""
#     asm += emit_function_header("entry_point")
#     asm += emit_expr(expr)
#     asm += "    ret"
#     return asm