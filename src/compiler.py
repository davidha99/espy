import os
from parser import parser


def create_binary(program):
    """Given text of a scheme program, write assembly and link it into an
    executable.

    """
    parser_status = parser.parse(program)

    if (parser_status == "Parsed"):
        os.system("gcc espy.s runtime.c -o main")
    else:
        exit()


if __name__ == '__main__':
    program = '''(+ 1 2 (- 5 7) 15 (+ 40 10 (+ 5 (+ 5 10 (- 10 5)) 5 (- 10 2))) 7 9 (+ 2 3 (- 10 5 2) 5 (+ 4 5)))'''
    create_binary(program)
