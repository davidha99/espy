#!/usr/bin/python3
import os
import sys
from environment import Environment_Stack
from parser import parser

'''
    espy.py
    Descripción: Clase principal que inicializa el compilador 
    y/o el interpretador
    Autores: David Hernández    |   A01383543
             Bernardo García    |   A00570682
'''

def create_binary(program):
    """
    Dado un texto de un programa espy, e inicializa el flujo de compilación.
    Su resultado se reproduce en un executable: main. 
    En caso de correr el interpretador, el resultado se muestra en la linea de comandos
    """
    parser_status = parser.parse(program)

    if (parser_status == "Parsed"):
        os.system("gcc espy.s runtime.c -o main -w")
        os.system("./main")

    else:
        exit()


if __name__ == '__main__':
    
    # El usuario puede elegir si leer un programa en archivo 
    # o escribir el programa en el interpretador    
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
