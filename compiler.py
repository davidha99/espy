import os
from parser import parser

def create_binary(program):
    """Given text of a scheme program, write assembly and link it into an
    executable.

    """
    parser.parse(program)

    os.system('gcc-12 scheme.s runtime.c -o main')

    
if __name__ == '__main__':
    program = "(fxadd1 0)"
    create_binary(program)