#!/usr/bin/python3

import os
import sys
from environment import Environment_Stack
from parser import parser


def create_binary(program):
    """
    Given text of a scheme program, write assembly and link it into an
    executable.
    """
    parser_status = parser.parse(program)

    if (parser_status == "Parsed"):
        os.system("gcc espy.s runtime.c -o main -w")
        os.system("./main")

    else:
        exit()


if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            program = f.read()
        create_binary(program)
    elif len(sys.argv) == 1:
        while True:
            program = input("espy> ")
            if program == "exit":
                exit()
            create_binary(program)
