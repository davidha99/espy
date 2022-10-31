import os
from platform import system
from parser import parser

def create_binary(program):
    """Given text of a scheme program, write assembly and link it into an
    executable.

    """
    parser_status = parser.parse(program)

    if (parser_status == "Parsed"):
        if system() == "Darwin":
            os.system("gcc-12 scheme.s runtime.c -o main")
        elif system() == "Windows":
            os.system('gcc scheme.s runtime.c -o main')
    else:
        exit()


    
if __name__ == '__main__':
    program = '''(if (not (if (if (not 1) 
                                    (not 2) 
                                    (not 3)) 
                                4 
                                5)) 
                        6 
                        7)'''
    create_binary(program)