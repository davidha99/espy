import os
from platform import system
from parser import parser

def create_binary(program):
    """Given text of a scheme program, write assembly and link it into an
    executable.

    """
    parser.parse(program)

    if system() == "Darwin":
        os.system("gcc-12 scheme.s runtime.c -o main")
    elif system() == "Windows":
        os.system('gcc scheme.s runtime.c -o main')

    
if __name__ == '__main__':
    program = "(fixnum? (fixnum? \#A))"
    create_binary(program)