'''
 *   @author Le Hoang Nam
'''
from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod

class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"

    def init(self):
        # return [Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
        #             Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
        #             Symbol("putIntLn", MType([IntType()], VoidType()), CName(self.libName))
                    
        #             ]
        return []

    def gen(self, ast: AST, dir_: str):

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)

class MethodType:
    def __init__(self, param_type_list, return_type):
        self.partype = param_type_list
        self.rettype = return_type

class Symbol:
    def __init__(self, name, d96_type, label, idx):
        self.name = name
        self.d96_type = d96_type
        self.label = label
        self.idx = idx
        
class SubBody():
    def __init__(self, frame, sym):
        #frame: Frame
        #sym: List[Symbol]

        self.frame = frame
        self.sym = sym

class Access():
    def __init__(self, frame: Frame, is_lhs: bool):
        self.frame = frame
        self.is_lhs = is_lhs

class Val(ABC):
    pass

class Index(Val):
    def __init__(self, value):
        #value: Int

        self.value = value

class CName(Val):
    def __init__(self, value):
        #value: String

        self.value = value

class CodeGenVisitor(BaseVisitor, Utils):
    def __init__(self, astTree: AST, env, dir_: str):
        self.astTree = astTree
        self.env = env
        self.class_name = ""
        self.path = dir_
        self.emit = None
        self.cur_symbols = {}
        self.constructor_decl: MethodDecl = MethodDecl(Instance(), Id('<init>'), [], Block([]))
        self.static_field_decl: MethodDecl = MethodDecl(Instance(), Id('<clinit>'), [], Block([]))
        self.ret_table = { 'method' : {}, 'attr': {} }

    def gen_static(self, ast: MethodDecl):
        is_static = True
        frame = Frame(MethodType([], VoidType()), VoidType())
        self.emit.printout(self.emit.emitMETHOD(
            '<clinit>',
            VoidType(),
            is_static,
            frame
        ))
        for stmt in ast.body.inst:
            if type(stmt) is not Block:
                self.visit(stmt, frame)
        
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        
        self.emit.printout(self.emit.emitENDMETHOD(frame))

    def visitProgram(self, ast: Program, _):
        for decl in ast.decl:
            self.visit(decl, None)

    def visitClassDecl(self, ast: ClassDecl, _):
        self.class_name = ast.classname.name
        self.emit = Emitter(f'{self.path}/{self.class_name}.j')

        self.emit.printout(self.emit.emitPROLOG(self.class_name, "java.lang.Object"))

        if not self.ret_table['method'].get(self.class_name):
            self.ret_table['method'][self.class_name] = { '<init>': VoidType(), '<clinit>': VoidType() }

        attr_list = [mem for mem in ast.memlist if type(mem) is AttributeDecl]

        for mem in attr_list:
            self.visit(mem, None)

        method_list = [mem for mem in ast.memlist if type(mem) is MethodDecl]

        has_constructor_decl = False
        for method_decl in method_list:
            if method_decl.name.name == 'Constructor':
                has_constructor_decl = True
            has_return = False
            name = method_decl.name.name
            for stmt in method_decl.body.inst:
                if type(stmt) is Return:
                    d96_type = self.visit(stmt.expr, None)
                    self.ret_table['method'][self.class_name][name] = d96_type
                    has_return = True
                    break
            if not has_return:
                self.ret_table['method'][self.class_name][name] = VoidType()
                has_return = True

        if not has_constructor_decl:
            self.visit(self.constructor_decl, None)

        for method_decl in method_list:
            self.visit(method_decl, None)

        if self.static_field_decl.body.inst:
            self.gen_static(self.static_field_decl)
            # self.visit(self.static_field_decl, None)

        self.emit.emitEPILOG()

    def visitMethodDecl(self, ast: MethodDecl, _):
        name = ast.name.name
        
        # jvm doesnt have destructor
        if name == 'Destructor':
            return
        
        if name == 'Constructor':
            self.constructor_decl.param = ast.param
            self.constructor_decl.body.inst += ast.body.inst
            self.visit(self.constructor_decl, None)
            return

        is_static = type(ast.kind) is Static or name in ('main', '<clinit>')
        frame = Frame(name, self.ret_table['method'][self.class_name][name])
        self.cur_symbols = {}
        frame.enterScope(False)


        # First loop
        param_type_list = [self.visit(param, None) for param in ast.param]
        method_decl_code = self.emit.emitMETHOD(
            name,
            MethodType(param_type_list, self.ret_table['method'][self.class_name][name]),
            is_static,
            None
        )
        self.emit.printout(method_decl_code)
        
        
        start_label = frame.getStartLabel()
        end_label = frame.getEndLabel()
        if not is_static:
            new_idx = frame.getNewIndex()
            var_this = self.emit.emitVAR(
                new_idx,
                'this',
                ClassType(Id(self.class_name)),
                start_label,
                end_label,
                None
            )
            self.emit.printout(var_this)
        
        for param in ast.param:
            new_idx = frame.getNewIndex()
            var_param = self.emit.emitVAR(
                new_idx,        
                param.variable.name,
                param.varType,
                start_label,
                end_label,
                None
            )
            self.emit.printout(var_param)
        
        # First for loop
        for stmt in ast.body.inst:
            if type(stmt) is VarDecl:
                new_idx = frame.getNewIndex()
                new_label = frame.getNewLabel()
                name = stmt.variable.name
                var_vardecl = self.emit.emitVAR(
                    new_idx,
                    name,
                    stmt.varType,
                    new_label,
                    end_label,
                    None
                )
                self.cur_symbols[name] = Symbol(name, stmt.varType, new_label, new_idx)
                self.emit.printout(var_vardecl)
            elif type(stmt) is ConstDecl:
                new_idx = frame.getNewIndex()
                new_label = frame.getNewLabel()
                name = stmt.constant.name
                var_vardecl = self.emit.emitVAR(
                    new_idx,
                    name,
                    stmt.constType,
                    new_label,
                    end_label,
                    None
                )
                self.cur_symbols[name] = Symbol(name, stmt.constType, new_label, new_idx)
                self.emit.printout(var_vardecl)
                

        self.emit.printout(self.emit.emitLABEL(start_label, frame))

        if name == '<init>':
            self.emit.printout(self.emit.emitREADVAR('this', ClassType(Id('this')), 0, frame))
            self.emit.emitDUP(frame)
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        
        # Second for loop
        for stmt in ast.body.inst:
            if type(stmt) is not Block:
                self.visit(stmt, frame)
        
        self.emit.printout(self.emit.emitLABEL(end_label, frame))

        if not ast.body.inst or ast.body.inst and type(ast.body.inst[-1]) is not Return:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))

        self.emit.printout(self.emit.emitENDMETHOD(frame))

        frame.exitScope()
    
    def visitAttributeDecl(self, ast: AttributeDecl, _):
        if not self.ret_table['attr'].get(self.class_name):
            self.ret_table['attr'][self.class_name] = {}
        if type(ast.kind) is Static:
            if type(ast.decl) is VarDecl:
                name = ast.decl.variable.name
                d96_type = ast.decl.varType
                if ast.decl.varInit:
                    self.static_field_decl.body.inst.append(Assign(ast.decl.variable, ast.decl.varInit))
            else:
                name = ast.decl.constant.name
                d96_type = ast.decl.constType
                self.static_field_decl.body.inst.append(Assign(ast.decl.constant, ast.decl.value))

            self.ret_table['attr'][self.class_name][name] = d96_type
            code = self.emit.emitSTATICFIELD(name, d96_type)
        else:
            if type(ast.decl) is VarDecl:
                name = ast.decl.variable.name
                d96_type = ast.decl.varType
                if ast.decl.varInit:
                    self.constructor_decl.body.inst.append(Assign(ast.decl.variable, ast.decl.varInit))
            else:
                name = ast.decl.constant.name
                d96_type = ast.decl.constType
                self.constructor_decl.body.inst.append(Assign(ast.decl.constant, ast.decl.value))

            self.ret_table['attr'][self.class_name][name] = d96_type
            code = self.emit.emitINSTANCEFIELD(name, d96_type)
        self.emit.printout(code)
    
    def visitVarDecl(self, ast: VarDecl, frame: Frame):
        name = ast.variable.name
        if frame:
            symbol = self.cur_symbols[name]
            self.emit.printout(self.emit.emitLABEL(symbol.label, frame))
            if ast.varInit:
                self.visit(Assign(ast.variable, ast.varInit), frame)
        
        return ast.varType
    
    def visitAssign(self, ast: Assign, frame: Frame):
        expr_code, expr_type = self.visit(ast.exp, Access(frame, False))
        lhs_code, lhs_type = self.visit(ast.lhs, Access(frame, True))
        self.emit.printout(self.emit.emitREADVAR('this', ClassType(Id('this')), 0, frame))
        self.emit.printout(expr_code)
        self.emit.printout(lhs_code)
        
    def visitFor(self, ast: For, frame: Frame):
        printout = self.emit.printout
        continue_label = frame.getContinueLabel()
        break_label = frame.getBreakLabel()
        frame.enterLoop()
        e1c, e1t = self.visit(ast.expr1, Access(frame, False))
        e2c, e2t = self.visit(ast.expr2, Access(frame, False))
        if ast.expr3:
            e3c, e3t = self.visit(ast.expr3, Access(frame, False))
        walker_assign, _ = self.visit(ast.id, Access(frame, True))

        printout(e1c)
        printout(walker_assign)

        walker, _ = self.visit(ast.id, Access(frame, False))

        printout(self.emit.emitLABEL(continue_label))
        # Loop condition
        printout(walker)
        printout(e2c)
        printout(self.emit.emitIFFALSE(break_label, frame))
        
        # Loop body
        self.visit(ast.loop, frame)

        printout(walker)
        if not ast.expr3:
            printout(self.emit.emitPUSHICONST(1, frame))
        else:
            printout(e3c)
        printout(self.emit.emitADDOP('+', IntType(), frame))
        printout(walker_assign)
        printout(self.emit.emitGOTO(continue_label))
        printout(self.emit.emitLABEL(break_label))
        frame.exitLoop()
        
    def visitBlock(self, ast: Block, frame: Frame):
        for stmt in ast.inst:
            if type(stmt) is Block:
                frame.enterScope()
                self.visit(stmt, frame)
                frame.exitScope()
            else:
                self.visit(stmt, frame)
        
    def visitIf(self, ast: If, frame: Frame):
        printout = self.emit.printout
        labels = [
            frame.getNewLabel(),
            frame.getNewLabel(),
            frame.getNewLabel(),
        ]
        ec, et = self.visit(ast.expr, Access(frame, False))
        printout(self.emit.emitLABEL(labels[0], frame))
        printout(ec)
        printout(self.emit.emitIFFALSE(labels[1], frame))
        frame.enterScope()
        self.visit(ast.thenStmt, frame)
        frame.exitScope()
        printout(self.emit.emitGOTO(labels[2], frame))
        printout(self.emit.emitLABEL(labels[1], frame))
        if ast.elseStmt:
            self.visit(ast.elseStmt, frame)
        printout(self.emit.emitLABEL(labels[2], frame))
        
    def visitCallStmt(self, ast: CallStmt, access: Access):
        ...
        
    def visitCallExpr(self, ast: CallExpr, access: Access):
        ...
        
    def visitFieldAccess(self, ast: FieldAccess, access: Access):
        ...
        
    def visitBinaryOp(self, ast: BinaryOp, access: Access):
        ecl, etl = self.visit(ast.left, access)
        ecr, etr = self.visit(ast.right, access)
        frame = access.frame
        if ast.op in ('+', '-', '*', '/'):
            emit = self.emit.emitADDOP if ast.op in ('+', '-') else self.emit.emitMULOP
            i2f = self.emit.emitI2F(frame)
            op = emit(ast.op, FloatType(), frame)
            if type(etl) is FloatType and type(etr) is IntType:
                return ecl + ecr + i2f + op, FloatType()
            elif type(etl) is IntType and type(etr) is FloatType:
                return ecl + i2f + ecr + op, FloatType()
            elif type(etl) is FloatType:
                return ecl + ecr + op, FloatType()
            op = emit(ast.op, IntType(), frame)
            return ecl + ecr + op, IntType()
        elif ast.op == '%':
            op = self.emit.emitMOD(frame)
            return ecl + ecr + op, IntType()
        elif ast.op in ('==', '!=', '>', '<', '>=', '<='):
            return ecl + ecr + self.emit.emitREOP(ast.op, BoolType(), frame), BoolType()
        elif ast.op == '+.':
            concat_method = "java/lang/String/concat"
            in_ = MethodType(
                [
                    StringType(),
                ],
                StringType()
            )
            return ecl + ecr + self.emit.emitINVOKEVIRTUAL(concat_method, in_, frame), StringType()
        elif ast.op == '==.':
            equals_method = "java/lang/String/equals"
            in_ = MethodType(
                [
                    StringType(),
                ],
                StringType()
            )
            return ecl + ecr + self.emit.emitINVOKEVIRTUAL(equals_method, in_, frame), BoolType()

        labels = (frame.getNewLabel(), frame.getNewLabel(), frame.getNewLabel())
        if ast.op == '||':
            res = [
                ecl,
                self.emit.emitIFTRUE(labels[0], frame),
                ecr,
                self.emit.emitIFFALSE(labels[1], frame),
                self.emit.emitLABEL(labels[0], frame),
                self.emit.emitPUSHICONST("true", frame),
                self.emit.emitGOTO(labels[2], frame),
                self.emit.emitLABEL(labels[1], frame),
                self.emit.emitPUSHICONST("false", frame),
                self.emit.emitLABEL(labels[2], frame),
            ]
        else:
            res = [
                ecl,
                self.emit.emitIFFALSE(labels[0], frame),
                ecr,
                self.emit.emitIFTRUE(labels[1], frame),
                self.emit.emitLABEL(labels[0], frame),
                self.emit.emitPUSHICONST("false", frame),
                self.emit.emitGOTO(labels[2], frame),
                self.emit.emitLABEL(labels[1], frame),
                self.emit.emitPUSHICONST("true", frame),
                self.emit.emitLABEL(labels[2], frame),
            ]
        return ''.join(res), BoolType()

        
    def visitUnaryOp(self, ast: UnaryOp, access: Access):
        ...
        
    def visitReturn(self, ast: Return, frame: Frame):
        expr_code, expr_type = self.visit(ast.expr, Access(frame, False))
        self.emit.printout(expr_code)
        self.emit.printout(self.emit.emitRETURN(expr_type, frame))
    
    def visitIntLiteral(self, ast: IntLiteral, access: Access):
        if not access:
            return IntType()
        return self.emit.emitPUSHICONST(ast.value, access.frame), IntType()

    def visitBooleanLiteral(self, ast: BooleanLiteral, access: Access):
        if not access:
            return IntType()
        value = "true" if ast.value else "false"
        return self.emit.emitPUSHICONST(value, access.frame), IntType()
    
    def visitFloatLiteral(self, ast: FloatLiteral, access: Access):
        if not access:
            return FloatType()
        return self.emit.emitPUSHFCONST(ast.value, access.frame), FloatType()
    
    def visitStringLiteral(self, ast: StringLiteral, access: Access):
        if not access:
            return StringType()
        return self.emit.emitPUSHCONST(ast.value, StringType(), access.frame), StringType()

    def visitArrayCell(self, ast: ArrayCell, access: Access):
        ast.arr
        ast.idx

    def visitId(self, ast: Id, access: Access):
        name = ast.name
        if access.is_lhs:
            if self.cur_symbols.get(name):
                d96_type = self.cur_symbols[name].d96_type
                idx = self.cur_symbols[name].idx
                code = self.emit.emitWRITEVAR(name, d96_type, idx, access.frame)
            else:
                d96_type = self.ret_table['attr'][self.class_name][name]
                is_static = '$' in name
                if is_static:
                    code = self.emit.emitPUTSTATIC(f'{self.class_name}/{name}', d96_type, access.frame)
                else:
                    code = self.emit.emitPUTFIELD(f'{self.class_name}/{name}', d96_type, access.frame)
        else:
            if self.cur_symbols.get(name):
                d96_type = self.cur_symbols[name].d96_type
                idx = self.cur_symbols[name].idx
                code = self.emit.emitREADVAR(name, d96_type, idx, access.frame)
            else:
                d96_type = self.ret_table['attr'][self.class_name][name]
                is_static = '$' in name
                if is_static:
                    code = self.emit.emitGETSTATIC(f'{self.class_name}/{name}', d96_type, access.frame)
                else:
                    code = self.emit.emitGETFIELD(f'{self.class_name}/{name}', d96_type)
        
        return code, d96_type
