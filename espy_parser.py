# ESPY parser

import ply.yacc as yacc
# import sys
from espy_lexer import tokens
from espy_symbol_table import *

stack = Stack_ST()

# ---------- Initial definitions ----------
def p_program(p):
    '''
    program : main
    '''
    p[0] = p[1]

def p_main(p):
    '''
    main : LPAREN MAIN form with_multiple_forms RPAREN
    '''

def p_form(p):
    '''
    form : variable_definition
         | expression
    '''

def p_with_multiple_forms(p):
    '''
    with_multiple_forms : with_multiple_forms form
                        | empty
    '''

def p_variable_definition(p):
    '''
    variable_definition : LPAREN DEFINE inside_var_def RPAREN
    '''

def p_with_multiple_defs(p):
    '''
    with_multiple_defs : with_multiple_defs variable_definition
                       | empty
    '''

def p_inside_var_def(p):
    '''
    inside_var_def : variable add_func_no_params expression
                   | LPAREN variable with_multiple_vars add_func_params RPAREN body
    '''

def p_add_func_no_params(p):
    "add_func_no_params :"
    stack.scope_enter(p[-1])

def p_add_func_params(p):
    "add_func_params :"


def p_variable(p):
    '''
    variable : ID
    '''

def p_with_multiple_vars(p):
    '''
    with_multiple_vars : with_multiple_vars variable
                       | empty
    '''

def p_body(p):
    '''
    body : with_multiple_defs expression with_multiple_expr
    '''

# ---------- Expressions ----------
def p_expression(p):
    '''
    expression : variable
               | literal
               | procedure_call
               | lambda_expression
               | conditional_expression
               | assignment
               | derived_expression
               | display
    '''

def p_with_multiple_expr(p):
    '''
    with_multiple_expr : with_multiple_expr expression
                       | empty
    '''

def p_literal(p):
    '''
    literal : quotation
            | self_evaluating
    '''

def p_quotation(p):
    '''
    quotation : LPAREN QUOTE datum RPAREN
              | SQUOTE datum
    '''

def p_self_evaluating(p):
    '''
    self_evaluating : BOOLEAN
                    | num10
                    | CHAR
                    | BANNER
    '''

def p_procedure_call(p):
    '''
    procedure_call : LPAREN operator with_multiple_operands RPAREN
    '''

def p_operator(p):
    '''
    operator : expression
    '''

def p_operand(p):
    '''
    operand : expression 
    '''

def p_with_multiple_operands(p):
    '''
    with_multiple_operands : with_multiple_operands operand
                           | empty 
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

def p_conditional_expression(p):
    '''
    conditional_expression : LPAREN IF test check_test consequent alternate RPAREN
    '''

def p_test(p):
    '''
    test : expression
    '''

def p_check_test(p):
    "check_test :"
    # Check if test is boolean
    # condition = stack_operands.pop()
    # condition_type = stack_types.pop()
    # if condition_type != bool:
    #   return Error.Type_Mismatch
    # else:
    #   generate_quadruple
    print("Test checked")

def p_consequent(p):
    '''
    consequent : expression
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

def p_display(p):
    '''
    display : LPAREN DISPLAY datum RPAREN
    '''

# def p_constant(p):
#     '''
#     constant : BOOLEAN
#              | num10
#              | CHAR
#              | BANNER
#     '''

# ---------- Derived Expressions ----------
def p_derived_expression(p):
    '''
    derived_expression : and_expression
                       | or_expression
                       | cond_expression
                       | do_expression
    '''

def p_and_expression(p):
    '''
    and_expression : LPAREN AND with_multiple_expr RPAREN
    '''

def p_or_expression(p):
    '''
    or_expression : LPAREN OR with_multiple_expr RPAREN
    '''

def p_cond_expression(p):
    '''
    cond_expression : LPAREN COND cond_clause with_multiple_cond_clause RPAREN
    '''

def p_cond_clause(p):
    '''
    cond_clause : LPAREN test sequence RPAREN
    '''

def p_with_multiple_cond_clause(p):
    '''
    with_multiple_cond_clause : with_multiple_cond_clause cond_clause
                              | empty
    '''

def p_sequence(p):
    '''
    sequence : with_multiple_commands expression
    '''

def p_command(p):
    '''
    command : expression
    '''

def p_with_multiple_commands(p):
    '''
    with_multiple_commands : with_multiple_commands command
                           | empty  
    '''

def p_do_expression(p):
    '''
    do_expression : LPAREN DO LPAREN iteration_spec RPAREN LPAREN test sequence RPAREN with_multiple_commands RPAREN
    '''

def p_iteration_spec(p):
    '''
    iteration_spec : LPAREN variable init step RPAREN
                   | LPAREN variable init RPAREN
    '''

# def p_with_multiple_iteration_specs(p):
#     '''
#     with_multiple_iteration_specs : with_multiple_iteration_specs iteration_spec
#                                   | empty
#     '''

def p_init(p): 
    '''
    init : expression
    '''

def p_step(p):
    '''
    step : expression
    '''

# ---------- Datums ----------
def p_datum(p):
    '''
    datum : simple_datum
          | compound_datum
    '''

def p_simple_datum(p):
    '''
    simple_datum : BOOLEAN
                 | num10
                 | CHAR
                 | BANNER
                 | symbol
    '''

def p_compound_datum(p):
    '''
    compound_datum : list
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

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! - {}".format(p))

# parser = yacc.yacc()

# if __name__ == '__main__':

#     if len(sys.argv) > 1:
#         file = sys.argv[1]
#         try:
#             f = open(file, 'r')
#             data = f.read()
#             f.close()
#             if parser.parse(data) == "COMPILED ESPY":
#                 print("Valid input")
#         except EOFError:
#             print(EOFError)
#     else:
#         print("No file to test found")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('espy > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)