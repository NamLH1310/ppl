
"""
 * @author Lê Hoàng Nam
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *


@dataclass
class Context:
    has_entry_point = False
    has_array_cell_error = False
    has_value = True
    is_param = False
    is_vardecl = False
    is_constDecl = False
    is_assign = False
    is_classmember = False
    is_static = False
    is_assign_to_const = False
    is_call_member = False
    is_init_decl = False
    is_in_for_stmt = False
    is_in_static_method = False
    is_const_init_val = False
    unknown_expr_value = False
    passdown_ast = None
    call_method_name = None
    self_literal = None
    current_class_name = None
    current_method_name = None
    param_type_list = []
    field_name = None

def get_class_member_type(
    scope_table: dict,
    decl: ClassDecl,
    mem_name: str,
    context: Context,
    method_return_table: dict,
    is_attr: bool
    ) -> Type:
    if mem_name == 'Constructor' and not is_attr:
        method_names = [mem.name.name for mem in decl.memlist if type(mem) is MethodDecl]
        if mem_name not in method_names :
            if not context.param_type_list:
                return
            else:
                context.param_type_list = None
        else:
            for mem in decl.memlist:
                if type(mem) is MethodDecl and mem.name.name == 'Constructor':
                    if len(mem.param) != len(context.param_type_list):
                        context.param_type_list = None
                    else: 
                        for param, arg in zip(mem.param, context.param_type_list):
                            if type(param.varType) is not type(arg):
                                context.param_type_list = None
                                break
                            elif type(param.varType) is ArrayType and (param.varType.size != arg.size or type(param.varType.eleType) is not type(arg.eleType)):
                                context.param_type_list = None
                                break
                            elif type(param.varType) is ClassType and not is_sub_class(scope_table[param.varType.classname.name], scope_table[arg.classname.name], scope_table):
                                context.param_type_list = None
                                break
                    break
        return

    for mem in decl.memlist:
        if is_attr and type(mem) is AttributeDecl:
            attr_name = mem.decl.variable.name if type(mem.decl) is VarDecl else mem.decl.constant.name
            if attr_name == mem_name:
                if type(mem.decl) is ConstDecl:
                    if context.is_assign:
                        context.is_assign_to_const = True
                    return mem.decl.constType
                else:
                    return mem.decl.varType
        elif not is_attr and type(mem) is MethodDecl:
            class_name = decl.classname.name
            method_name = mem.name.name
            if mem_name == method_name:
                if len(mem.param) != len(context.param_type_list):
                    context.param_type_list = None
                else: 
                    for param, arg in zip(mem.param, context.param_type_list):
                        if type(param.varType) is not type(arg):
                            context.param_type_list = None
                            break
                        elif type(param.varType) is ArrayType and (param.varType.size != arg.size or type(param.varType.eleType) is not type(arg.eleType)):
                            context.param_type_list = None
                            break
                        elif type(param.varType) is ClassType and not is_sub_class(scope_table[param.varType.classname.name], scope_table[arg.classname.name], scope_table):
                            context.param_type_list = None
                            break

                return method_return_table[class_name + '.' + method_name]

    if decl.parentname:
        return get_class_member_type(scope_table, scope_table[decl.parentname.name], mem_name, context, method_return_table, is_attr)
    
    if is_attr:
        raise Undeclared(Attribute(), mem_name)
    else:
        raise Undeclared(Method(), mem_name)

def get_array_cell_type(array_type: ArrayType, level: int, ast):
    ele_type = array_type.eleType
    if level == 1:
        return ele_type

    # level > 1
    if type(ele_type) is ArrayType:
        return get_array_cell_type(ele_type, level - 1, ast)
    
    raise TypeMismatchInExpression(ast)

def is_sub_class(class_decl_parent: ClassDecl, class_decl_child: ClassDecl, scope: dict):
    if class_decl_parent.classname.name == class_decl_child.classname.name:
        return True
    if not class_decl_child.parentname:
        return False
    if class_decl_parent.classname.name == class_decl_child.parentname.name:
        return True
    return is_sub_class(class_decl_parent, scope[class_decl_child.parentname.name], scope)


class StaticChecker(BaseVisitor,Utils):
    
    def __init__(self, ast):
        self.method_return_type = {}
        self.has_value = {}
        self.ast = ast
        self.context = Context()
    
    def check(self):
        global_scope = [{}]
        return self.visit(self.ast, global_scope)

    def visitProgram(self, ast: Program, scope): 
        for decl in ast.decl:
            self.visit(decl, scope)
            
        if not self.context.has_entry_point:
            raise NoEntryPoint()
        return []
    
    def visitClassDecl(self, ast: ClassDecl, scopes: list[dict]):
        class_name = ast.classname.name
        if class_name in scopes[0]:
            raise Redeclared(Class(), class_name)

        scopes[0][class_name] = ast

        if ast.parentname and ast.parentname.name not in scopes[0]:
            raise Undeclared(Class(), ast.parentname.name) 
            
        self.context.current_class_name = class_name
        new_scopes = [{}] + scopes
        for decl in ast.memlist:
            self.visit(decl, new_scopes)
        self.context.current_class_name = None
        
    def visitMethodDecl(self, ast: MethodDecl, scopes: list[dict]):
        method_name = ast.name.name
        if method_name in scopes[0]:
            if type(scopes[0][method_name]) is MethodDecl:
                raise Redeclared(Method(), method_name)
            else:
                raise Redeclared(Identifier(), method_name)

        if method_name == 'main' and self.context.current_class_name == 'Program':
            self.context.has_entry_point = True
            if ast.param:
                self.context.has_entry_point = False

        scopes[0][method_name] = ast
        
        new_scopes = [{}] + scopes
        self.context.is_param = True
        for decl in ast.param:
            self.visit(decl, new_scopes)
        self.context.is_in_static_method = '$' in method_name or type(ast.kind) is Static
        self.context.is_param = False
        self.context.current_method_name = method_name
        key = self.context.current_class_name + '.' + self.context.current_method_name
        self.method_return_type[key] = None
        self.visit(ast.body, new_scopes)
        self.context.current_method_name = None
        if not self.method_return_type[key]:
            self.method_return_type[key] = VoidType()

    
    def visitAttributeDecl(self, ast: AttributeDecl, scopes: list[dict]):
        decl = ast.decl
        self.context.is_classmember = True
        self.visit(decl, scopes)
        self.context.is_classmember = False
        attr_name = decl.variable.name if type(decl) is VarDecl else decl.constant.name
        scopes[0][attr_name] = ast
    
    def visitVarDecl(self, ast: VarDecl, scopes: list[dict]):
        var_name = ast.variable.name
        if var_name in scopes[0]:
            if self.context.is_param:
                raise Redeclared(Parameter(), var_name)
            elif self.context.is_classmember and type(scopes[0][var_name].decl) is VarDecl:
                raise Redeclared(Attribute(), var_name)
            elif type(scopes[0][var_name]) is VarDecl:
                raise Redeclared(Variable(), var_name)
            raise Redeclared(Identifier(), var_name)
        
        if type(ast.varType) is ClassType and ast.varType.classname.name not in scopes[-1]:
            raise Undeclared(Class(), ast.varType.classname.name)

        scopes[0][var_name] = ast

        if ast.varInit:
            init_val_type = self.visit(ast.varInit, scopes)

            if self.context.is_classmember:
                self.has_value[self.context.current_class_name + '.' + var_name] = self.context.has_value
            else:
                scopes[0][f'#{var_name}'] = self.context.has_value

            if type(ast.varType) is FloatType and type(init_val_type) not in (IntType, FloatType):
                raise TypeMismatchInStatement(ast)
            elif type(ast.varType) is not FloatType and type(init_val_type) is not type(ast.varType):
                raise TypeMismatchInStatement(ast)
            elif type(init_val_type) is ClassType:
                if not is_sub_class(scopes[-1][ast.varType.classname.name], scopes[-1][init_val_type.classname.name], scopes[-1]):
                    raise TypeMismatchInStatement(ast)
            elif type(init_val_type) is ArrayType:
                if init_val_type.size != ast.varType.size or type(init_val_type.eleType) is not type(ast.varType.eleType):
                    raise TypeMismatchInStatement(ast)
                
        else:
            if self.context.is_classmember:
                self.has_value[self.context.current_class_name + '.' + var_name] = False
            else:
                scopes[0][f'#{var_name}'] = False

        return ast.varType
        
    def visitConstDecl(self, ast: ConstDecl, scopes: list[dict]):
        const_name = ast.constant.name
        if const_name in scopes[0]:
            if self.context.is_classmember and type(scopes[0][const_name].decl) is ConstDecl:
                raise Redeclared(Attribute(), const_name)
            elif type(scopes[0][const_name]) is ConstDecl:
                raise Redeclared(Constant(), const_name)
            raise Redeclared(Identifier(), const_name)

        if type(ast.constType) is ClassType and ast.constType.classname.name not in scopes[-1]:
            raise Undeclared(Class(), ast.constType.classname.name)

        scopes[0][const_name] = ast
        
        if ast.value:
            init_val_type = self.visit(ast.value, scopes)
            if type(ast.constType) is FloatType and type(init_val_type) not in (IntType, FloatType):
                raise TypeMismatchInConstant(ast)
            elif type(ast.constType) is not FloatType and type(init_val_type) is not type(ast.constType):
                raise TypeMismatchInConstant(ast)
            elif type(init_val_type) is ClassType:
                if not is_sub_class(scopes[-1][ast.constType.classname.name], scopes[-1][init_val_type.classname.name], scopes[-1]):
                    raise TypeMismatchInConstant(ast)
            elif type(init_val_type) is ArrayType:
                if init_val_type.size != ast.constType.size or type(init_val_type.eleType) is not type(ast.constType.eleType):
                    raise TypeMismatchInConstant(ast)

            if self.context.is_classmember:
                self.has_value[self.context.current_class_name + '.' + const_name] = True
            else:
                scopes[0][f'#{const_name}'] = True
        else:
            raise IllegalConstantExpression(None)


        return ast.constType
        
    def visitBlock(self, ast: Block, scopes: list[dict]):
        for stmt in ast.inst:
            if type(stmt) is Block:
                self.visit(stmt, [{}] + scopes)
            else:
                self.visit(stmt, scopes)

    def visitAssign(self, ast: Assign, scopes: list[dict]):
        rhs = self.visit(ast.exp, scopes)
        
        self.context.is_assign = True
        lhs = self.visit(ast.lhs, scopes)

        if self.context.is_assign_to_const:
            raise CannotAssignToConstant(ast)
        
        if type(lhs) is FloatType and type(rhs) not in (FloatType, IntType):
            raise TypeMismatchInStatement(ast)
        elif type(lhs) is not FloatType and type(lhs) is not type(rhs) or type(lhs) is VoidType:
            raise TypeMismatchInStatement(ast)
        elif type(lhs) is type(rhs):
            if type(lhs) is ArrayType and (type(lhs.eleType) is not type(rhs.eleType) or lhs.size != rhs.size):
                raise TypeMismatchInStatement(ast)
            elif type(lhs) is ClassType and not is_sub_class(scopes[-1][lhs.classname.name], scopes[-1][rhs.classname.name], scopes[-1]):
                raise TypeMismatchInStatement(ast)
        
        self.context.is_assign = False
        self.context.is_assign_to_const = False 
        
    def visitCallStmt(self, ast: CallStmt, scopes: list[dict]):
        method_name = ast.method.name
        is_static = '$' in method_name
        self.context.param_type_list = [self.visit(expr, scopes) for expr in ast.param]
        self.context.is_call_member = True
        call_stmt_type = self.visit(ast.obj, scopes) 
        self.context.is_call_member = False
        
        if type(call_stmt_type) is ClassDecl:
            if is_static:
                method_type = get_class_member_type(
                    scopes[-1],
                    call_stmt_type,
                    method_name,
                    self.context,
                    self.method_return_type,
                    False
                )
            else:
                IllegalMemberAccess(ast)
        elif type(call_stmt_type) is ClassType:
            if not is_static:
                method_type = get_class_member_type(
                    scopes[-1],
                    scopes[-1][call_stmt_type.classname.name],
                    method_name,
                    self.context,
                    self.method_return_type,
                    False
                )
            else:
                IllegalMemberAccess(ast)
        
        if type(method_type) is not VoidType or self.context.param_type_list is None:
            raise TypeMismatchInStatement(ast)
            
    
    def visitCallExpr(self, ast: CallExpr, scopes: list[dict]):
        method_name = ast.method.name
        is_static = '$' in method_name
        self.context.param_type_list = [self.visit(expr, scopes) for expr in ast.param]
        self.context.is_call_member = True
        call_expr_type = self.visit(ast.obj, scopes) 
        self.context.is_call_member = False
        if type(call_expr_type) is ClassDecl:
            if is_static:
                method_type = get_class_member_type(
                    scopes[-1],
                    call_expr_type,
                    method_name,
                    self.context,
                    self.method_return_type,
                    False
                )
            else:
                IllegalMemberAccess(ast)
        elif type(call_expr_type) is ClassType:
            if not is_static:
                method_type = get_class_member_type(
                    scopes[-1],
                    scopes[-1][call_expr_type.classname.name],
                    method_name,
                    self.context,
                    self.method_return_type,
                    False
                )
            else:
                IllegalMemberAccess(ast)
        
        if type(method_type) is VoidType or self.context.param_type_list is None:
            raise TypeMismatchInExpression(ast)
        
        return method_type


    def visitBinaryOp(self, ast: BinaryOp, scopes: list[dict]):
        left = self.visit(ast.left, scopes)
        right = self.visit(ast.right, scopes)
        op = ast.op
        
        if type(left) is ClassDecl:
            raise Undeclared(Identifier(), left.classname.name)
        elif type(left) is MethodDecl:
            raise Undeclared(Identifier(), left.name.name)
        if type(right) is ClassDecl:
            raise Undeclared(Identifier(), right.classname.name)
        elif type(right) is MethodDecl:
            raise Undeclared(Identifier(), right.name.name)
        
        if op in ('==', '!='):
            if type(left) not in (IntType, BoolType) or type(right) not in (IntType, BoolType) or type(left) is not type(right):
                raise TypeMismatchInExpression(ast)
            return_type = BoolType()
        elif op in ('>', '<', '>=', '<='):
            if type(left) not in (IntType, FloatType) or type(right) not in (IntType, FloatType):
                raise TypeMismatchInExpression(ast)
            return_type = BoolType()
        elif op in ('!', '&&', '||'):
            if type(left) is not BoolType or type(right) is not BoolType:
                raise TypeMismatchInExpression(ast)
            return_type = BoolType()
        elif op == '==.':
            if type(left) is not StringType or type(right) is not StringType:
                raise TypeMismatchInExpression(ast)
            return_type = BoolType()
        elif op == '+.':
            if type(left) is not StringType or type(right) is not StringType:
                raise TypeMismatchInExpression(ast)
            return_type = StringType()
        elif op in ('+', '-', '*', '/'):
            if type(left) not in (IntType, FloatType) or type(right) not in (IntType, FloatType):
                raise TypeMismatchInExpression(ast)
            if type(left) is FloatType or type(right) is FloatType:
                return_type = FloatType()
            else:
                return_type = IntType()
        elif op == '%':
            if type(left) is not IntType or type(right) is not IntType:
                raise TypeMismatchInExpression(ast)
            return_type = IntType()
        return return_type


    def visitUnaryOp(self, ast: UnaryOp, scopes: list[dict]):
        op = ast.op
        expr = self.visit(ast.body, scopes)
        if op == '-':
            if type(expr) not in (IntType, FloatType):
                raise TypeMismatchInExpression(ast)
            return_type = expr
        elif op == '!':
            if type(expr) is not BoolType:
                raise TypeMismatchInExpression(ast)
            return_type = BoolType()
        return return_type


    def visitFieldAccess(self, ast: FieldAccess, scopes: list[dict]):
        if self.context.is_in_static_method and type(ast.obj) is SelfLiteral:
            raise IllegalMemberAccess(ast)

        field_name = ast.fieldname.name
        is_static = '$' in field_name
        is_call_member = self.context.is_call_member
        self.context.is_call_member = True
        obj_type = self.visit(ast.obj, scopes)
        self.context.is_call_member = is_call_member
        if type(obj_type) is ClassDecl:
            # Static
            if is_static:
                return_type = get_class_member_type(
                    scopes[-1],
                    obj_type,
                    field_name,
                    self.context,
                    self.method_return_type,
                    True
                )
                if self.context.is_assign:
                    ...
                if self.context.is_const_init_val and not self.has_value[obj_type.classname.name + '.' + field_name]:
                    self.context.has_value = False
                return return_type
            else:
                raise IllegalMemberAccess(ast)
        elif type(obj_type) is ClassType:
            # Instance
            if not is_static:
                class_name = obj_type.classname.name
                class_decl = scopes[-1][class_name]
                return_type = get_class_member_type(
                    scopes[-1],
                    class_decl,
                    field_name,
                    self.context,
                    self.method_return_type,
                    True
                )
                if self.context.is_const_init_val and not self.has_value[class_decl.classname.name + '.' + field_name]:
                    self.context.has_value = False
                return return_type
            else:
                raise IllegalMemberAccess(ast)
        raise TypeMismatchInExpression(ast)
        
    
    def visitSelfLiteral(self, ast: SelfLiteral, scopes: list[dict]):
        obj_class_name = self.context.current_class_name
        return ClassType(Id(obj_class_name))
    
    def visitArrayCell(self, ast: ArrayCell, scopes: list[dict]):
        arr_type = self.visit(ast.arr, scopes)
        if type(arr_type) is not ArrayType:
            raise TypeMismatchInExpression(ast)
        for expr in ast.idx:
            if type(self.visit(expr, scopes)) is not IntType:
                raise TypeMismatchInExpression(ast)
        
        level = len(ast.idx)
        return get_array_cell_type(arr_type, level, ast)
        
    
    def visitIf(self, ast: If, scopes: list[dict]):
        expr_type = self.visit(ast.expr, scopes)
        if type(expr_type) is not BoolType:
            raise TypeMismatchInStatement(ast)
        self.visit(ast.thenStmt, [{}] + scopes)
        if type(ast.elseStmt) is Block:
            self.visit(ast.elseStmt, [{}] + scopes)
        elif type(ast.elseStmt) is If:
            self.visit(ast.elseStmt, scopes)
        

    def visitFor(self, ast: For, scopes: list[dict]):
        expr1 = self.visit(ast.expr1, scopes)
        expr2 = self.visit(ast.expr2, scopes)
        if type(expr1) is not IntType or type(expr2) is not IntType:
            raise TypeMismatchInStatement(ast)
        if ast.expr3 and type(self.visit(ast.expr3, scopes)) is not IntType:
            raise TypeMismatchInStatement(ast)
        new_scopes = [{}] + scopes
        new_scopes[0][ast.id.name] = VarDecl(ast.id, IntType())
        self.context.is_in_for_stmt = True
        self.visit(ast.loop, new_scopes)
        self.context.is_in_for_stmt = False

        
    def visitBreak(self, ast: Break, scopes: list[dict]):
        if not self.context.is_in_for_stmt:
            raise MustInLoop(ast)

        
    def visitContinue(self, ast: Continue, scopes: list[dict]):
        if not self.context.is_in_for_stmt:
            raise MustInLoop(ast)
        
        
    def visitReturn(self, ast: Return, scopes: list[dict]):
        class_name = self.context.current_class_name
        method_name = self.context.current_method_name
        if class_name == 'Program' and method_name == 'main' or method_name == 'Constructor' or method_name == 'Destructor':
            if ast.expr:
                raise TypeMismatchInStatement(ast)
        key = class_name + '.' + method_name

        if not self.method_return_type[key]:
            if not ast.expr:
                self.method_return_type[key] = VoidType()
            else:
                expr_type = self.visit(ast.expr, scopes)
                self.method_return_type[key] = expr_type
        else:
            if not ast.expr and type(self.method_return_type[key]) is not VoidType:
                raise TypeMismatchInStatement(ast)
            if ast.expr:
                expr_type = self.visit(ast.expr, scopes)
                if type(expr_type) is not type(self.method_return_type[key]):
                    raise TypeMismatchInStatement(ast)
        
    def visitIntLiteral(self, ast, _):
        return IntType()

    def visitFloatLiteral(self, ast, _):
        return FloatType()
    
    def visitBooleanLiteral(self, ast, _):
        return BoolType()
    
    def visitStringLiteral(self, ast, _):
        return StringType()
    
    def visitNullLiteral(self, ast: NullLiteral, _):
        ...
    
    def visitArrayLiteral(self, ast: ArrayLiteral, scopes: list[dict]):
        arr_type = [self.visit(expr, scopes) for expr in ast.value]
        pivot_type = arr_type[0]
        for ele_type in arr_type[1:]:
            if type(pivot_type) is not type(ele_type):
                raise IllegalArrayLiteral(ast)
        return ArrayType(len(arr_type), pivot_type)
    
    def visitNewExpr(self, ast: NewExpr, scopes: list[dict]):
        class_name = ast.classname.name
        self.context.param_type_list = [self.visit(expr, scopes) for expr in ast.param]
        get_class_member_type(
            scopes[-1],
            scopes[-1][class_name],
            'Constructor',
            self.context,
            self.method_return_type,
            False
        )
        if self.context.param_type_list is None:
            raise TypeMismatchInExpression(ast)
        return ClassType(ast.classname)
        
    def visitId(self, ast: Id, scopes: list[dict]):
        for scope in scopes:
            if ast.name in scope:
                if type(scope[ast.name]) is ConstDecl:
                    if self.context.is_assign:
                        self.context.is_assign_to_const = True
                    return scope[ast.name].constType
                elif type(scope[ast.name]) is VarDecl:
                    if self.context.is_const_init_val:
                        self.context.has_value = scope[f'#{ast.name}']
                    return scope[ast.name].varType
                elif type(scope[ast.name]) is AttributeDecl:
                    break
                # ClassDecl or MethodDecl
                return scope[ast.name]

        if self.context.is_call_member:
            raise Undeclared(Class(), ast.name)
        raise Undeclared(Identifier(), ast.name)
