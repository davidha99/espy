from subprocess import check_output
from unittest import main, TestCase

from compiler import create_binary

class ImmediateTest(TestCase):
    def assertEvaluatesRepr(self, program, result_repr):
        """Assert that the given program, when compiled and executed, writes
        result_repr to stdout.

        """
        create_binary(program)
        self.assertEqual(check_output(['./main']).strip().decode('utf-8'), result_repr)
    
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

    def test_char_a(self):
        self.assertEvaluatesRepr("\#b", "\#b")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#c", "\#c")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#d", "\#d")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#f", "\#f")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#g", "\#g")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#h", "\#h")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#i", "\#i")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#j", "\#j")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#k", "\#k")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#l", "\#l")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#m", "\#m")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#n", "\#n")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#o", "\#o")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#p", "\#p")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#q", "\#q")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#r", "\#r")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#s", "\#s")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#t", "\#t")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#u", "\#u")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#v", "\#v")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#w", "\#w")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#x", "\#x")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#y", "\#y")

    def test_char_a(self):
        self.assertEvaluatesRepr("\#z", "\#z")
    
    def test_fxadd1_0(self):
        self.assertEvaluatesRepr("(fxadd1 0)", "1")
    
    def test_fxadd1_neg_1(self):
        self.assertEvaluatesRepr("(fxadd1 -1)", "0")
    
    def test_fxadd1_1(self):
        self.assertEvaluatesRepr("(fxadd1 1)", "2")
    
    def test_fxadd1_neg_100(self):
        self.assertEvaluatesRepr("(fxadd1 -100)", "-99")
    
    def test_fxadd1_1000(self):
        self.assertEvaluatesRepr("(fxadd1 1000)", "1001")
    
    def test_fxadd1_536870910(self):
        self.assertEvaluatesRepr("(fxadd1 536870910)", "536870911")
    
    def test_fxadd1_neg_536870912(self):
        self.assertEvaluatesRepr("(fxadd1 -536870912)", "-536870911")
    
    def test_2_fxadd1_0(self):
        self.assertEvaluatesRepr("(fxadd1 (fxadd1 0))", "2")
    
    def test_6_fxadd1_12(self):
        self.assertEvaluatesRepr("(fxadd1 (fxadd1 (fxadd1 (fxadd1 (fxadd1 (fxadd1 12))))))", "18")
    
    def test_fxsub1_0(self):
        self.assertEvaluatesRepr("(fxsub1 0)", "-1")
    
    def test_fxsub1_neg_1(self):
        self.assertEvaluatesRepr("(fxsub1 -1)", "-2")
    
    def test_fxsub1_1(self):
        self.assertEvaluatesRepr("(fxsub1 1)", "0")
    
    def test_fxsub1_neg_100(self):
        self.assertEvaluatesRepr("(fxsub1 -100)", "-101")
    
    def test_fxsub1_1000(self):
        self.assertEvaluatesRepr("(fxsub1 1000)", "999")
    
    def test_fxsub1_536870911(self):
        self.assertEvaluatesRepr("(fxsub1 536870911)", "536870910")
    
    def test_fxsub1_neg_536870911(self):
        self.assertEvaluatesRepr("(fxsub1 -536870911)", "-536870912")
    
    def test_2_fxsub1_0(self):
        self.assertEvaluatesRepr("(fxsub1 (fxsub1 0))", "-2")
    
    def test_6_fxsub1_12(self):
        self.assertEvaluatesRepr("(fxsub1 (fxsub1 (fxsub1 (fxsub1 (fxsub1 (fxsub1 12))))))", "6")
    
    def test_fxsub1_fxadd1_0(self):
        self.assertEvaluatesRepr("(fxsub1 (fxadd1 0))", "0")
    
    def test_fixnum_to_char_65(self):
        self.assertEvaluatesRepr("(fixnum->char 65)", "\#A")
    
    def test_fixnum_to_char_97(self):
        self.assertEvaluatesRepr("(fixnum->char 97)", "\#a")

    def test_fixnum_to_char_122(self):
        self.assertEvaluatesRepr("(fixnum->char 122)", "\#z")

    def test_fixnum_to_char_90(self):
        self.assertEvaluatesRepr("(fixnum->char 90)", "\#Z")

    def test_fixnum_to_char_48(self):
        self.assertEvaluatesRepr("(fixnum->char 48)", "\#0")

    def test_fixnum_to_char_57(self):
        self.assertEvaluatesRepr("(fixnum->char 57)", "\#9")

    def test_char_to_fixnum_A(self):
        self.assertEvaluatesRepr("(char->fixnum \#A)", "65")

    def test_char_to_fixnum_a(self):
        self.assertEvaluatesRepr("(char->fixnum \#a)", "97")

    def test_char_to_fixnum_z(self):
        self.assertEvaluatesRepr("(char->fixnum \#z)", "122")

    def test_char_to_fixnum_Z(self):
        self.assertEvaluatesRepr("(char->fixnum \#Z)", "90")

    def test_char_to_fixnum_0(self):
        self.assertEvaluatesRepr("(char->fixnum \#0)", "48")

    def test_char_to_fixnum_9(self):
        self.assertEvaluatesRepr("(char->fixnum \#9)", "57")

    def test_char_to_fixnum_fixnum_to_char_12(self):
        self.assertEvaluatesRepr("(char->fixnum (fixnum->char 12))", "12")

    def test_fixnum_to_char_char_to_fixnum_x(self):
        self.assertEvaluatesRepr("(fixnum->char (char->fixnum \#x))", "\#x")
    
    def test_is_fixnum_0(self):
        self.assertEvaluatesRepr("(fixnum? 0)", "#t")
    
    def test_is_fixnum_1(self):
        self.assertEvaluatesRepr("(fixnum? 1)", "#t")
    
    def test_is_fixnum_neg_1(self):
        self.assertEvaluatesRepr("(fixnum? -1)", "#t")
    
    def test_is_fixnum_37287(self):
        self.assertEvaluatesRepr("(fixnum? 37287)", "#t")
    
    def test_is_fixnum_neg_23873(self):
        self.assertEvaluatesRepr("(fixnum? -23873)", "#t")
    
    def test_is_fixnum_536870911(self):
        self.assertEvaluatesRepr("(fixnum? 536870911)", "#t")
    
    def test_is_fixnum_neg_536870911(self):
        self.assertEvaluatesRepr("(fixnum? -536870911)", "#t")
    
    def test_is_fixnum_bool_t(self):
        self.assertEvaluatesRepr("(fixnum? #t)", "#f")
    
    def test_is_fixnum_bool_f(self):
        self.assertEvaluatesRepr("(fixnum? #f)", "#f")
    
    def test_is_fixnum_null(self):
        self.assertEvaluatesRepr("(fixnum? ())", "#f")
    
    def test_is_fixnum_char_Q(self):
        self.assertEvaluatesRepr("(fixnum? \#Q)", "#f")
    
    def test_2_is_fixnum_12(self):
        self.assertEvaluatesRepr("(fixnum? (fixnum? 12))", "#f")
    
    def test_2_is_fixnum_bool_f(self):
        self.assertEvaluatesRepr("(fixnum? (fixnum? #f))", "#f")
    
    def test_2_is_fixnum_char_a(self):
        self.assertEvaluatesRepr("(fixnum? (fixnum? \#A))", "#f")
    
    def test_is_fixnum_char_to_fixnum_char_r(self):
        self.assertEvaluatesRepr("(fixnum? (char->fixnum \#r))", "#t")
    
    def test_is_fixnum_fixnum_to_char_12(self):
        self.assertEvaluatesRepr("(fixnum? (fixnum->char 12))", "#f")
    
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

    def test_not_fixnum_15(self):
        self.assertEvaluatesRepr("(not (fixnum? 15))", "#f")

    def test_not_fixnum_f(self):
        self.assertEvaluatesRepr("(not (fixnum? #f))", "#t")

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
        self.assertEvaluatesRepr("(if (not (boolean? #t)) 15 (boolean? #f))", "#t")
    
    def test_if_9(self):
        self.assertEvaluatesRepr("(if (if (char? \#a) (boolean? \#b) (fixnum? \#c)) 119 -23)", "-23")
    
    def test_if_10(self):
        self.assertEvaluatesRepr("(if (if (if (not 1) (not 2) (not 3)) 4 5) 6 7)", "6")
    
    def test_if_11(self):
        self.assertEvaluatesRepr("(if (not (if (if (not 1) (not 2) (not 3)) 4 5)) 6 7)", "7")
    
    def test_if_12(self):
        self.assertEvaluatesRepr("(not (if (not (if (if (not 1) (not 2) (not 3)) 4 5)) 6 7))", "#f")
    
    def test_if_13(self):
        self.assertEvaluatesRepr("(if (char? 12) 13 14)", "14")
    
    def test_if_14(self):
        self.assertEvaluatesRepr("(if (char? \#a) 13 14)", "13")
    
    def test_if_15(self):
        self.assertEvaluatesRepr("(fxadd1 (if (fxsub1 1) (fxsub1 13) 14))", "13")    
    
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

if __name__ == '__main__':
    main()