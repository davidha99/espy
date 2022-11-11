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
    program = '''(if #t 12 13)'''
    create_binary(program)
