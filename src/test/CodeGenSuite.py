import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    # def test_int(self):
    #     """Simple program: int main() {} """
    #     input = """void main() {putInt(100);}"""
    #     expect = "100"
    #     self.assertTrue(TestCodeGen.test(input,expect,500))
    # def test_int_ast(self):
    # 	input = Program([
    # 		FuncDecl(Id("main"),[],VoidType(),Block([],[
    # 			CallExpr(Id("putInt"),[IntLiteral(5)])]))])
    #     expect = "5"
    #     self.assertTrue(TestCodeGen.test(input,expect,501))
        
    def test_500(self):
        input = """
            Class Program {
                Var a: Int = 10;
                main(args: Array[String, 1]) {
                }
            }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 500))

    def test_501(self):
        input = """
            Class Program {
                Var $a: Int = 10;
                main(args: Array[String, 1]) {
                }
            }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 501))

    def test_502(self):
        input = """
            Class Program {
                main(args: Array[String, 1]) {
                    Var a, b: Int;
                    Var c: Int = 10;
                }
            }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 502))

    def test_503(self):
        input = """
            Class Program {
                main(args: Array[String, 1]) {
                    Var a: Int;
                }
                sum(a, b: Int) {
                }
            }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 503))

    def test_504(self):
        input = """
            Class A {
                
            }
            Class Program {
                main(args: Array[String, 1]) {
                    Var a: Int;
                }
                sum(a, b: Int) {
                }
            }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 504))

    def test_505(self):
        input = """
            Class Program {
                main(args: Array[String, 1]) {
                    Var a: Int;
                }
                sum(a, b: Int) {
                    Return 10;
                }
            }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 505))

    def test_506(self):
        input = """
            Class Program {
                main() {
                }
            }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 506))