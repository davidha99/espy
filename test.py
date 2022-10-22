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


if __name__ == '__main__':
    main()