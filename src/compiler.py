import os
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
    # program = '''(letrec ([fib (lambda (x) (if (<= x 2) 1 (+ 0 (fib (- x 1)) (fib (- x 2)))))]) (fib 17))'''
    # program = '''(letrec ([f (lambda (x acc) (if (zero? x) acc (f (sub1 x) (* acc x))))]) (f 5 1))'''
    # program = '''(letrec ([f (lambda (x) (if (zero? x) 0 (+ 1 (f (sub1 x)))))]) (f 200))'''
    # program = '''(list [arr 2 3 4 5])'''
    # program = '''(letrec ([fib (lambda (n r1 r2) (if (== n 0) r1 (if (== n 1) r2 (fib (- n 1) r2 (+ r1 r2)))))]) (fib 6 0 1))'''
    # program = '''(+ 2 3 ( + 4 5 ( + 6 (+ 7 8) 9) 10) 11)'''
    # program = '''(letrec ([f (lambda (x) 
    #                             (if (zero? x)
    #                                 1 
    #                                 (* x (f (sub1 x)))))]) 
    #                 (f 5))'''
    # program = '''(letrec ([sum (lambda (n ac)
    #                                 (if (zero? n)
    #                                     ac
    #                                     (sum (sub1 n) (+ n ac))))])
    #                 (sum 10 0))'''
    # print(program)
    # create_binary(program)
    while True:
        program = input("espy> ")
        if program == "exit":
            exit()
        create_binary(program)
    
    (letrec ([fib (lambda (x) (if (<= x 2) arr[0] (+ 0 (fib (- x arr[0])) (fib (- x 2)))))]) (fib arr[2]))
    (letrec ([fib (lambda (x) (if (<= x y) 1 (+ 0 (fib (- x 1)) (fib (- x y)))))]) (fib arr[2]))
