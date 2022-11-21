import os
from environment import Environment_Stack
from parser import parser

environment_stack = Environment_Stack()


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
    # program = '''(let ([x 1]) (let ([y 2]) (let ([z 3]) (* x y (+ z x)))))'''
    # program = '''(var [x 2])'''
    # program = '''(letrec ([g (lambda (x y) (+ x y))] [f (lambda (x) (g x x))]) (f 12))'''
    # program = '''(letrec ([f (lambda (x y) (+ x y))] [g (lambda (x) (+ x 12))]) (f 16 (f (g 0) (+ 1 (g 0)))))'''
    program = '''(letrec ([sum (lambda (n ac)
                                    (if (zero? n)
                                        ac
                                        (sum (sub1 n) (+ n ac))))])
                    (sum 10 0))'''
    # print(program)
    create_binary(program)
    # environment_stack.scope_enter(0)    # Global scope
    # while True:
    #     program = input("espy> ")
    #     if program == "exit":
    #         exit()
    #     create_binary(program)
    
