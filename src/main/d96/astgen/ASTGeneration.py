from D96Visitor import D96Visitor
from D96Parser import D96Parser
from AST import *

def flatten(l: list):
    new_list = []
    for elem in l:
        if type(elem) is list:
            new_list += elem
        else:
            new_list += [elem]
    return new_list

def is_class_type(data_type):
    return type(data_type) not in [IntType, FloatType, BoolType, StringType, ArrayType]

class ASTGeneration(D96Visitor):

    # Visit a parse tree produced by D96Parser#program.
    def visitProgram(self, ctx:D96Parser.ProgramContext):
        return Program([self.visit(class_decl) for class_decl in ctx.children[:-1]])


    # Visit a parse tree produced by D96Parser#assign_stmt.
    def visitAssign_stmt(self, ctx:D96Parser.Assign_stmtContext):
        lhs = self.visit(ctx.assign_lhs())
        expr = self.visit(ctx.expr())
        return Assign(lhs, expr)


    # Visit a parse tree produced by D96Parser#assign_lhs.
    def visitAssign_lhs(self, ctx:D96Parser.Assign_lhsContext):
        child = ctx.getChild(0)
        if ctx.Identifier() or ctx.DolarIdentifier():
            return Id(child.getText())

        return self.visit(child)

    # Visit a parse tree produced by D96Parser#if_stmt.
    def visitIf_stmt(self, ctx:D96Parser.If_stmtContext):
        expr, block_stmt = self.visit(ctx.if_clause())
        else_stmt = self.visit(ctx.else_stmt())
        return If(expr, block_stmt, else_stmt)


    # Visit a parse tree produced by D96Parser#else_stmt.
    def visitElse_stmt(self, ctx:D96Parser.Else_stmtContext):
        child_count = ctx.getChildCount()

        if child_count == 0:
            return None
        if child_count == 1:
            return self.visit(ctx.getChild(0))
        
        expr, block_stmt = self.visit(ctx.elseif_clause())
        else_stmt = self.visit(ctx.else_stmt())
        return If(expr, block_stmt, else_stmt)


    # Visit a parse tree produced by D96Parser#if_clause.
    def visitIf_clause(self, ctx:D96Parser.If_clauseContext):
        expr = self.visit(ctx.expr())
        block_stmt = self.visit(ctx.block_stmt())
        return expr, block_stmt


    # Visit a parse tree produced by D96Parser#elseif_clause.
    def visitElseif_clause(self, ctx:D96Parser.Elseif_clauseContext):
        expr = self.visit(ctx.expr())
        block_stmt = self.visit(ctx.block_stmt())
        return expr, block_stmt


    # Visit a parse tree produced by D96Parser#else_clause.
    def visitElse_clause(self, ctx:D96Parser.Else_clauseContext):
        return self.visit(ctx.block_stmt())


    # Visit a parse tree produced by D96Parser#for_stmt.
    def visitFor_stmt(self, ctx:D96Parser.For_stmtContext):
        expr1 = self.visit(ctx.getChild(4))
        expr2 = self.visit(ctx.getChild(6))
        expr3 = self.visit(ctx.step_decl())
        identifier = Id(ctx.Identifier().getText())
        stmt = self.visit(ctx.block_stmt())
        return For(identifier, expr1, expr2, stmt, expr3)


    # Visit a parse tree produced by D96Parser#step_decl.
    def visitStep_decl(self, ctx:D96Parser.Step_declContext):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.expr())


    # Visit a parse tree produced by D96Parser#break_stmt.
    def visitBreak_stmt(self, ctx:D96Parser.Break_stmtContext):
        return Break()


    # Visit a parse tree produced by D96Parser#continue_stmt.
    def visitContinue_stmt(self, ctx:D96Parser.Continue_stmtContext):
        return Continue()


    # Visit a parse tree produced by D96Parser#return_stmt.
    def visitReturn_stmt(self, ctx:D96Parser.Return_stmtContext):
        if ctx.getChildCount() == 2:
            return Return()
        return Return(self.visit(ctx.expr()))


    # Visit a parse tree produced by D96Parser#var_decl_stmt.
    def visitVar_decl_stmt(self, ctx:D96Parser.Var_decl_stmtContext):
        ids, exprs, data_type = self.visit(ctx.getChild(1))
        has_init_vals = bool(exprs)
        VarDeclare = ConstDecl if ctx.VAL() else VarDecl

        if has_init_vals:
            return [VarDeclare(identifier, data_type, expr) for identifier, expr in zip(ids, exprs)]

        init_val = None
        if is_class_type(data_type):
            init_val = NullLiteral()

        return [VarDeclare(identifier, data_type, init_val) for identifier in ids]


    # Visit a parse tree produced by D96Parser#identifier_list_with_init_value.
    def visitIdentifier_list_with_init_value(self, ctx:D96Parser.Identifier_list_with_init_valueContext):
        identifier = Id(ctx.getChild(0).getText())
        expr = self.visit(ctx.getChild(4))
        if ctx.Colon():
            return [identifier], [expr], self.visit(ctx.data_type())

        ids_tail, exprs_head, data_type = self.visit(ctx.identifier_list_with_init_value())
        
        return [identifier] + ids_tail, exprs_head + [expr], data_type


    # Visit a parse tree produced by D96Parser#identifier_list_with_type.
    def visitIdentifier_list_with_type(self, ctx:D96Parser.Identifier_list_with_typeContext):
        identifier = Id(ctx.getChild(0).getText())
        if ctx.Colon():
            return [identifier], [], self.visit(ctx.data_type())
        
        ids_tail, exprs, data_type = self.visit(ctx.getChild(2))
        
        return [identifier] + ids_tail, exprs, data_type


    # Visit a parse tree produced by D96Parser#class_decl_stmt.
    def visitClass_decl_stmt(self, ctx:D96Parser.Class_decl_stmtContext):
        identifier = Id(ctx.Identifier().getText())
        parent = self.visit(ctx.super_class_decl())
        mem_list = self.visit(ctx.class_member_decl())
        return ClassDecl(identifier, mem_list, parent)


    # Visit a parse tree produced by D96Parser#super_class_decl.
    def visitSuper_class_decl(self, ctx:D96Parser.Super_class_declContext):
        if ctx.getChildCount() == 0:
            return None   
        return Id(ctx.Identifier().getText())


    # Visit a parse tree produced by D96Parser#class_member_decl.
    def visitClass_member_decl(self, ctx:D96Parser.Class_member_declContext):
        if ctx.getChildCount() == 0:
            return []
        return flatten([self.visit(ctx.getChild(0))] + self.visit(ctx.class_member_decl()))


    # Visit a parse tree produced by D96Parser#attr_decl_stmt.
    def visitAttr_decl_stmt(self, ctx:D96Parser.Attr_decl_stmtContext):
        ids, exprs, data_type = self.visit(ctx.getChild(1))
        has_init_vals = bool(exprs)
        VarDeclare = ConstDecl if ctx.VAL() else VarDecl
        
        if has_init_vals:
            return [AttributeDecl(
                Static() if '$' in str(identifier) else Instance(),
                VarDeclare(identifier, data_type, expr)
            ) for identifier, expr in zip(ids, exprs)]

        init_val = None
        if is_class_type(data_type):
            init_val = NullLiteral()
        
        return [AttributeDecl(
            Static() if '$' in str(identifier) else Instance(),
            VarDeclare(identifier, data_type, init_val)
        ) for identifier in ids]


    # Visit a parse tree produced by D96Parser#attr_list_with_init_value.
    def visitAttr_list_with_init_value(self, ctx:D96Parser.Attr_list_with_init_valueContext):
        identifier = Id(ctx.getChild(0).getText())
        expr = self.visit(ctx.getChild(4))

        if ctx.Colon():
            return [identifier], [expr], self.visit(ctx.data_type())

        ids_tail, exprs_head, data_type = self.visit(ctx.attr_list_with_init_value())
        return [identifier] + ids_tail, exprs_head + [expr], data_type


    # Visit a parse tree produced by D96Parser#attr_list_with_type.
    def visitAttr_list_with_type(self, ctx:D96Parser.Attr_list_with_typeContext):
        identifier = Id(ctx.getChild(0).getText())

        if ctx.Colon():
            return [identifier], [], self.visit(ctx.data_type())
        
        ids_tail, exprs, data_type = self.visit(ctx.attr_list_with_type())
        return [identifier] + ids_tail, exprs, data_type


    # Visit a parse tree produced by D96Parser#method_decl_stmt.
    def visitMethod_decl_stmt(self, ctx:D96Parser.Method_decl_stmtContext):
        identifier = Id(ctx.getChild(0).getText())
        kind = Instance() if ctx.Identifier() else Static()
        body = self.visit(ctx.block_stmt())
        params = self.visit(ctx.param_list()) if ctx.param_list() else []
        return MethodDecl(kind, identifier, params, body)


    # Visit a parse tree produced by D96Parser#constructor_decl_stmt.
    def visitConstructor_decl_stmt(self, ctx:D96Parser.Constructor_decl_stmtContext):
        body = self.visit(ctx.block_stmt())
        constructor = Id(ctx.CONSTRUCTOR().getText())
        params = self.visit(ctx.param_list()) if ctx.param_list() else []
        return MethodDecl(Instance(), constructor, params, body)


    # Visit a parse tree produced by D96Parser#destructor_decl_stmt.
    def visitDestructor_decl_stmt(self, ctx:D96Parser.Destructor_decl_stmtContext):
        body = self.visit(ctx.block_stmt())
        destructor = Id(ctx.DESTRUCTOR().getText())
        return MethodDecl(Instance(), destructor, [], body)


    # Visit a parse tree produced by D96Parser#param_list.
    def visitParam_list(self, ctx:D96Parser.Param_listContext):
        child_count = ctx.getChildCount()

        ids, _, data_type = self.visit(ctx.identifier_list_with_type())

        var_decls = [VarDecl(identifier, data_type) for identifier in ids]

        if child_count == 1:
            return var_decls

        return var_decls + self.visit(ctx.param_list())


    # Visit a parse tree produced by D96Parser#block_stmt.
    def visitBlock_stmt(self, ctx:D96Parser.Block_stmtContext):
        return Block(self.visit(ctx.in_block_stmts()))


    # Visit a parse tree produced by D96Parser#in_block_stmts.
    def visitIn_block_stmts(self, ctx:D96Parser.In_block_stmtsContext):
        if ctx.getChildCount() == 0:
            return []
        return flatten([self.visit(ctx.getChild(0))] + self.visit(ctx.getChild(1)))


    # Visit a parse tree produced by D96Parser#expr.
    def visitExpr(self, ctx:D96Parser.ExprContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        return BinaryOp(ctx.getChild(1).getText(), self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))


    # Visit a parse tree produced by D96Parser#expr1.
    def visitExpr1(self, ctx:D96Parser.Expr1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        return BinaryOp(ctx.getChild(1).getText(), self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))


    # Visit a parse tree produced by D96Parser#expr2.
    def visitExpr2(self, ctx:D96Parser.Expr2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        return BinaryOp(ctx.getChild(1).getText(), self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))


    # Visit a parse tree produced by D96Parser#expr3.
    def visitExpr3(self, ctx:D96Parser.Expr3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        return BinaryOp(ctx.getChild(1).getText(), self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))


    # Visit a parse tree produced by D96Parser#expr4.
    def visitExpr4(self, ctx:D96Parser.Expr4Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        return BinaryOp(ctx.getChild(1).getText(), self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))


    # Visit a parse tree produced by D96Parser#expr5.
    def visitExpr5(self, ctx:D96Parser.Expr5Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        return UnaryOp(ctx.getChild(0).getText(), self.visit(ctx.getChild(1)))


    # Visit a parse tree produced by D96Parser#expr6.
    def visitExpr6(self, ctx:D96Parser.Expr6Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        return UnaryOp(ctx.getChild(0).getText(), self.visit(ctx.getChild(1)))


    # Visit a parse tree produced by D96Parser#expr7.
    # def visitExpr7(self, ctx:D96Parser.Expr7Context):
    #     pass


    # Visit a parse tree produced by D96Parser#index_expr.
    def visitIndex_expr(self, ctx:D96Parser.Index_exprContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        idx_list = self.visit(ctx.getChild(1))
        return ArrayCell(self.visit(ctx.getChild(0)), idx_list)


    # Visit a parse tree produced by D96Parser#index_operators.
    def visitIndex_operators(self, ctx:D96Parser.Index_operatorsContext):
        expr = self.visit(ctx.getChild(1))
        if ctx.getChildCount() == 3:
            return [expr]
        return [expr] + self.visit(ctx.getChild(3))


    # Visit a parse tree produced by D96Parser#expr8.
    def visitExpr8(self, ctx:D96Parser.Expr8Context):
        child_count = ctx.getChildCount()
        if child_count == 1:
            return self.visit(ctx.getChild(0))

        expr = self.visit(ctx.getChild(0))
        identifier = Id(ctx.getChild(2).getText())
        if child_count == 3:
            return FieldAccess(expr, identifier)
        
        param_list = self.visit(ctx.getChild(4))
        return CallExpr(expr, identifier, param_list)


    # Visit a parse tree produced by D96Parser#member_call.
    # def visitMember_call(self, ctx:D96Parser.Member_callContext):
    #     return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by D96Parser#attr_call.
    def visitAttr_call(self, ctx:D96Parser.Attr_callContext):
        return FieldAccess(self.visit(ctx.getChild(0)), Id(ctx.getChild(2).getText()))


    # Visit a parse tree produced by D96Parser#method_call.
    def visitMethod_call(self, ctx:D96Parser.Method_callContext):
        return CallStmt(self.visit(ctx.getChild(0)), Id(ctx.getChild(2).getText()), self.visit(ctx.getChild(4)))


    # Visit a parse tree produced by D96Parser#expr9.
    def visitExpr9(self, ctx:D96Parser.Expr9Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        return NewExpr(Id(ctx.getChild(1).getText()), self.visit(ctx.getChild(3)))


    # Visit a parse tree produced by D96Parser#atom.
    def visitAtom(self, ctx:D96Parser.AtomContext):
        if ctx.getChildCount() == 3:
            return self.visit(ctx.getChild(1))

        if ctx.NULL():
            return NullLiteral()

        if ctx.SELF():
            return SelfLiteral()

        if ctx.literal():
            return self.visit(ctx.literal())

        return Id(ctx.getChild(0).getText())


    # Visit a parse tree produced by D96Parser#expr_list.
    def visitExpr_list(self, ctx:D96Parser.Expr_listContext):
        child_count = ctx.getChildCount()
        if child_count == 0:
            return []
        expr = self.visit(ctx.getChild(0))
        if child_count == 1:
            return [expr]
        return [expr] + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by D96Parser#data_type.
    def visitData_type(self, ctx:D96Parser.Data_typeContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by D96Parser#primitive_type.
    def visitPrimitive_type(self, ctx:D96Parser.Primitive_typeContext):
        if ctx.INT():
            return IntType()
        if ctx.FLOAT():
            return FloatType()
        if ctx.BOOL():
            return BoolType()
        return StringType()


    # Visit a parse tree produced by D96Parser#array_type.
    def visitArray_type(self, ctx:D96Parser.Array_typeContext):
        return ArrayType(int(ctx.Intliteral().getText()), self.visit(ctx.element_type()))


    # Visit a parse tree produced by D96Parser#element_type.
    def visitElement_type(self, ctx:D96Parser.Element_typeContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by D96Parser#class_type.
    def visitClass_type(self, ctx:D96Parser.Class_typeContext):
        return ClassType(Id(ctx.Identifier().getText()))


    # Visit a parse tree produced by D96Parser#literal.
    def visitLiteral(self, ctx:D96Parser.LiteralContext):
        first_child = ctx.getChild(0)
        if type(first_child) is D96Parser.Array_literalContext:
            return self.visit(first_child)
        if ctx.Intliteral():
            intlit_text = first_child.getText()
            if '0x' in intlit_text or '0X' in intlit_text:
                return IntLiteral(int(intlit_text, base=16))
            if '0b' in intlit_text or '0B' in intlit_text:
                return IntLiteral(int(intlit_text, base=2))
            if intlit_text[0] == '0' and len(intlit_text) > 1:
                return IntLiteral(int(intlit_text, base=8))
            return IntLiteral(int(intlit_text))
        if ctx.Realliteral():
            return FloatLiteral(float(first_child.getText()))
        if ctx.Boolliteral():
            return BooleanLiteral(True if first_child.getText() == 'True' else False) 
        return StringLiteral(first_child.getText())


    # Visit a parse tree produced by D96Parser#array_literal.
    def visitArray_literal(self, ctx:D96Parser.Array_literalContext):
        return ArrayLiteral(self.visit(ctx.element_list()))


    # Visit a parse tree produced by D96Parser#element_list.
    def visitElement_list(self, ctx:D96Parser.Element_listContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.getChild(0))]
        return [self.visit(ctx.getChild(0))] + self.visit(ctx.getChild(2))