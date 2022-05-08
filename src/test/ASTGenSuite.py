import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    count = 299
    # def test_simple_program(self):
    #     """Simple program: int main() {} """
    #     input = """int main() {}"""
    #     expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([],[]))]))
    #     self.assertTrue(TestAST.test(input,expect,300))

    # def test_more_complex_program(self):
    #     """More complex program"""
    #     input = """int main () {
    #         putIntLn(4);
    #     }"""
    #     expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([],[CallExpr(Id("putIntLn"),[IntLiteral(4)])]))]))
    #     self.assertTrue(TestAST.test(input,expect,301))
    
    # def test_call_without_parameter(self):
    #     """More complex program"""
    #     input = """int main () {
    #         getIntLn();
    #     }"""
    #     expect = str(Program([FuncDecl(Id("main"),[],IntType(),Block([],[CallExpr(Id("getIntLn"),[])]))]))
    #     self.assertTrue(TestAST.test(input,expect,302))
   
    def test_300(self):
        input = """
        Class Program {
            Var a: Int = 10;
            Var a: Float = 20.2;
            main() {}
        }
        """
        expect = str(Program([
            ClassDecl(
                Id('Program'),
                [
                    AttributeDecl(
                        Instance(),
                        VarDecl(
                            Id('a'),
                            IntType(),
                            IntLiteral(10),
                        )
                    ),
                    AttributeDecl(
                        Instance(),
                        VarDecl(
                            Id('a'),
                            FloatType(),
                            FloatLiteral(20.2),
                        )
                    ),
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([]),
                    )
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))

    def test_301(self):
        input = """
        Class Program {
            Val $a: Int = 10;
            $a() {}
            main() {}
        }
        """
        expect = str(Program([
            ClassDecl(
                Id('Program'),
                [
                    AttributeDecl(
                        Static(),
                        ConstDecl(
                            Id('$a'),
                            IntType(),
                            IntLiteral(10),
                        )
                    ),
                    MethodDecl(
                        Static(),
                        Id('$a'),
                        [],
                        Block([]),
                    ),
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([]),
                    )
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))

    def test_302(self):
        input = """
        Class Program {
            main() {}
            method(a: Int) {
                a = 10;
                b = 20.2;
            }
        }
        """
        expect = str(Program([
            ClassDecl(
                Id('Program'),
                [
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([]),
                    ),
                    MethodDecl(
                        Instance(),
                        Id('method'),
                        [
                            VarDecl(Id('a'), IntType()),
                        ],
                        Block([
                            Assign(Id('a'), IntLiteral(10)),
                            Assign(Id('b'), FloatLiteral(20.2)),
                        ]),
                    )
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))

    def test_303(self):
        input = """
        Class Parent {}
        Class Child: Parent {
            method() {
                Self.hello = 10;
            }
        }
        Class Program {
            main() {
            }
        }
        """
        expect = str(Program([
            ClassDecl(Id('Parent'), []),
            ClassDecl(
                Id('Child'),
                [
                    MethodDecl(
                        Instance(),
                        Id('method'),
                        [],
                        Block([
                            Assign(
                                FieldAccess(
                                    SelfLiteral(),
                                    Id('hello'),
                                ),
                                IntLiteral(10),
                            ),
                        ]),
                    )
                ],
                Id('Parent')
            ),
            ClassDecl(
                Id('Program'),
                [
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([]),
                    ),
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))

    def test_304(self):
        input = """
        Class Program {
            main() {}
            method(a: Float; b: Float) {
                a = 10.0;
                a = b + 20.2;
                Parent::$hello();
            }
        }
        """
        expect = str(Program([
            ClassDecl(
                Id('Program'),
                [
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([]),
                    ),
                    MethodDecl(
                        Instance(),
                        Id('method'),
                        [
                            VarDecl(Id('a'), FloatType()),
                            VarDecl(Id('b'), FloatType()),
                        ],
                        Block([
                            Assign(Id('a'), FloatLiteral(10.0)),
                            Assign(Id('a'), BinaryOp('+', Id('b'), FloatLiteral(20.2))),
                            CallStmt(Id('Parent'), Id('$hello'), []),
                        ])
                    ),
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))

    def test_305(self):
        input = """
        Class Program {
            main() {}
            method(a: Float; b: Float) {
                a = 10.0;
                a = b + Parent::$hello;
            }
        }
        """
        expect = str(Program([
            ClassDecl(
                Id('Program'),
                [
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([]),
                    ),
                    MethodDecl(
                        Instance(),
                        Id('method'),
                        [
                            VarDecl(Id('a'), FloatType()),
                            VarDecl(Id('b'), FloatType()),
                        ],
                        Block([
                            Assign(Id('a'), FloatLiteral(10.0)),
                            Assign(Id('a'), BinaryOp('+', Id('b'), FieldAccess(Id('Parent'), Id('$hello')))),
                        ])
                    ),
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))

    def test_306(self):
        input = """
        Class A {
            Val $a: Int = 10;
        }
        Class Program {
            main() {
                A::$a = 20;
            }
        }
        """
        expect = str(Program([
            ClassDecl(
                Id('A'),
                [
                    AttributeDecl(Static(), ConstDecl(Id('$a'), IntType(), IntLiteral(10))),
                ],
            ),
            ClassDecl(
                Id('Program'),
                [
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([
                            Assign(FieldAccess(Id('A'), Id('$a')), IntLiteral(20)),
                        ]),
                    ),
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))

    def test_307(self):
        input = """
        Class Program {
            Val a: Int = 10;
            main() {
                Var b: Int = 20;
                Foreach (i In a .. 100.0 By b) {}
            }
        }
        """
        expect = str(Program([
            ClassDecl(
                Id('Program'),
                [
                    AttributeDecl(Instance(), ConstDecl(Id('a'), IntType(), IntLiteral(10))),
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([
                            VarDecl(Id('b'), IntType(), IntLiteral(20)),
                            For(
                                Id('i'),
                                Id('a'),
                                FloatLiteral(100.0),
                                Block([]),
                                Id('b')
                            ),
                        ]),
                    ),
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))

    def test_308(self):
        input = """
        Class Program {
            getFloat(n: Int) {
                Return n + 0.0;
            }
            print(a: Int) {
            }
            main() {
                Var a: Float = 20.0;
                Self.print(a + Self.getFloat(10));
            }
        }
        """
        expect = str(Program([
            ClassDecl(
                Id('Program'),
                [
                    MethodDecl(
                        Instance(),
                        Id('getFloat'),
                        [VarDecl(Id('n'), IntType())],
                        Block([
                            Return(BinaryOp('+', Id('n'), FloatLiteral(0.0)))
                        ])
                    ),
                    MethodDecl(
                        Instance(),
                        Id('print'),
                        [VarDecl(Id('a'), IntType())],
                        Block([])
                    ),
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([
                            VarDecl(Id('a'), FloatType(), FloatLiteral(20.0)),
                            CallStmt(
                                SelfLiteral(),
                                Id('print'),
                                [BinaryOp(
                                    '+',
                                    Id('a'),
                                    CallExpr(SelfLiteral(), Id('getFloat'), [IntLiteral(10)])
                                    )
                                 ]
                            ),
                        ]),
                    ),
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))

    def test_309(self):
        input = """
        Class C {
            Constructor() {}
        }
        Class A {
            Constructor(s: String; c: C) {}
            getInt() {
                Return 1;
            }
        }
        Class B {
            Constructor() {}
            Val a: A = New A("string", New C());
        }
        Class Program {
            print(a: Float) {}
            main() {
                Var b: B = New B();
                Self.print(b.a.getInt());
            }
        }
        """
        expect = str(Program([
            ClassDecl(
                Id('C'),
                [
                    MethodDecl(Instance(), Id('Constructor'), [], Block([])),
                ]
            ),
            ClassDecl(
                Id('A'),
                [
                    MethodDecl(Instance(), Id('Constructor'), [
                        VarDecl(Id('s'), StringType()),
                        VarDecl(Id('c'), ClassType(Id('C')), NullLiteral()),
                    ], Block([])),
                ]
            ),
            ClassDecl(
                Id('B'),
                [
                    MethodDecl(Instance(), Id('Constructor'), [], Block([])),
                    AttributeDecl(
                        Instance(),
                        ConstDecl(
                            Id('a'),
                            ClassType(Id('A')),
                            NewExpr(Id('A'), [
                                StringLiteral('string'),
                                NewExpr(Id('C'), []),
                            ])
                        )
                    ),
                ]
            ),
            ClassDecl(
                Id('Program'),
                [
                    MethodDecl(
                        Instance(),
                        Id('print'),
                        [VarDecl(Id('a'), FloatType())],
                        Block([])
                    ),
                    MethodDecl(
                        Instance(),
                        Id('main'),
                        [],
                        Block([
                            VarDecl(
                                Id('b'),
                                ClassType(Id('B')),
                                NewExpr(
                                    Id('B'),
                                    []
                                )
                            ),
                            CallStmt(
                                SelfLiteral(),
                                Id('print'),
                                [BinaryOp(
                                    '+',
                                    Id('a'),
                                    CallExpr(SelfLiteral(), Id('getFloat'), [IntLiteral(10)])
                                    )
                                 ]
                            ),
                        ]),
                    ),
                ],
            )
        ]))
        ASTGenSuite.count += 1
        self.assertTrue(TestAST.test(input,expect,ASTGenSuite.count))