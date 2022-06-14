# from typing_extensions import Self
# import unittest
# from TestUtils import TestChecker
# from AST import *
# from main.d96.checker.StaticError import *


# class CheckerSuite(unittest.TestCase):
#     count = 399
    
#     def test_400(self):
#         input = """
#         Class Program {
#             main() {
#                 Val a: Int = 10;
#                 Val a: Int = 20;
#             }
#         }
#         """
#         expect = str(Redeclared(Constant(), 'a'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_401(self):
#         input = """
#         Class Program {
#             main() {
#                 Var a: Int = 10;
#                 Var a: Int = 20;
#             }
#         }
#         """
#         expect = str(Redeclared(Variable(), 'a'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_402(self):
#         input = """
#         Class Program {
#             main() {
#                 Var a: Int = 10;
#                 Val a: Int = 20;
#             }
#         }
#         """
#         expect = str(Redeclared(Constant(), 'a'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_403(self):
#         input = """
#         Class Program {
#             main() {}
#         }
#         Class Program {
#             main() {
#                 Var a: Int = 10;
#             }
#         }
#         """
#         expect = str(Redeclared(Class(), 'Program'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_404(self):
#         input = """
#         Class Program {
#             main() {
#                 Var a: Int = 10;
#             }
#             main() {}
#         }
#         """
#         expect = str(Redeclared(Method(), 'main'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_405(self):
#         input = """
#         Class Program {
#             Var a: Int = 10;
#             Var a: Float = 20.2;
#             main() {}
#         }
#         """
#         expect = str(Redeclared(Attribute(), 'a'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_406(self):
#         input = """
#         Class Program {
#             Val $a: Int = 10;
#             Var $a: Float = 20.2;
#             main() {}
#         }
#         """
#         expect = str(Redeclared(Attribute(), '$a'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_407(self):
#         input = """
#         Class Program {
#             Val a: Int = 10;
#             Var b: Int = a + 10;
#             main() {
#             }
#         }
#         """
#         expect = str(Undeclared(Identifier(), 'a'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_408(self):
#         input = """
#         Class Program {
#             $a(a: Int; a: Float) {}
#             main() {}
#         }
#         """
#         expect = str(Redeclared(Parameter(), 'a'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_409(self):
#         input = """
#         Class Program {
#             $a(a, a: Int; b: Float) {}
#             main() {}
#         }
#         """
#         expect = str(Redeclared(Parameter(), 'a'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_410(self):
#         input = """
#         Class Child: Parent {}
#         Class Program {
#             main() {
#             }
#         }
#         """
#         expect = str(Undeclared(Class(), 'Parent'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_411(self):
#         input = """
#         Class Parent {}
#         Class Child: Parent {
#             method() {
#                 Self.hello = 10;
#             }
#         }
#         Class Program {
#             main() {
#             }
#         }
#         """
#         expect = str(Undeclared(Attribute(), 'hello'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_412(self):
#         input = """
#         Class Parent {
#             Val hello: Int = 20;
#         }
#         Class Child: Parent {
#             method() {
#                 Self.hello = Self.world;
#             }
#         }
#         Class Program {
#             main() {
#             }
#         }
#         """
#         expect = str(Undeclared(Attribute(), 'world'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_413(self):
#         input = """
#         Class Program {
#             main() {
#                 a = b;
#             }
#         }
#         """
#         expect = str(Undeclared(Identifier(), 'b'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_414(self):
#         input = """
#         Class Program {
#             main() {
#                 a = 10;
#             }
#         }
#         """
#         expect = str(Undeclared(Identifier(), 'a'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_415(self):
#         input = """
#         Class Program {
#             main() {}
#             method(a: Int) {
#                 a = 10;
#                 b = 20.2;
#             }
#         }
#         """
#         expect = str(Undeclared(Identifier(), 'b'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_416(self):
#         input = """
#         Class Program {
#             main() {}
#             method(a: Float; b: Float) {
#                 a = 10.0;
#                 a = b + 20.2;
#                 Parent::$hello();
#             }
#         }
#         """
#         expect = str(Undeclared(Class(), 'Parent'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_417(self):
#         input = """
#         Class Parent {}
#         Class Program {
#             main() {}
#             method(a: Float; b: Float) {
#                 a = 10.0;
#                 a = b + 20.2;
#                 Parent::$hello();
#             }
#         }
#         """
#         expect = str(Undeclared(Method(), '$hello'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_418(self):
#         input = """
#         Class Program {
#             Var a, b: Float;
#             $a() {}
#             main() {}
#             method() {
#                 Self.a = 10.0;
#                 Self.a = b + Program::$a();
#             }
#         }
#         """
#         expect = str(Undeclared(Identifier(), 'b'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_419(self):
#         input = """
#         Class Parent {
#         }
#         Class Program {
#             main() {}
#             method(a: Float; b: Float) {
#                 a = 10.0;
#                 a = b + Parent::$method;
#             }
#         }
#         """
#         expect = str(Undeclared(Attribute(), '$method'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))


