from subprocess import check_output
from unittest import main, TestCase

from espy import create_binary

'''
    Tests.py
    Descripción: Archivo de pruebas para cada funcionalidad.
    Su finalidad es poder asegurar que al agregar nuevas funcionalidades, no genere cambios
    en las funcionalidad anteriores
    Autores: David Hernández    |   A01383543
             Bernardo García    |   A00570682
'''

"""
    Función que revisa que al correr el programa asignado, de el resultado esperado
    """
class ImmediateTest(TestCase):
    def assertEvaluatesRepr(self, program, result_repr):
        create_binary(program)
        self.assertEqual(check_output(
            ['./main']).strip().decode('utf-8'), result_repr)

    '''
    Self Evaluation
    '''    
    def test_42(self):
        self.assertEvaluatesRepr("42", "42")

    def test_0(self):
        self.assertEvaluatesRepr("0", "0")

    def test_1(self):
        self.assertEvaluatesRepr("1", "1")

    def test_neg_1(self):
        self.assertEvaluatesRepr("-1", "-1")

    def test_10(self):
        self.assertEvaluatesRepr("10", "10")

    def test_neg_10(self):
        self.assertEvaluatesRepr("-10", "-10")

    def test_2736(self):
        self.assertEvaluatesRepr("2736", "2736")

    def test_neg_2736(self):
        self.assertEvaluatesRepr("-2736", "-2736")

    def test_536870911(self):
        self.assertEvaluatesRepr("536870911", "536870911")

    def test_neg_536870911(self):
        self.assertEvaluatesRepr("-536870911", "-536870911")

    def test_bool_f(self):
        self.assertEvaluatesRepr("#f", "#f")

    def test_bool_t(self):
        self.assertEvaluatesRepr("#t", "#t")

    def test_empty_list(self):
        self.assertEvaluatesRepr("()", "()")

    def test_char_0(self):
        self.assertEvaluatesRepr("\#0", "\#0")

    def test_char_1(self):
        self.assertEvaluatesRepr("\#1", "\#1")

    def test_char_2(self):
        self.assertEvaluatesRepr("\#2", "\#2")

    def test_char_3(self):
        self.assertEvaluatesRepr("\#3", "\#3")

    def test_char_4(self):
        self.assertEvaluatesRepr("\#4", "\#4")

    def test_char_5(self):
        self.assertEvaluatesRepr("\#5", "\#5")

    def test_char_6(self):
        self.assertEvaluatesRepr("\#6", "\#6")

    def test_char_7(self):
        self.assertEvaluatesRepr("\#7", "\#7")

    def test_char_8(self):
        self.assertEvaluatesRepr("\#8", "\#8")

    def test_char_9(self):
        self.assertEvaluatesRepr("\#9", "\#9")

    def test_char_A(self):
        self.assertEvaluatesRepr("\#A", "\#A")

    def test_char_B(self):
        self.assertEvaluatesRepr("\#B", "\#B")

    def test_char_C(self):
        self.assertEvaluatesRepr("\#C", "\#C")

    def test_char_D(self):
        self.assertEvaluatesRepr("\#D", "\#D")

    def test_char_E(self):
        self.assertEvaluatesRepr("\#E", "\#E")

    def test_char_F(self):
        self.assertEvaluatesRepr("\#F", "\#F")

    def test_char_G(self):
        self.assertEvaluatesRepr("\#G", "\#G")

    def test_char_H(self):
        self.assertEvaluatesRepr("\#H", "\#H")

    def test_char_I(self):
        self.assertEvaluatesRepr("\#I", "\#I")

    def test_char_J(self):
        self.assertEvaluatesRepr("\#J", "\#J")

    def test_char_K(self):
        self.assertEvaluatesRepr("\#K", "\#K")

    def test_char_L(self):
        self.assertEvaluatesRepr("\#L", "\#L")

    def test_char_M(self):
        self.assertEvaluatesRepr("\#M", "\#M")

    def test_char_N(self):
        self.assertEvaluatesRepr("\#N", "\#N")

    def test_char_O(self):
        self.assertEvaluatesRepr("\#O", "\#O")

    def test_char_P(self):
        self.assertEvaluatesRepr("\#P", "\#P")

    def test_char_Q(self):
        self.assertEvaluatesRepr("\#Q", "\#Q")

    def test_char_R(self):
        self.assertEvaluatesRepr("\#R", "\#R")

    def test_char_S(self):
        self.assertEvaluatesRepr("\#S", "\#S")

    def test_char_T(self):
        self.assertEvaluatesRepr("\#T", "\#T")

    def test_char_U(self):
        self.assertEvaluatesRepr("\#U", "\#U")

    def test_char_V(self):
        self.assertEvaluatesRepr("\#V", "\#V")

    def test_char_W(self):
        self.assertEvaluatesRepr("\#W", "\#W")

    def test_char_X(self):
        self.assertEvaluatesRepr("\#X", "\#X")

    def test_char_Y(self):
        self.assertEvaluatesRepr("\#Y", "\#Y")

    def test_char_Z(self):
        self.assertEvaluatesRepr("\#Z", "\#Z")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#a", "\#a")

    def test_char_b(self):
        self.assertEvaluatesRepr("\#b", "\#b")

    def test_char_c(self):
        self.assertEvaluatesRepr("\#c", "\#c")

    def test_char_d(self):
        self.assertEvaluatesRepr("\#d", "\#d")

    def test_char_f(self):
        self.assertEvaluatesRepr("\#f", "\#f")

    def test_char_g(self):
        self.assertEvaluatesRepr("\#g", "\#g")

    def test_char_h(self):
        self.assertEvaluatesRepr("\#h", "\#h")

    def test_char_i(self):
        self.assertEvaluatesRepr("\#i", "\#i")

    def test_char_j(self):
        self.assertEvaluatesRepr("\#j", "\#j")

    def test_char_k(self):
        self.assertEvaluatesRepr("\#k", "\#k")

    def test_char_l(self):
        self.assertEvaluatesRepr("\#l", "\#l")

    def test_char_m(self):
        self.assertEvaluatesRepr("\#m", "\#m")

    def test_char_n(self):
        self.assertEvaluatesRepr("\#n", "\#n")

    def test_char_o(self):
        self.assertEvaluatesRepr("\#o", "\#o")

    def test_char_p(self):
        self.assertEvaluatesRepr("\#p", "\#p")

    def test_char_q(self):
        self.assertEvaluatesRepr("\#q", "\#q")

    def test_char_r(self):
        self.assertEvaluatesRepr("\#r", "\#r")

    def test_char_s(self):
        self.assertEvaluatesRepr("\#s", "\#s")

    def test_char_t(self):
        self.assertEvaluatesRepr("\#t", "\#t")

    def test_char_u(self):
        self.assertEvaluatesRepr("\#u", "\#u")

    def test_char_v(self):
        self.assertEvaluatesRepr("\#v", "\#v")

    def test_char_w(self):
        self.assertEvaluatesRepr("\#w", "\#w")

    def test_char_x(self):
        self.assertEvaluatesRepr("\#x", "\#x")

    def test_char_y(self):
        self.assertEvaluatesRepr("\#y", "\#y")

    def test_char_z(self):
        self.assertEvaluatesRepr("\#z", "\#z")
    
    '''
    Unary Primitives: Add1
    '''
    def test_add1_0(self):
        self.assertEvaluatesRepr("(add1 0)", "1")

    def test_add1_neg_1(self):
        self.assertEvaluatesRepr("(add1 -1)", "0")

    def test_add1_1(self):
        self.assertEvaluatesRepr("(add1 1)", "2")

    def test_add1_neg_100(self):
        self.assertEvaluatesRepr("(add1 -100)", "-99")

    def test_add1_1000(self):
        self.assertEvaluatesRepr("(add1 1000)", "1001")

    def test_add1_536870910(self):
        self.assertEvaluatesRepr("(add1 536870910)", "536870911")

    def test_add1_neg_536870912(self):
        self.assertEvaluatesRepr("(add1 -536870912)", "-536870911")

    def test_2_add1_0(self):
        self.assertEvaluatesRepr("(add1 (add1 0))", "2")

    def test_6_add1_12(self):
        self.assertEvaluatesRepr(
            "(add1 (add1 (add1 (add1 (add1 (add1 12))))))", "18")

    '''
    Unary Primitives: Sub1
    '''
    def test_sub1_0(self):
        self.assertEvaluatesRepr("(sub1 0)", "-1")

    def test_sub1_neg_1(self):
        self.assertEvaluatesRepr("(sub1 -1)", "-2")

    def test_sub1_1(self):
        self.assertEvaluatesRepr("(sub1 1)", "0")

    def test_sub1_neg_100(self):
        self.assertEvaluatesRepr("(sub1 -100)", "-101")

    def test_sub1_1000(self):
        self.assertEvaluatesRepr("(sub1 1000)", "999")

    def test_sub1_536870911(self):
        self.assertEvaluatesRepr("(sub1 536870911)", "536870910")

    def test_sub1_neg_536870911(self):
        self.assertEvaluatesRepr("(sub1 -536870911)", "-536870912")

    def test_2_sub1_0(self):
        self.assertEvaluatesRepr("(sub1 (sub1 0))", "-2")

    def test_6_sub1_12(self):
        self.assertEvaluatesRepr(
            "(sub1 (sub1 (sub1 (sub1 (sub1 (sub1 12))))))", "6")

    def test_sub1_add1_0(self):
        self.assertEvaluatesRepr("(sub1 (add1 0))", "0")

    '''
    Conversion functions:
    '''
    def test_num_to_char_65(self):
        self.assertEvaluatesRepr("(num->char 65)", "\#A")

    def test_num_to_char_97(self):
        self.assertEvaluatesRepr("(num->char 97)", "\#a")

    def test_num_to_char_122(self):
        self.assertEvaluatesRepr("(num->char 122)", "\#z")

    def test_num_to_char_90(self):
        self.assertEvaluatesRepr("(num->char 90)", "\#Z")

    def test_num_to_char_48(self):
        self.assertEvaluatesRepr("(num->char 48)", "\#0")

    def test_num_to_char_57(self):
        self.assertEvaluatesRepr("(num->char 57)", "\#9")

    def test_char_to_num_A(self):
        self.assertEvaluatesRepr("(char->num \#A)", "65")

    def test_char_to_num_a(self):
        self.assertEvaluatesRepr("(char->num \#a)", "97")

    def test_char_to_num_z(self):
        self.assertEvaluatesRepr("(char->num \#z)", "122")

    def test_char_to_num_Z(self):
        self.assertEvaluatesRepr("(char->num \#Z)", "90")

    def test_char_to_num_0(self):
        self.assertEvaluatesRepr("(char->num \#0)", "48")

    def test_char_to_num_9(self):
        self.assertEvaluatesRepr("(char->num \#9)", "57")

    def test_char_to_num_num_to_char_12(self):
        self.assertEvaluatesRepr("(char->num (num->char 12))", "12")

    def test_num_to_char_char_to_num_x(self):
        self.assertEvaluatesRepr("(num->char (char->num \#x))", "\#x")

    '''
    Self Type: Is_Num
    '''
    def test_is_num_0(self):
        self.assertEvaluatesRepr("(num? 0)", "#t")

    def test_is_num_1(self):
        self.assertEvaluatesRepr("(num? 1)", "#t")

    def test_is_num_neg_1(self):
        self.assertEvaluatesRepr("(num? -1)", "#t")

    def test_is_num_37287(self):
        self.assertEvaluatesRepr("(num? 37287)", "#t")

    def test_is_num_neg_23873(self):
        self.assertEvaluatesRepr("(num? -23873)", "#t")

    def test_is_num_536870911(self):
        self.assertEvaluatesRepr("(num? 536870911)", "#t")

    def test_is_num_neg_536870911(self):
        self.assertEvaluatesRepr("(num? -536870911)", "#t")

    def test_is_num_bool_t(self):
        self.assertEvaluatesRepr("(num? #t)", "#f")

    def test_is_num_bool_f(self):
        self.assertEvaluatesRepr("(num? #f)", "#f")

    def test_is_num_null(self):
        self.assertEvaluatesRepr("(num? ())", "#f")

    def test_is_num_char_Q(self):
        self.assertEvaluatesRepr("(num? \#Q)", "#f")

    def test_2_is_num_12(self):
        self.assertEvaluatesRepr("(num? (num? 12))", "#f")

    def test_2_is_num_bool_f(self):
        self.assertEvaluatesRepr("(num? (num? #f))", "#f")

    def test_2_is_num_char_a(self):
        self.assertEvaluatesRepr("(num? (num? \#A))", "#f")

    def test_is_num_char_to_num_char_r(self):
        self.assertEvaluatesRepr("(num? (char->num \#r))", "#t")

    def test_is_num_num_to_char_12(self):
        self.assertEvaluatesRepr("(num? (num->char 12))", "#f")

    '''
    Self Type: Is_Null
    '''
    def test_is_null_0(self):
        self.assertEvaluatesRepr("(null? ())", "#t")

    def test_is_null_1(self):
        self.assertEvaluatesRepr("(null? ())", "#t")

    def test_is_null_2(self):
        self.assertEvaluatesRepr("(null? ())", "#t")

    def test_is_null_3(self):
        self.assertEvaluatesRepr("(null? ())", "#t")

    def test_is_null_4(self):
        self.assertEvaluatesRepr("(null? ())", "#t")

    def test_is_null_5(self):
        self.assertEvaluatesRepr("(null? ())", "#t")

    def test_is_null_6(self):
        self.assertEvaluatesRepr("(null? ())", "#t")

    def test_is_null_7(self):
        self.assertEvaluatesRepr("(null? ())", "#t")

    '''
    Self Type: Is_bool
    '''
    def test_is_bool_0_0(self):
        self.assertEvaluatesRepr("(boolean? #t)", "#t")

    def test_is_bool_0_1(self):
        self.assertEvaluatesRepr("(boolean? #f)", "#t")

    def test_is_bool_1(self):
        self.assertEvaluatesRepr("(boolean? 0)", "#f")

    def test_is_bool_2(self):
        self.assertEvaluatesRepr("(boolean? 1)", "#f")

    def test_is_bool_3(self):
        self.assertEvaluatesRepr("(boolean? -1)", "#f")

    def test_is_bool_4(self):
        self.assertEvaluatesRepr("(boolean? ())", "#f")

    def test_is_bool_5(self):
        self.assertEvaluatesRepr("(boolean? \#a)", "#f")

    def test_is_bool_6(self):
        self.assertEvaluatesRepr("(boolean? (boolean? 0))", "#t")

    def test_is_bool_7(self):
        self.assertEvaluatesRepr("(boolean? (num? (boolean? 0)))", "#t")

    '''
    Self Type: Is_char
    '''
    def test_is_char_0(self):
        self.assertEvaluatesRepr("(char? \#a)", "#t")

    def test_is_char_1(self):
        self.assertEvaluatesRepr("(char? \#Z)", "#t")

    def test_is_char_3(self):
        self.assertEvaluatesRepr("(char? #t)", "#f")

    def test_is_char_4(self):
        self.assertEvaluatesRepr("(char? #f)", "#f")

    def test_is_char_5(self):
        self.assertEvaluatesRepr("(char? ())", "#f")

    def test_is_char_6(self):
        self.assertEvaluatesRepr("(char? (char? #t))", "#f")

    def test_is_char_7(self):
        self.assertEvaluatesRepr("(char? 0)", "#f")

    def test_is_char_8(self):
        self.assertEvaluatesRepr("(char? 23870)", "#f")

    def test_is_char_9(self):
        self.assertEvaluatesRepr("(char? -23789)", "#f")

    '''
    Conditionals: If statement
    '''
    def test_if_1(self):
        self.assertEvaluatesRepr("(if #t 12 13)", "12")

    def test_if_2(self):
        self.assertEvaluatesRepr("(if #f 12 13)", "13")

    def test_if_3(self):
        self.assertEvaluatesRepr("(if 0 12 13)", "12")

    def test_if_4(self):
        self.assertEvaluatesRepr("(if () 43 ())", "43")

    def test_if_5(self):
        self.assertEvaluatesRepr("(if #t (if 12 13 4) 17)", "13")

    def test_if_6(self):
        self.assertEvaluatesRepr("(if #f 12 (if #f 13 4))", "4")

    def test_if_7(self):
        self.assertEvaluatesRepr("(if \#X (if 1 2 3) (if 4 5 6))", "2")

    def test_if_8(self):
        self.assertEvaluatesRepr(
            "(if (not (boolean? #t)) 15 (boolean? #f))", "#t")

    def test_if_9(self):
        self.assertEvaluatesRepr(
            "(if (if (char? \#a) (boolean? \#b) (num? \#c)) 119 -23)", "-23")

    def test_if_10(self):
        self.assertEvaluatesRepr(
            "(if (if (if (not 1) (not 2) (not 3)) 4 5) 6 7)", "6")

    def test_if_11(self):
        self.assertEvaluatesRepr(
            "(if (not (if (if (not 1) (not 2) (not 3)) 4 5)) 6 7)", "7")

    def test_if_12(self):
        self.assertEvaluatesRepr(
            "(not (if (not (if (if (not 1) (not 2) (not 3)) 4 5)) 6 7))", "#f")

    def test_if_13(self):
        self.assertEvaluatesRepr("(if (char? 12) 13 14)", "14")

    def test_if_14(self):
        self.assertEvaluatesRepr("(if (char? \#a) 13 14)", "13")

    def test_if_15(self):
        self.assertEvaluatesRepr("(add1 (if (sub1 1) (sub1 13) 14))", "13")
    
    '''
    Aritmethic operations: +
    '''
    def test_add_1(self):
        self.assertEvaluatesRepr("(+ 1 2)",  "3")
    
    def test_add_2(self):
        self.assertEvaluatesRepr("(+ 1 -2)",  "-1")
    
    def test_add_3(self):
        self.assertEvaluatesRepr("(+ -1 2)",  "1")
    
    def test_add_4(self):
        self.assertEvaluatesRepr("(+ -1 -2)",  "-3")
    
    def test_add_5(self):
        self.assertEvaluatesRepr("(+ 536870911 -1)",  "536870910")
    
    def test_add_6(self):
        self.assertEvaluatesRepr("(+ 536870910 1)",  "536870911")
    
    def test_add_7(self):
        self.assertEvaluatesRepr("(+ -536870912 1)",  "-536870911")
    
    def test_add_8(self):
        self.assertEvaluatesRepr("(+ -536870911 -1)",  "-536870912")
    
    def test_add_9(self):
        self.assertEvaluatesRepr("(+ 536870911 -536870912)",  "-1")
    
    def test_add_10(self):
        self.assertEvaluatesRepr("(+ 1 (+ 2 3))",  "6")
    
    def test_add_11(self):
        self.assertEvaluatesRepr("(+ 1 (+ 2 -3))",  "0")
    
    def test_add_12(self):
        self.assertEvaluatesRepr("(+ 1 (+ -2 3))",  "2")
    
    def test_add_13(self):
        self.assertEvaluatesRepr("(+ 1 (+ -2 -3))",  "-4")
    
    def test_add_14(self):
        self.assertEvaluatesRepr("(+ -1 (+ 2 3))",  "4")
    
    def test_add_15(self):
        self.assertEvaluatesRepr("(+ -1 (+ 2 -3))",  "-2")
    
    def test_add_16(self):
        self.assertEvaluatesRepr("(+ -1 (+ -2 3))",  "0")
    
    def test_add_17(self):
        self.assertEvaluatesRepr("(+ -1 (+ -2 -3))",  "-6")
    
    def test_add_18(self):
        self.assertEvaluatesRepr("(+ (+ 1 2) 3)",  "6")
    
    def test_add_19(self):
        self.assertEvaluatesRepr("(+ (+ 1 2) -3)",  "0")
    
    def test_add_20(self):
        self.assertEvaluatesRepr("(+ (+ 1 -2) 3)",  "2")
    
    def test_add_21(self):
        self.assertEvaluatesRepr("(+ (+ 1 -2) -3)",  "-4")
    
    def test_add_22(self):
        self.assertEvaluatesRepr("(+ (+ -1 2) 3)",  "4")
    
    def test_add_23(self):
        self.assertEvaluatesRepr("(+ (+ -1 2) -3)",  "-2")
    
    def test_add_24(self):
        self.assertEvaluatesRepr("(+ (+ -1 -2) 3)",  "0")
    
    def test_add_25(self):
        self.assertEvaluatesRepr("(+ (+ -1 -2) -3)",  "-6")
    
    def test_add_26(self):
        self.assertEvaluatesRepr("(+ (+ (+ (+ (+ (+ (+ (+ 1 2) 3) 4) 5) 6) 7) 8) 9)",  "45")
    
    def test_add_27(self):
        self.assertEvaluatesRepr("(+ 1 (+ 2 (+ 3 (+ 4 (+ 5 (+ 6 (+ 7 (+ 8 9))))))))",  "45")
    
    def test_add_28(self):
        self.assertEvaluatesRepr("(+ 1 2 (- 5 7) 15 (+ 40 10 (+ 5 (+ 5 10 (- 10 5)) 5 (- 10 2))) 7 9 (+ 2 3 (- 10 5 2) 5 (+ 4 5)))",  "142")
    '''
    Aritmethic operations: -
    '''
    def test_sub_1(self):
        self.assertEvaluatesRepr("(- 1 2)", "-1")
    
    def test_sub_2(self):
        self.assertEvaluatesRepr("(- 1 -2)", "3")
    
    def test_sub_3(self):
        self.assertEvaluatesRepr("(- -1 2)", "-3")
    
    def test_sub_4(self):
        self.assertEvaluatesRepr("(- -1 -2)", "1")
    
    def test_sub_5(self):
        self.assertEvaluatesRepr("(- 536870910 -1)", "536870911")
    
    def test_sub_6(self):
        self.assertEvaluatesRepr("(- 536870911 1)", "536870910")
    
    def test_sub_7(self):
        self.assertEvaluatesRepr("(- -536870911 1)", "-536870912")
    
    def test_sub_8(self):
        self.assertEvaluatesRepr("(- -536870912 -1)", "-536870911")
    
    def test_sub_9(self):
        self.assertEvaluatesRepr("(- 1 536870911)", "-536870910")
    
    def test_sub_10(self):
        self.assertEvaluatesRepr("(- -1 536870911)", "-536870912")
    
    def test_sub_11(self):
        self.assertEvaluatesRepr("(- 1 -536870910)", "536870911")
    
    def test_sub_12(self):
        self.assertEvaluatesRepr("(- -1 -536870912)", "536870911")
    
    def test_sub_13(self):
        self.assertEvaluatesRepr("(- 536870911 536870911)", "0")
    
    def test_sub_14(self):
        self.assertEvaluatesRepr("(- 536870911 -536870912)", "-1")
    
    def test_sub_15(self):
        self.assertEvaluatesRepr("(- -536870911 -536870912)", "1")
    
    def test_sub_16(self):
        self.assertEvaluatesRepr("(- 1 (- 2 3))", "2")
    
    def test_sub_17(self):
        self.assertEvaluatesRepr("(- 1 (- 2 -3))", "-4")
    
    def test_sub_18(self):
        self.assertEvaluatesRepr("(- 1 (- -2 3))", "6")
    
    def test_sub_19(self):
        self.assertEvaluatesRepr("(- 1 (- -2 -3))", "0")
    
    def test_sub_20(self):
        self.assertEvaluatesRepr("(- -1 (- 2 3))", "0")
    
    def test_sub_21(self):
        self.assertEvaluatesRepr("(- -1 (- 2 -3))", "-6")
    
    def test_sub_22(self):
        self.assertEvaluatesRepr("(- -1 (- -2 3))", "4")
    
    def test_sub_23(self):
        self.assertEvaluatesRepr("(- -1 (- -2 -3))", "-2")
    
    def test_sub_24(self):
        self.assertEvaluatesRepr("(- 0 (- -2 -3))", "-1")
    
    def test_sub_25(self):
        self.assertEvaluatesRepr("(- (- 1 2) 3)", "-4")
    
    def test_sub_26(self):
        self.assertEvaluatesRepr("(- (- 1 2) -3)", "2")
    
    def test_sub_27(self):
        self.assertEvaluatesRepr("(- (- 1 -2) 3)", "0")
    
    def test_sub_28(self):
        self.assertEvaluatesRepr("(- (- 1 -2) -3)", "6")
    
    def test_sub_29(self):
        self.assertEvaluatesRepr("(- (- -1 2) 3)", "-6")
    
    def test_sub_30(self):
        self.assertEvaluatesRepr("(- (- -1 2) -3)", "0")
    
    def test_sub_31(self):
        self.assertEvaluatesRepr("(- (- -1 -2) 3)", "-2")
    
    def test_sub_32(self):
        self.assertEvaluatesRepr("(- (- -1 -2) -3)", "4")
    
    def test_sub_33(self):
        self.assertEvaluatesRepr("(- (- (- (- (- (- (- (- 1 2) 3) 4) 5) 6) 7) 8) 9)", "-43")
    
    def test_sub_34(self):
        self.assertEvaluatesRepr("(- 1 (- 2 (- 3 (- 4 (- 5 (- 6 (- 7 (- 8 9))))))))", "5")
    
    '''
    Aritmethic operations: *
    '''
    def test_mult_1(self):
        self.assertEvaluatesRepr("(* 2 3)", "6")
    
    def test_mult_2(self):
        self.assertEvaluatesRepr("(* 2 -3)", "-6")
    
    def test_mult_3(self):
        self.assertEvaluatesRepr("(* -2 3)", "-6")
    
    def test_mult_4(self):
        self.assertEvaluatesRepr("(* -2 -3)", "6")
    
    def test_mult_5(self):
        self.assertEvaluatesRepr("(* 536870911 1)", "536870911")
    
    def test_mult_6(self):
        self.assertEvaluatesRepr("(* 536870911 -1)", "-536870911")
    
    def test_mult_7(self):
        self.assertEvaluatesRepr("(* -536870912 1)", "-536870912")
    
    def test_mult_8(self):
        self.assertEvaluatesRepr("(* -536870911 -1)", "536870911")
    
    def test_mult_9(self):
        self.assertEvaluatesRepr("(* 2 (* 3 4))", "24")
    
    def test_mult_10(self):
        self.assertEvaluatesRepr("(* (* 2 3) 4)", "24")
    
    def test_mult_11(self):
        self.assertEvaluatesRepr("(* (* (* (* (* 2 3) 4) 5) 6) 7)", "5040")
    
    def test_mult_12(self):
        self.assertEvaluatesRepr("(* 2 (* 3 (* 4 (* 5 (* 6 7)))))", "5040"    )
    
    '''
    Aritmethic operations: /
    '''

    def test_div_1(self):
        self.assertEvaluatesRepr("(/ 10 2)", "5")
    
    def test_div_2(self):
        self.assertEvaluatesRepr("(/ 100 50)", "2")
    
    # def test_div_3(self):
    #     self.assertEvaluatesRepr("(/ -1000 30)", "-33")
    
    # def test_div_4(self):
    #     self.assertEvaluatesRepr("(/ 248 -2)", "124")
    
    def test_div_5(self):
        self.assertEvaluatesRepr("(/ 536870911 1)", "536870911")
    
    def test_div_7(self):
        self.assertEvaluatesRepr("(/ -536870911 1)", "-536870911")
    
    def test_div_9(self):
        self.assertEvaluatesRepr("(/ 33 (/ 12 4))", "11")
    
    def test_div_10(self):
        self.assertEvaluatesRepr("(/ (/ 3 1) 1)", "3")
    
    def test_div_11(self):
        self.assertEvaluatesRepr("(/ (/ (/ (/ (/ 1000 2) 5) 3) 3) 11)", "1")
    
    '''
    Boolean: Not
    '''
    def test_not_t(self):
        self.assertEvaluatesRepr("(not #t)", "#f")

    def test_not_f(self):
        self.assertEvaluatesRepr("(not #f)", "#t")

    def test_not_15(self):
        self.assertEvaluatesRepr("(not 15)", "#f")

    def test_not_null(self):
        self.assertEvaluatesRepr("(not ())", "#f")

    def test_not_A(self):
        self.assertEvaluatesRepr("(not \#A)", "#f")

    def test_2_not_t(self):
        self.assertEvaluatesRepr("(not (not #t))", "#t")

    def test_2_not_f(self):
        self.assertEvaluatesRepr("(not (not #f))", "#f")

    def test_2_not_15(self):
        self.assertEvaluatesRepr("(not (not 15))", "#t")

    def test_not_num_15(self):
        self.assertEvaluatesRepr("(not (num? 15))", "#f")

    def test_not_num_f(self):
        self.assertEvaluatesRepr("(not (num? #f))", "#t")
    '''
    Comparison: >
    '''
    def test_gt_1(self):
        self.assertEvaluatesRepr("(> 2 4)", "#f")
    # def test_gt_3(self):
        # self.assertEvaluatesRepr("(> -1 -2)", "#t")
    def test_gt_4(self):
        self.assertEvaluatesRepr("(> 10 10)", "#f")
    
    # Funciones de error: Deben regresar un error
    # def test_gt_5(self):
    #     self.assertEvaluatesRepr("(> #t 1)", "#t")
    # def test_gt_6(self):
    #     self.assertEvaluatesRepr("(> #t #f)", "#f")
    # def test_gt_7(self):
    #     self.assertEvaluatesRepr("(> \#A \#B)", "#f")

    '''
    Comparison: <
    '''
    def test_lt_1(self):
        self.assertEvaluatesRepr("(< 2 4)", "#t")
    # def test_lt_3(self):
    #     self.assertEvaluatesRepr("(< -1 -2)", "#f")
    def test_lt_4(self):
        self.assertEvaluatesRepr("(< 10 10)", "#f")
    
    # Funciones de error: Deben regresar un error
    # def test_lt_5(self):
        # self.assertEvaluatesRepr("(< #t 1)", "#f")
    # def test_lt_6(self):
    #     self.assertEvaluatesRepr("(< #t #f)", "#f")
    # def test_lt_7(self):
    #     self.assertEvaluatesRepr("(< \#A \#B)", "#f")
    '''
    Comparison: >=
    '''
    def test_ge_1(self):
        self.assertEvaluatesRepr("(>= 2 4)", "#f")
    # def test_ge_3(self):
        # self.assertEvaluatesRepr("(>= -1 -2)", "#t")
    def test_ge_4(self):
        self.assertEvaluatesRepr("(>= 10 10)", "#t")
    
    # Funciones de error: Deben regresar un error
    # def test_ge_5(self):
        # self.assertEvaluatesRepr("(>= #f 0)", "#f")
    # def test_ge_6(self):
    #     self.assertEvaluatesRepr("(>= #t #f)", "#t")
    # def test_ge_7(self):
    #     self.assertEvaluatesRepr("(>= \#A \#B)", "#f")
    '''
    Comparison: <=
    '''
    def test_le_1(self):
        self.assertEvaluatesRepr("(<= 2 4)", "#t")
    # def test_le_3(self):
        # self.assertEvaluatesRepr("(<= -1 -2)", "#f")
    def test_le_4(self):
        self.assertEvaluatesRepr("(<= 10 10)", "#t")
    
    # Funciones de error: Deben regresar un error
    # # def test_le_5(self):
    #     self.assertEvaluatesRepr("(<= #t 1)", "#f")
    # def test_le_6(self):
    #     self.assertEvaluatesRepr("(<= #t #f)", "#f")
    # def test_le_7(self):
    #     self.assertEvaluatesRepr("(<= \#A \#B)", "#f")
    '''
    Comparison: ==
    '''
    def test_eq_1(self):
        self.assertEvaluatesRepr("(== 2 4)", "#f")
    # def test_eq_3(self):
        # self.assertEvaluatesRepr("(== -5 -5)", "#t")
    def test_eq_4(self):
        self.assertEvaluatesRepr("(== 10 10)", "#t")
    
    # Funciones de error: Deben regresar un error
    # def test_eq_5(self):
        # self.assertEvaluatesRepr("(== #f 0)", "#f")
    # def test_eq_6(self):
    #     self.assertEvaluatesRepr("(== #t #t)", "#t")
    # def test_eq_7(self):
    #     self.assertEvaluatesRepr("(== \#A \#A)", "#t")
    # def test_eq_8(self):
    #     self.assertEvaluatesRepr("(== \#A \#B)", "#f")
    '''
    Boolean: And/Or
    '''
    # def test_and_1(self):
    #     self.assertEvaluatesRepr("(and)", "#t")


    # def test_and_2(self):
    #     self.assertEvaluatesRepr("(and 5)", "5")


    # def test_and_3(self):
    #     self.assertEvaluatesRepr("(and #f)", "#f")


    # def test_and_4(self):
    #     self.assertEvaluatesRepr("(and 5 6)", "6")


    # def test_or_1(self):
    #     self.assertEvaluatesRepr("(or)", "#f")


    # def test_or_2(self):
    #     self.assertEvaluatesRepr("(or #t)", "#t")


    # def test_or_3(self):
    #     self.assertEvaluatesRepr("(or 5)", "5")


    # def test_or_4(self):
    #     self.assertEvaluatesRepr("(or 1 2 3)", "1")

    '''
    Functions: Let\Letrec
    '''
    def test_let_1(self):
        self.assertEvaluatesRepr("(let ([x 5]) x)", "5")

    def test_let_2(self):
        self.assertEvaluatesRepr("(let ([x (+ 1 2)]) x)", "3")
    
    def test_let_3(self):
        self.assertEvaluatesRepr("(let ([x (+ 1 2)]) (let ([y (+ 3 4)]) (+ x y)))", "10")
    
    def test_let_4(self):
        self.assertEvaluatesRepr("(let ([x (+ 1 2)]) (let ([y (+ 3 4)]) (- y x)))", "4")
    
    def test_let_5(self):
        self.assertEvaluatesRepr("(let ([x (+ 1 2)] [y (+ 3 4)]) (- y x))", "4")
    
    def test_let_6(self):
        self.assertEvaluatesRepr("(let ([x (let ([y (+ 1 2)]) (* y y))]) (+ x x))", "18")
    
    def test_let_7(self):
        self.assertEvaluatesRepr("(let ([x (+ 1 2)]) (let ([x (+ 3 4)]) x))", "7")
    
    def test_let_8(self):
        self.assertEvaluatesRepr("(let ([x (+ 1 2)]) (let ([x (+ x 4)]) x))", "7")
    
    def test_let_9(self):
        self.assertEvaluatesRepr("(let ([t (let ([t (let ([t (let ([t (+ 1 2)]) t)]) t)]) t)]) t)", "3")
    
    def test_let_10(self):
        self.assertEvaluatesRepr("(let ([x 12]) (let ([x (+ x x)]) (let ([x (+ x x)]) (let ([x (+ x x)]) (+ x x)))))", "192")
    
    def test_def_1(self):
        self.assertEvaluatesRepr("(def () 12)", "12")

    def test_def_2(self):
        self.assertEvaluatesRepr("(def () (let ([x 5]) (+ x x)))", "10")

    def test_def_3(self):
        self.assertEvaluatesRepr("(def ([f (lambda () 5)]) 7)", "7")

    def test_def_4(self):
        self.assertEvaluatesRepr("(def ([f (lambda () 5)]) (let ([x 12]) x))", "12")

    def test_def_5(self):
        self.assertEvaluatesRepr("(def ([f (lambda () 5)]) (f))", "5")

    def test_def_6(self):
        self.assertEvaluatesRepr("(def ([f (lambda () 5)]) (let ([x (f)]) x))", "5")

    def test_def_7(self):
        self.assertEvaluatesRepr("(def ([f (lambda () 5)]) (+ (f) 6))", "11")

    def test_def_8(self):
        self.assertEvaluatesRepr("(def ([f (lambda () 5)]) (+ 6 (f)))", "11")

    def test_def_9(self):
        self.assertEvaluatesRepr("(def ([f (lambda () 5)]) (- 20 (f)))", "15")

    def test_def_10(self):
        self.assertEvaluatesRepr("(def ([f (lambda () 5)]) (+ (f) (f)))", "10")

    def test_def_11(self):
        self.assertEvaluatesRepr("(def ([f (lambda () (+ 5 7))] [g (lambda () 13)]) (+ (f) (g)))", "25")

    def test_def_12(self):
        self.assertEvaluatesRepr("(def ([f (lambda (x) (+ x 12))]) (f 13))", "25")

    def test_def_13(self):
        self.assertEvaluatesRepr("(def ([f (lambda (x) (+ x 12))]) (f (f 10)))", "34")

    def test_def_14(self):
        self.assertEvaluatesRepr("(def ([f (lambda (x) (+ x 12))]) (f (f (f 0))))", "36")

    def test_def_15(self):
        self.assertEvaluatesRepr("(def ([f (lambda (x y) (+ x y))] [g (lambda (x) (+ x 12))]) (f 16 (f (g 0) (+ 1 (g 0)))))", "41")

    def test_def_16(self):
        self.assertEvaluatesRepr("(def ([g (lambda (x y) (+ x y))] [f (lambda (x) (g x x))]) (f 12))", "24")

    def test_def_17(self):
        self.assertEvaluatesRepr("(def ([f (lambda (x) (if (zero? x) 1 (* x (f (sub1 x)))))]) (f 5))", "120")

    def test_def_18(self):
        self.assertEvaluatesRepr("(def ([f (lambda (x acc) (if (zero? x) acc (f (sub1 x) (* acc x))))]) (f 5 1))", "120")

    def test_def_19_1(self):
        self.assertEvaluatesRepr("(def ([f (lambda (x) (if (zero? x) 0 (+ 1 (f (sub1 x)))))]) (f 63))", "63")
    
    def test_fibonacci_rec(self):
        self.assertEvaluatesRepr("(def ([fib (lambda (x) (if (<= x 2) 1 (+ 0 (fib (- x 1))(fib (- x 2)))))]) (fib 6))", "8")
    
    def test_fibonacci_iterativo(self):
        self.assertEvaluatesRepr("(def ([fib (lambda (n r1 r2) (if (< n 2) r2 (fib (- n 1) r2 (+ r1 r2))))]) (fib 6 0 1))", "8")
    
    def test_factorial_rec(self):
        self.assertEvaluatesRepr("(def ([fact (lambda (n) (if (== n 0) 1 (* n (fact (- n 1)))))]) (fact 3))", "6")
    
if __name__ == '__main__':
    main()

