import os
from parser import parser


def create_binary(program):
    """Given text of a scheme program, write assembly and link it into an
    executable.

    """
    parser_status = parser.parse(program)

    if (parser_status == "Parsed"):
        os.system("gcc espy.s runtime.c -o main -w")
        os.system("./main")
        # r = open("main", 'r')
        # print(str(r.readline()))
        # r.close()

    else:
        exit()


if __name__ == '__main__':
    # program = '''(let ([x 12]) (let ([x (+ x x)]) (let ([x (+ x x)]) (let ([x (+ x x)]) (+ x x)))))'''
    while True:
        program = input("espy> ")
        if program == "exit":
            exit()
        create_binary(program)
    
