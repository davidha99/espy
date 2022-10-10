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
    main : LPAREN MAIN form with_multiple_forms RPAREN
    '''

def p_with_multiple_forms(p):
    '''
    with_multiple_forms : with_multiple_forms form
                        | empty
    '''

def p_form(p):
    '''
    form : variable_definition
         | expression
    '''

def p_variable_definition(p):
    '''
    variable_definition : LPAREN DEFINE inside_var_def RPAREN
    '''

def p_inside_var_def(p):
    '''
    inside_var_def : variable expression
                   | LPAREN variable with_multiple_vars RPAREN body
    '''

def p_with_multiple_vars(p):
    '''
    with_multiple_vars : with_multiple_vars variable
                       | empty
    '''

def p_variable(p):
    '''
    variable : ID
             | PLUS
             | MINUS
             | TIMES
             | DIVIDE
    '''

def p_body(p):
    '''
    body : with_multiple_defs expression with_multiple_expr
    '''

def p_with_multiple_defs(p):
    '''
    with_multiple_defs : with_multiple_defs variable_definition
                       | empty
    '''

def p_with_multiple_expr(p):
    '''
    with_multiple_expr : with_multiple_expr expression
                       | empty
    '''

def p_expression(p):
    '''
    expression : variable
               | literal
               | procedure_call
               | lambda_expression
               | conditional_expression
               | assignment
               | derived_expressions
    '''

def p_conditional_expression(p):
    '''
    condition_expression : LPAREN IF expression expression alternate RPAREN
    '''

def p_alternate(p):
    '''
    alternate : expression
              | empty
    '''

def p_assignment(p):
    '''
    assignment : LPAREN SET variable expression RPAREN
    '''

def p_literal(p):
    '''
    literal : quotation
            | self_evaluating
    '''

def p_self_evaluating(p):
    '''
    self_evaluating : BOOL
                    | num10
                    | CHAR
                    | BANNER
    '''

def p_quotation(p):
    '''
    quotation : LPAREN QUOTE datum RPAREN
              | SQUOTE datum
    '''

def p_procedure_call(p):
    '''
    procedure_call : LPAREN expression with_multiple_expr RPAREN
    '''

def p_lambda_expression(p):
    '''
    lambda_expression : LPAREN LAMBDA formals body RPAREN
    '''

def p_formals(p):
    '''
    formals : LPAREN with_multiple_vars RPAREN
            | variable
    '''

def p_inside_expr(p):
    '''
    inside_expr : QUOTE datum
                | SET variable expression
                | IF expression expression expression
    '''

def p_constant(p):
    '''
    constant : BOOLEAN
             | num10
             | CHAR
             | BANNER
    '''

def p_derived_expression(p):
    '''
    derived_expression : COND
                       | AND
                       | OR
                       | DO
    '''

def p_datum(p):
    '''
    datum : constant
          | symbol
          | list
    '''

def p_symbol(p):
    '''
    symbol : ID
    '''

def p_list(p):
    '''
    list : LPAREN with_multiple_datums RPAREN
    '''

def p_with_multiple_datums(p):
    '''
    with_multiple_datums : with_multiple_datums datum
                         | empty
    '''

def p_num10(p):
    '''
    num10 : CTEINT
          | CTEFLOAT
    '''

def p_display(p):
    '''
    display : LPAREN DISPLAY datum RPAREN
    '''

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! - {}".format(p))

parser = yacc.yacc()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if parser.parse(data) == "COMPILED ESPY":
                print("Valid input")
        except EOFError:
            print(EOFError)
    else:
        print("No file to test found")