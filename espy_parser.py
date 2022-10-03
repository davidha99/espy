# ESPY parser

import ply.yacc as yacc
import sys
from espy_lexer import tokens

def p_program(p):
    '''
    program : main
    '''
    p[0] = "COMPILED ESPY"

def p_main(p):
    '''
    main : LPAREN MAIN form RPAREN
    '''

def p_form(p):
    '''
    form : form form
         | variable_definition
         | expression
    '''

def p_variable_definition(p):
    '''
    variable_definition : LPAREN DEFINE inside_var_def RPAREN
    '''

def p_inside_var_def(p):
    '''
    inside_var_def : variable expression
                   | LPAREN multiple_vars RPAREN body
    '''

def p_multiple_vars(p):
    '''
    multiple_vars : multiple_vars multiple_vars
                  | variable
    '''

def p_variable(p):
    '''
    variable : ID
    '''

def p_body(p):
    '''
    body : with_multiple_defs multiple_expr
    '''

def p_with_multiple_defs(p):
    '''
    with_multiple_defs : with_multiple_defs with_multiple_defs
                       | definition
                       | empty
    '''

def p_multiple_expr(p):
    '''
    multiple_expr : multiple_expr multiple_expr
                  | expression
    '''

# def keyword(p):
#     '''
#     keyword : identifier
#     '''

def p_expression(p):
    '''
    expression : constant
               | variable
               | LPAREN inside_expr RPAREN
               | SQUOTE datum
               | application
               | derived_expression
    '''

def p_inside_expr(p):
    '''
    inside_expr : QUOTE datum
                | SET variable expression
                | IF expression expression
                | IF expression expression expression
    '''

def p_constant(p):
    '''
    constant : boolean
             | number
             | character
             | string
    '''

def p_application(p):
    '''
    application : LPAREN expression RPAREN
    '''

def p_derived_expression(p):
    '''
    derived_expression: COND
                      | AND
                      | OR
                      | DO
    '''

def p_datum(p):
    '''
    datum : boolean
          | number
          | character
          | string
          | list
    '''

def p_list(p):
    '''
    list : LPAREN with_multiple_datums RPAREN
    '''

def p_with_multiple_datums(p):
    '''
    with_multiple_datums : with_multiple_datums with_multiple_datums
                         | empty
    '''

def p_var_id(p):
    '''
    var_id : ID
           | ID COMA var_id
    '''

def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
    '''

def p_vars_bloque(p):
    '''
    vars_bloque : var_id COLON tipo SEMICOLON vars_bloque
                | empty
    '''

def p_vars(p):
    '''
    vars : VAR var_id COLON tipo SEMICOLON vars_bloque
    '''

def p_bloque(p):
    '''
    bloque : LBRACK estatuto_bloque RBRACK
    '''

def p_estatuto_bloque(p):
    '''
    estatuto_bloque : estatuto estatuto_bloque
                    | empty
    '''

def p_estatuto(p):
    '''
    estatuto : asignacion
             | condicion
             | escritura
    '''

def p_asignacion(p):
    '''
    asignacion : ID EQUALS expresion SEMICOLON
    '''

def p_condicion(p):
    '''
    condicion : IF LPAREN expresion RPAREN bloque bloque_else
    '''

def p_bloque_else(p):
    '''
    bloque_else : ELSE bloque
                | empty
    '''

def p_escritura(p):
    '''
    escritura : PRINT LPAREN impr_valor RPAREN SEMICOLON
    '''

def p_impr_valor(p):
    '''
    impr_valor : expresion impr_expresion
               | CTESTRING impr_expresion
    '''

def p_impr_expresion(p):
    '''
    impr_expresion : COMA impr_valor
                   | empty
    '''

def p_expresion(p):
    '''
    expresion : exp operador_comparacion
    '''

def p_operador_comparacion(p):
    '''
    operador_comparacion : GT exp
                         | LT exp
                         | NE exp
                         | empty
    '''

def p_exp(p):
    '''
    exp : termino operador_termino
    '''

def p_operador_termino(p):
    '''
    operador_termino : PLUS exp
                     | MINUS exp
                     | empty
    '''

def p_termino(p):
    '''
    termino : factor operador_factor
    '''

def p_operador_factor(p):
    '''
    operador_factor : TIMES termino
                    | DIVIDE termino
                    | empty
    '''

def p_factor(p):
    '''
    factor : LPAREN expresion RPAREN
           | signo var_cte
    '''

def p_signo(p):
    '''
    signo : PLUS
          | MINUS
          | empty
    '''

def p_var_cte(p):
    '''
    var_cte : ID
            | CTEI
            | CTEF
    '''

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if parser.parse(data) == "COMPILED":
                print("Valid input")
        except EOFError:
            print(EOFError)
    else:
        print("No file to test found")