import os
from parser import parser

def create_binary(program):
    """Given text of a scheme program, write assembly and link it into an
    executable.

    """
    parser.parse(program)

    os.system('gcc scheme.s runtime.c -o main')

    
if __name__ == '__main__':
    program = "(char->fixnum (fixnum->char 32))"
    create_binary(program)