import os
from emitter import emit_program

def create_binary(program):
    """Given text of a scheme program, write assembly and link it into an
    executable.

    """
    # todo: lex and parse
    
    with open('scheme.s', 'w') as f:
        f.write(emit_program(program))

    os.system('gcc-12 scheme.s runtime.c -o main')

    
if __name__ == '__main__':
    program = 32
    create_binary(program)