#     def test_420(self):
#         input = """
#         Class Program {
#             Var a, $b: Int = 20, 30;
#             main() {
#                 Self.a = Program::$b + Self.c;
#             }
#         }
#         """
#         expect = str(Undeclared(Attribute(), 'c'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_421(self):
#         input = """
#         Class Program {
#             main() {
#                 Val a: Int = 10;
#                 a = 20;
#             }
#         }
#         """
#         expect = str(CannotAssignToConstant(Assign(Id('a'), IntLiteral(20))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_422(self):
#         input = """
#         Class Program {
#             Val a: Int = 10;
#             main() {
#                 Self.a = 20;
#             }
#         }
#         """
#         expect = str(CannotAssignToConstant(Assign(FieldAccess(SelfLiteral(), Id('a')), IntLiteral(20))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_423(self):
#         input = """
#         Class A {
#             Val $a: Int = 10;
#         }
#         Class Program {
#             main() {
#                 A::$a = 20;
#             }
#         }
#         """
#         expect = str(CannotAssignToConstant(Assign(FieldAccess(Id('A'), Id('$a')), IntLiteral(20))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_424(self):
#         input = """
#         Class Program {
#             Val a: Int = 10;
#             main() {
#                 Self.a = 20.2;
#             }
#         }
#         """
#         expect = str(CannotAssignToConstant(
#             Assign(
#                 FieldAccess(SelfLiteral(), Id('a')),
#                 FloatLiteral(20.2)
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_425(self):
#         input = """
#         Class Program {
#             Val arr: Array[Int, 5] = Array(1, 2, 3, 4, 5);
#             main() {
#                 Self.arr[3] = 12.2421532;
#             }
#         }
#         """
#         expect = str(CannotAssignToConstant(
#             Assign(
#                 ArrayCell(
#                     FieldAccess(SelfLiteral(), Id('arr')),
#                     [IntLiteral(3)]), FloatLiteral(12.2421532))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_426(self):
#         input = """
#         Class Program {
#             Val a: Int = 10;
#             main() {
#                 Var b: Int = 20;
#                 If (Self.a > b) {
#                 } Elseif (Self.a + b) {}
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             If(
#                 BinaryOp(
#                     '+',
#                     FieldAccess(SelfLiteral(), Id('a')),
#                     Id('b')
#                 ),
#                 Block([]))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_427(self):
#         input = """
#         Class Program {
#             Val a: Int = 10;
#             main() {
#                 Var b: Int = 20;
#                 Var i: Int;
#                 Foreach (i In Self.a .. 100.0 By b) {}
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             For(
#                 Id('i'),
#                 FieldAccess(SelfLiteral(), Id('a')),
#                 FloatLiteral(100.0),
#                 Block([]),
#                 Id('b')
#             )))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_428(self):
#         input = """
#         Class Program {
#             Val a: Int = 10;
#             main() {
#                 Var b: Int = 20;
#                 Foreach (i In b .. 100 By Self.a + 1.0) {}
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             For(
#                 Id('i'),
#                 Id('b'),
#                 IntLiteral(100),
#                 Block([]),
#                 BinaryOp('+', FieldAccess(SelfLiteral(), Id('a')), FloatLiteral(1.0))
#             )))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_429(self):
#         input = """
#         Class Program {
#             Val a: Int = 10;
#             main() {
#                 Var b: Int = 20;
#                 b = Self.a;
#                 b = Self.a + 1.0;
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             Assign(Id('b'),
#                    BinaryOp('+',
#                             FieldAccess(SelfLiteral(), Id('a')),
#                             FloatLiteral(1.0)))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_430(self):
#         input = """
#         Class AnotherClass {
#             Var $arr: Array[String, 1];
#         }
#         Class Program {
#             main() {
#                 Var arr: Array[String, 2];
#                 arr = AnotherClass::$arr;
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             Assign(
#                 Id('arr'),
#                 FieldAccess(Id('AnotherClass'), Id('$arr'))
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_431(self):
#         input = """
#         Class AnotherClass {
#             Var $arr: Array[Int, 2];
#         }
#         Class Program {
#             main() {
#                 Var arr: Array[String, 2];
#                 arr = AnotherClass::$arr;
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             Assign(
#                 Id('arr'),
#                 FieldAccess(Id('AnotherClass'), Id('$arr'))
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_432(self):
#         input = """
#         Class AnotherClass {
#             Var $arr: Array[Array[Array[Int, 3], 2], 2];
#         }
#         Class Program {
#             main() {
#                 Var arr: Array[Array[Int, 3], 2];
#                 arr = AnotherClass::$arr[1];
#                 arr[1][1] = AnotherClass::$arr[1][1][1] + 1.0;
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             Assign(
#                 ArrayCell(Id('arr'), [IntLiteral(1), IntLiteral(1)]),
#                 BinaryOp('+', ArrayCell(FieldAccess(Id('AnotherClass'), Id('$arr')), [IntLiteral(1), IntLiteral(1), IntLiteral(1)]), FloatLiteral(1.0)),
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_433(self):
#         input = """
#         Class Program {
#             getFloat(n: Int) {
#                 Return n + 0.0;
#             }
#             print(a: Int) {
#             }
#             main() {
#                 Var a: Float = 20.0;
#                 Self.print(a + Self.getFloat(10));
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             CallStmt(
#                 SelfLiteral(),
#                 Id('print'),
#                 [BinaryOp(
#                     '+',
#                     Id('a'),
#                     CallExpr(SelfLiteral(), Id('getFloat'), [IntLiteral(10)])
#                     )
#                  ]
#             ),
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_434(self):
#         input = """
#         Class Program {
#             getFloat(n: Int) {
#                 Return n + 0.0;
#             }
#             print(a: Int) {
#                 Return 1;
#             }
#             main() {
#                 Var a: Int = 20;
#                 Self.print(a);
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             CallStmt(
#                 SelfLiteral(),
#                 Id('print'),
#                 [
#                     Id('a'),
#                 ]
#             ),
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_435(self):
#         input = """
#         Class Program {
#             getFloat(n: Int) {
#                 Return n + 0.0;
#             }
#             print(a, b: Int) {
#                 Return ;
#             }
#             main() {
#                 Var a: Float = 20.0;
#                 Self.print(a);
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             CallStmt(
#                 SelfLiteral(),
#                 Id('print'),
#                 [
#                     Id('a'),
#                 ]
#             ),
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_436(self):
#         input = """
#         Class Program {
#             getFloat(n: Int) {
#                 Return n + 0.0;
#             }
#             print(a: Int) {
#                 Return ;
#             }
#             main() {
#                 Var a: Int = 20;
#                 Self.print(a, 10);
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             CallStmt(
#                 SelfLiteral(),
#                 Id('print'),
#                 [
#                     Id('a'),
#                     IntLiteral(10),
#                 ]
#             ),
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_437(self):
#         input = """
#         Class Program {
#             getFloat(n: Int) {
#                 Return n + 0.0;
#             }
#             print(a: Int) {
#                 Return ;
#                 Return 10;
#             }
#             main() {
#                 Var a: Int = 20;
#                 Self.print(a);
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             Return(IntLiteral(10)),
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_438(self):
#         input = """
#         Class Program {
#             getFloat(n: Int) {
#                 Return n + 0.0;
#             }
#             print(a: Int) {
#                 If (True) {
#                     Return 10.2;
#                 }
#                 Return 10;
#             }
#             main() {
#                 Var a: Int = 20;
#                 Self.print(a);
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             Return(IntLiteral(10)),
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_439(self):
#         input = """
#         Class A {
#             $getInt() {
#                 Return 1;
#             }
#         }
#         Class B : A {
#         }
#         Class C : B {
#         }
#         Class Program {
#             print(a: Int) {
#                 If (True) {
#                     Return;
#                 }
#             }
#             main() {
#                 Var a: Int = 20;
#                 Self.print(C::$getInt());
#                 Self.print(a + 0.0);
#             }
#         }
#         """
#         expect = str(Undeclared(Method(), '$getInt'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_440(self):
#         input = """
#         Class A {
#             $getInt() {
#                 Return 1;
#             }
#         }
#         Class B : A {
#             $getInt() {
#                 Return 2.2;
#             }
#         }
#         Class C : B {
#         }
#         Class Program {
#             print(a: Int) {
#                 If (True) {
#                     Return;
#                 }
#             }
#             main() {
#                 Var a: Int = 20;
#                 Self.print(C::$getInt());
#                 Self.print(a + 0.0);
#             }
#         }
#         """
#         expect = str(Undeclared(Method(), '$getInt'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_441(self):
#         input = """
#         Class Program {
#             Var arr: Array[String, 2] = Array("Hwllo", "wrwer");
#             main() {
#                 Val a: Int = 2;
#                 Var b: Float = 3.3;
#                 If ((10 > 20.2) && (a < b) || ("Hello" ==. "World")) {
#                     Self.arr[1] = (Self.arr[2] +. "wrewr") + 0;
#                 }
#             }
#         }
#         """
#         expect = str(TypeMismatchInExpression(
#             BinaryOp(
#                 '+',
#                 BinaryOp(
#                     '+.',
#                     ArrayCell(FieldAccess(SelfLiteral(), Id('arr')), [IntLiteral(2)]),
#                     StringLiteral("wrewr")
#                 ),
#                 IntLiteral(0)
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_442(self):
#         input = """
#         Class Program {
#             main() {
#                 Var a: Int = 10;
#                 {
#                     Var a: Int = 10;
#                     Var arr: Array[Int, 3] = Array(1, 2, 3);
#                     a = a + arr[1.0];
#                 }
#             }
#         }
#         """
#         expect = str(TypeMismatchInExpression(
#             ArrayCell(
#                 Id('arr'),
#                 [
#                     FloatLiteral(1.0),
#                 ]
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_443(self):
#         input = """
#         Class Out {
#             $printInt(value: Int){}
#             $printFloat(value: Float){}
#             $printBool(value: Boolean){}
#             $printString(value: String){}
#             $printArray(value: Array[Int, 3]){}
#         }
#         Class Program {
#             main() {
#                 Out::$printInt(1.0 % 2);
#             }
#         }
#         """
#         expect = str(TypeMismatchInExpression(
#             BinaryOp(
#                 '%',
#                 FloatLiteral(1.0),
#                 IntLiteral(2)
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_444(self):
#         input = """
#         Class Out {
#             $printInt(value: Int){}
#             $printFloat(value: Float){}
#             $printBool(value: Boolean){}
#             $printString(value: String){}
#             $printArray(value: Array[Int, 3]){}
#         }
#         Class Program {
#             main() {
#                 Out::$printInt(-2 + -3 + -"4.0");
#             }
#         }
#         """
#         expect = str(TypeMismatchInExpression(
#             UnaryOp('-', StringLiteral('4.0')),
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_445(self):
#         input = """
#         Class Out {
#             $printInt(value: Int){}
#             $printFloat(value: Float){}
#             $printBool(value: Boolean){}
#             $printString(value: String){}
#             $printArray(value: Array[Int, 3]){}
#         }
#         Class Program {
#             main() {
#                 Out::$printArray(Array(1, 2, 3.0));
#             }
#         }
#         """
#         expect = str(IllegalArrayLiteral(
#             ArrayLiteral([
#                 IntLiteral(1),
#                 IntLiteral(2),
#                 FloatLiteral(3.0),
#             ])
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_446(self):
#         input = """
#         Class Out {
#             $printInt(value: Int){}
#             $printFloat(value: Float){}
#             $printBool(value: Boolean){}
#             $printString(value: String){}
#             $printArray(value: Array[Int, 3]){}
#         }
#         Class Program {
#             main() {
#                 Out::$printArray(Array(1, 2, 3, 4));
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             CallStmt(
#                 Id('Out'),
#                 Id('$printArray'),
#                 [
#                     ArrayLiteral([
#                         IntLiteral(1),
#                         IntLiteral(2),
#                         IntLiteral(3),
#                         IntLiteral(4),
#                     ])
#                 ]
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_447(self):
#         input = """
#         Class A {
#             Constructor(a, b: Int) {}
#         }
#         Class Program {
#             main() {
#                 Var a: A = New A();
#             }
#         }
#         """
#         expect = str(TypeMismatchInExpression(
#             NewExpr(Id('A'), [])
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_448(self):
#         input = """
#         Class A {
#             Constructor() {}
#             getInt() {
#                 Return 1;
#             }
#         }
#         Class Program {
#             print(a: Boolean) {}
#             main() {
#                 Var a: A = New A();
#                 Self.print(a.getInt());
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             CallStmt(
#                 SelfLiteral(),
#                 Id('print'),
#                 [
#                     CallExpr(Id('a'), Id('getInt'), []),
#                 ]
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_449(self):
#         input = """
#         Class C {
#             Constructor() {}
#         }
#         Class A {
#             Constructor(s: String; c: C) {}
#             getInt() {
#                 Return 1;
#             }
#         }
#         Class B {
#             Constructor() {}
#             Val a: A = New A("string", New C());
#         }
#         Class Program {
#             print(a: String) {}
#             main() {
#                 Var b: B = New B();
#                 Self.print(b.a.getInt());
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             CallStmt(
#                 SelfLiteral(),
#                 Id('print'),
#                 [
#                     CallExpr(FieldAccess(Id('b'), Id('a')), Id('getInt'), []),
#                 ]
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_450(self):
#         input = """
#         Class A {
#             Constructor() {}
#         }
#         Class B {
#             Constructor() {}
#         }
#         Class Program {
#             print(a: Float) {}
#             main() {
#                 Val a: A = New B();
#                 Self.print(a.getInt());
#             }
#         }
#         """
#         expect = str(TypeMismatchInConstant(
#             ConstDecl(
#                 Id('a'),
#                 ClassType(Id('A')),
#                 NewExpr(Id('B'), [])
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_451(self):
#         input = """
#         Class A {
#             Constructor() {}
#         }
#         Class B {
#             Constructor() {}
#         }
#         Class Program {
#             print(a: Float) {}
#             main() {
#                 Var a: A = New B();
#                 Self.print(a.getInt());
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             VarDecl(
#                 Id('a'),
#                 ClassType(Id('A')),
#                 NewExpr(Id('B'), [])
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_452(self):
#         input = """
#         Class A {
#             Constructor() {}
#         }
#         Class B : A{
#             Constructor() {}
#         }
#         Class Program {
#             print(a: Float) {}
#             main() {
#                 Var a: A = New B();
#                 Var b: B = New A();
#                 Self.print(a.getInt());
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             VarDecl(
#                 Id('b'),
#                 ClassType(Id('B')),
#                 NewExpr(Id('A'), [])
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_453(self):
#         input = """
#         Class A {
#             Constructor() {}
#         }
#         Class B : A{
#             Constructor() {}
#         }
#         Class Program {
#             print(a: A) {}
#             main() {
#                 Var a: A = New B();
#                 Self.print(a);
#                 Var b: B = New A();
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             VarDecl(
#                 Id('b'),
#                 ClassType(Id('B')),
#                 NewExpr(Id('A'), [])
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_454(self):
#         input = """
#         Class Program {
#             print(a: Int) {}
#             main() {
#                 Var i: Int;
#                 Foreach (i In 0 .. 10) {
#                     Continue;
#                 }
#                 Break;
#             }
#         }
#         """
#         expect = str(MustInLoop(Break()))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_455(self):
#         input = """
#         Class Program {
#             print(a: Int) {}
#             main() {
#                 Var i: Int;
#                 Foreach (i In 0 .. 10) {
#                     Break;
#                 }
#                 Continue;
#             }
#         }
#         """
#         expect = str(MustInLoop(Continue()))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_456(self):
#         input = """
#         Class Program {
#             print(a: Int) {}
#             main() {
#                 Continue;
#             }
#         }
#         """
#         expect = str(MustInLoop(Continue()))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_457(self):
#         input = """
#         Class A {
#             Val a: Int = 10;
#         }
#         Class Program {
#             print(a: Int) {}
#             main() {
#                 Self.print(A::a);
#             }
#         }
#         """
#         expect = str(IllegalMemberAccess(FieldAccess(Id('A'), Id('a'))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_458(self):
#         input = """
#         Class A {
#             Constructor() {}
#             Val $a: Int = 10;
#         }
#         Class Program {
#             print(a: Int) {}
#             main() {
#                 Val a: A = New A();
#                 Self.print(a.$a);
#             }
#         }
#         """
#         expect = str(IllegalMemberAccess(FieldAccess(Id('a'), Id('$a'))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_459(self):
#         input = """
#         Class A {
#             Val a: Int = 10;
#         }
#         Class Program {
#             print(a: Int) {}
#             main() {
#                 Self.print(A.a);
#             }
#         }
#         """
#         expect = str(IllegalMemberAccess(FieldAccess(Id('A'), Id('a'))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_460(self):
#         input = """
#         Class A {
#             Val a: Int = 10;
#         }
#         Class Program {
#             print(a: Int) {}
#             main() {
#                 Foreach (i In 0 .. 10) {
#                     i = 10.0;
#                 }
#             }
#         }
#         """
#         expect = str(Undeclared(Identifier(), 'i'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_461(self):
#         input = """
#         Class A {
#             Val a: Int = 10;
#         }
#         Class Program {
#             print(a: Int) {}
#             main(a: String) {
#             }
#         }
#         """
#         expect = str(NoEntryPoint())
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_462(self):
#         input = """
#         Class A {
#             Val a: Int = 10;
#         }
#         Class Program {
#             print(a: Int) {}
#             main() {
#                 Var i: Int;
#                 Foreach (i In 0 .. 10) {}
#                 Return "main";
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(Return(StringLiteral("main"))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_463(self):
#         input = """
#         Class A {
#             Val a: Int = 10;
#         }
#         Class Program {
#             print(a: Int) {}
#             method() {}
#         }
#         """
#         expect = str(NoEntryPoint())
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_464(self):
#         input = """
#         Class A {
#             Val a: Int = 10;
#         }
#         Class Program {
#             print(a: Int) {}
#             method() {}
#         }
#         """
#         expect = str(NoEntryPoint())
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_465(self):
#         input = """
#         Class Program {
#             Var a: Int = 10;
#             $print(a: Int) {
#                 Self.a = 20;
#             }
#             main() {
#             }
#         }
#         """
#         expect = str(IllegalMemberAccess(
#             FieldAccess(SelfLiteral(), Id('a'))
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_466(self):
#         input = """
#         Class Program {
#             Var a: A;
#             main() {
#             }
#         }
#         """
#         expect = str(Undeclared(Class(), 'A'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))
    
#     def test_467(self):
#         input = """
#         Class Car {}
#         Class Program {
#             main(){
#                 Val car: Car = New Car();
#                 Var x : Int = 1 + Car;
#             }
#         }
#         """
#         expect = str(Undeclared(Identifier(), 'Car'))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_468(self):
#         input = """
#         Class Program {
#             main(){
#                 Var b: Boolean = True == 2;  
#             }
#         }
#         """
#         expect = str(TypeMismatchInExpression(
#             BinaryOp(
#                 '==',
#                 BooleanLiteral(True),
#                 IntLiteral(2) 
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_469(self):
#         input = """
#         Class Program {
#             main(){
#                 Var a: Int;
#                 Val b: Int = a + 10;
#             }
#         }
#         """
#         expect = str(IllegalConstantExpression(
#             BinaryOp(
#                 '+',
#                 Id('a'),
#                 IntLiteral(10)
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_470(self):
#         input = """
#         Class Program {
#             Var $a: Int;
#             main(){
#                 Var a: Int = Program::$a + 1;
#                 Val b: Int = a + 10;
#             }
#         }
#         """
#         expect = str(IllegalConstantExpression(
#             BinaryOp(
#                 '+',
#                 Id('a'),
#                 IntLiteral(10)
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_471(self):
#         input = """
#         Class A {
#             Var $a: Int;
#         }
#         Class Program {
#             main() {
#                 Val b: Int = A::$a + 10;
#             }
#         }
#         """
#         expect = str(IllegalConstantExpression(
#             BinaryOp(
#                 '+',
#                 FieldAccess(Id('A'), Id('$a')),
#                 IntLiteral(10)
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_472(self):
#         input = """
#         Class A {
#             Var $a: Int;
#         }
#         Class Program {
#             method(d: Int) {
#                 A::$a = 10;
#                 Val b: Int = A::$a + d;
#             }
#         }
#         """
#         expect = str(NoEntryPoint())
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))
    
#     def test_473(self):
#         input = """
#         Class Program {
#             method(d: Int) {
#                 Val c: Float = d;
#                 Var e: Int = c;
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             VarDecl(
#                 Id('e'),
#                 IntType(),
#                 Id('c')
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))
    
#     def test_474(self):
#         input = """
#         Class Program {
#             Var a: Int;
#             a() {
#                 Return 1;
#             }
#             main() {
#                 Val b: Int = Self.a * Self.a();
#             }
#         }
#         """
#         expect = str(
#             IllegalConstantExpression(
#                 BinaryOp(
#                     '*',
#                     FieldAccess(SelfLiteral(), Id('a')),
#                     CallExpr(SelfLiteral(), Id('a'), [])
#                 )
#             )
#         )
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_475(self):
#         input = """
#         Class Program {
#             print(a: Float) {}
#             print2(a, b: Int) {}
#             main() {
#                 Self.print(10);
#                 Self.print2(20);
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(
#             CallStmt(
#                 SelfLiteral(),
#                 Id('print2'),
#                 [IntLiteral(20)]
#             )
#         ))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_476(self):
#         input = """
#         Class Program {
#             main() {
#                 Val i: Int = 0;
#                 Foreach (i In 100 % 100 .. 10) {
#                 }
#             }
#         }
#         """
#         expect = str(CannotAssignToConstant(
#             Assign(
#                 Id('i'),
#                 BinaryOp(
#                     '%',
#                     IntLiteral(100),
#                     IntLiteral(100)
#                 )
#        )))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))

#     def test_477(self):
#         input = """
#         Class Program {
#             main() {
#             }
#             Destructor() {
#                 Return "";
#             }
#         }
#         """
#         expect = str(TypeMismatchInStatement(Return(StringLiteral(''))))
#         CheckerSuite.count += 1
#         self.assertTrue(TestChecker.test(input, expect, CheckerSuite.count))
        

import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    # def test_undeclared_function(self):
    #     """Simple program: int main() {} """
    #     input = """int main() {foo();}"""
    #     expect = "Undeclared Function: foo"
    #     self.assertTrue(TestChecker.test(input,expect,400))

    # def test_diff_numofparam_stmt(self):
    #     """More complex program"""
    #     input = """int main () {
    #         putIntLn();
    #     }"""
    #     expect = "Type Mismatch In Statement: CallExpr(Id(putIntLn),List())"
    #     self.assertTrue(TestChecker.test(input,expect,401))
    
    # def test_diff_numofparam_expr(self):
    #     """More complex program"""
    #     input = """int main () {
    #         putIntLn(getInt(4));
    #     }"""
    #     expect = "Type Mismatch In Expression: CallExpr(Id(getInt),List(IntLiteral(4)))"
    #     self.assertTrue(TestChecker.test(input,expect,402))

    # def test_undeclared_function_use_ast(self):
    #     """Simple program: int main() {} """
    #     input = Program([FuncDecl(Id("main"),[],IntType(),Block([],[
    #         CallExpr(Id("foo"),[])]))])
    #     expect = "Undeclared Function: foo"
    #     self.assertTrue(TestChecker.test(input,expect,403))

    # def test_diff_numofparam_expr_use_ast(self):
    #     """More complex program"""
    #     input = Program([
    #             FuncDecl(Id("main"),[],IntType(),Block([],[
    #                 CallExpr(Id("putIntLn"),[
    #                     CallExpr(Id("getInt"),[IntLiteral(4)])
    #                     ])]))])
    #     expect = "Type Mismatch In Expression: CallExpr(Id(getInt),List(IntLiteral(4)))"
    #     self.assertTrue(TestChecker.test(input,expect,404))

    # def test_diff_numofparam_stmt_use_ast(self):
    #     """More complex program"""
    #     input = Program([
    #             FuncDecl(Id("main"),[],IntType(),Block([],[
    #                 CallExpr(Id("putIntLn"),[])]))])
    #     expect = "Type Mismatch In Statement: CallExpr(Id(putIntLn),List())"
    #     self.assertTrue(TestChecker.test(input,expect,405))
    
    def test_45(self):
        input = Program([
            ClassDecl(
                        Id('Shape'),
                        [
                            AttributeDecl(Instance(), VarDecl(
                                Id('x'), FloatType(), FloatLiteral(0.001))),
                            AttributeDecl(Static(), VarDecl(
                                Id('$y'), StringType(), StringLiteral('PPL')))
                        ],
                        ),
            ClassDecl(
                Id('Program'),
                [
                    AttributeDecl(Instance(), VarDecl(Id('x'), IntType())),
                    AttributeDecl(Instance(), VarDecl(
                        Id('y'), StringType(), FieldAccess(Id('x'), Id('$x')))),
                    MethodDecl(Static(), Id('main'), [], Block([]))
                ],
            )
        ])
        expect = 'Undeclared Class: x'
        self.assertTrue(TestChecker.test(input, expect, 445))
        
    
    def test_0(self):
        input = Program(
            [
                ClassDecl(
                    Id("A"),
                    []
                ),
                ClassDecl(
                    Id("A"),
                    []
                ),
                ClassDecl(
                    Id("Program"),
                    [
                        MethodDecl(
                            Static(),
                            Id("main"),
                            [],
                            Block([])
                        )
                    ]
                )
            ]
        )
        expect = "Redeclared Class: A"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_1(self):
        input = Program(
            [
                ClassDecl(
                    Id("Program"),
                    [
                        MethodDecl(
                            Static(),
                            Id("main"),
                            [],
                            Block([])
                        ),
                        AttributeDecl(
                            Instance(),
                            VarDecl(
                                Id("myVar"),
                                StringType(),
                                StringLiteral("Hello World")
                            )
                        ),
                        AttributeDecl(
                            Instance(),
                            VarDecl(
                                Id("myVar"),
                                IntType()
                            )
                        )
                    ]
                )
            ]
        )
        expect = "Redeclared Attribute: myVar"
        self.assertTrue(TestChecker.test(input,expect,401))
