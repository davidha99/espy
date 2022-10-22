from immediates import is_immediate, immediate_repr
from primitives import is_primitive

def emit_function_header(func):
    function_header = """	.text
	.globl	_%s
_%s:
LFB0:
\t
""" % (func,func,)

    return function_header

def emit_immediate(expr):
    return immediate_repr(expr)

def emit_primcall(expr):
    pass

def emit_expr(expr):
    if is_immediate(expr):
        return emit_immediate(expr)
    elif is_primitive(expr):
        return emit_primcall(expr)
    else:
        print("Error")
        exit()

def emit_program(expr):
    asm = ""
    asm += emit_function_header("entry_point")
    asm += emit_expr(expr)
    asm += "    ret"
    return asm