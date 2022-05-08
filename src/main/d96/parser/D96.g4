// @lexer::members { def emit(self): tk = self.type result = super().emit() if tk == self.UNCLOSE_STRING: print('unclose') raise
// UncloseString(result.text) elif tk == self.ERROR_CHAR: print('char') raise ErrorToken(result.text) return result }// TODO: Illegal escape ILLEGAL_ESCAPE: . ;// $antlr-format false
// $antlr-format columnLimit 150
// $antlr-format allowShortBlocksOnASingleLine true, indentWidth 8
// 1914220
grammar D96;

@lexer::header {
from lexererr import *
}

options {
	language = Python3;
}

program: class_decl_stmt+ EOF;

assign_stmt
	: assign_lhs Eq expr Semi
	;

assign_lhs
    : Identifier
	| DolarIdentifier
    | index_expr
	| attr_call
    ;

if_stmt
    : if_clause else_stmt
    ;

else_stmt
	: elseif_clause else_stmt
	| else_clause
	|
	;

// elseif_stmt_sequence
//     : elseif_clause elseif_stmt_sequence
//   	| elseif_clause
//     ;

if_clause
    : IF OpenRoundBracket expr CloseRoundBracket block_stmt
    ;

elseif_clause
    : ELSEIF OpenRoundBracket expr CloseRoundBracket block_stmt
    ;

else_clause
    : ELSE block_stmt
    ;

for_stmt
    : FOREACH OpenRoundBracket Identifier IN expr DDot expr step_decl CloseRoundBracket block_stmt
    ;

step_decl
    : BY expr
    |
    ;

break_stmt
    : BREAK Semi
    ;

continue_stmt
    : CONTINUE Semi
    ;

return_stmt
    : RETURN expr? Semi
    ;

var_decl_stmt
	: (VAL | VAR) (identifier_list_with_type | identifier_list_with_init_value) Semi
	// : (VAL | VAR) identifier_list_with_init_value Semi
	// | VAR identifier_list_with_type Semi
	;

identifier_list_with_init_value
	: Identifier Comma identifier_list_with_init_value Comma expr
	| Identifier Colon data_type Eq expr
	;

identifier_list_with_type
	: Identifier Comma identifier_list_with_type
	| Identifier Colon data_type
	;

class_decl_stmt
	: CLASS Identifier super_class_decl OpenBracket class_member_decl CloseBracket
	;

super_class_decl
	: Colon Identifier
	|
	;

class_member_decl
	: (attr_decl_stmt
	  | constructor_decl_stmt
	  | destructor_decl_stmt
	  | method_decl_stmt) class_member_decl
	|
	;

// main_class_decl
// 	: CLASS PROGRAM OpenBracket main_class_member_decl CloseBracket
// 	;

// main_class_member_decl
// 	: class_member_decl main_method_decl class_member_decl
// 	;

// main_method_decl
// 	: MAIN OpenRoundBracket CloseRoundBracket block_stmt
// 	;

attr_decl_stmt
	: (VAL | VAR) (attr_list_with_type | attr_list_with_init_value) Semi
	// : (VAL | VAR) attr_list_with_init_value Semi
	// | VAR attr_list_with_type Semi
	;

attr_list_with_init_value
	: (Identifier | DolarIdentifier) Comma attr_list_with_init_value Comma expr
	| (Identifier | DolarIdentifier) Colon data_type Eq expr
	;

attr_list_with_type
	: (Identifier | DolarIdentifier) Comma attr_list_with_type
	| (Identifier | DolarIdentifier) Colon data_type
	;

method_decl_stmt
	: (Identifier | DolarIdentifier) OpenRoundBracket param_list? CloseRoundBracket block_stmt
	;

constructor_decl_stmt
	: CONSTRUCTOR OpenRoundBracket param_list? CloseRoundBracket block_stmt
	;

destructor_decl_stmt
	: DESTRUCTOR OpenRoundBracket CloseRoundBracket block_stmt
	;

param_list
	: identifier_list_with_type Semi param_list
	| identifier_list_with_type
	;

block_stmt
	: OpenBracket in_block_stmts CloseBracket
	;

in_block_stmts
	: ( assign_stmt
	  | if_stmt
	  | for_stmt
	  | break_stmt
	  | continue_stmt
	  | var_decl_stmt
	  | method_call
	  | block_stmt
	  | return_stmt) in_block_stmts
	|
	;

expr
	: expr1 op=(PlusDot | EEqDot) expr1
    | expr1
	;

expr1
    : expr2 op=(EEq | BangEq | Less | Greater | LessEq | GreaterEq) expr2
    | expr2
    ;

expr2
    : expr2 op=(AAmpersand | PPipe) expr3
    | expr3
    ;

expr3
    : expr3 op=(Plus | Minus) expr4
    | expr4
    ;

expr4
    : expr4 op=(Asterisk | Divide | Percent) expr5
    | expr5
    ;

expr5
    : Bang expr5
    | expr6
    ;

expr6
    : Minus expr6
    | index_expr
    ;

// expr7
//     // : expr7 OpenSquareBracket expr CloseSquareBracket 
// 	: index_expr
//     | expr8
//     ;

index_expr
	: expr8 index_operators
	| expr8
	;

index_operators
	: OpenSquareBracket expr CloseSquareBracket
	| OpenSquareBracket expr CloseSquareBracket index_operators
	;

expr8
    : expr8 (CColon | Dot) (Identifier | DolarIdentifier)
    | expr8 (CColon | Dot) (Identifier | DolarIdentifier) OpenRoundBracket expr_list CloseRoundBracket
    | expr9
    ;

// member_call
//     : attr_call
//     | method_call
// 	;

attr_call
	: expr (CColon | Dot) (Identifier | DolarIdentifier)
	;

method_call
	: expr (CColon | Dot) (Identifier | DolarIdentifier) OpenRoundBracket expr_list CloseRoundBracket Semi
	;

expr9
    : NEW Identifier OpenRoundBracket expr_list CloseRoundBracket
    | atom
    ;

atom
    : literal
    | OpenRoundBracket expr CloseRoundBracket
    | Identifier
	| DolarIdentifier
	| NULL
	| SELF
    ;

expr_list
	: expr Comma expr_list
	| expr
	|
	;

data_type
	: primitive_type
	| array_type
	| class_type
	;

primitive_type
	: INT
	| FLOAT
	| BOOL
	| STRING
	;

array_type
	: ARRAY OpenSquareBracket element_type Comma Intliteral CloseSquareBracket
	;

element_type
	: array_type
	| primitive_type
	;


class_type
	: Identifier
	;

literal
	: Intliteral
	| Realliteral
	| Boolliteral
	| Stringliteral
	| array_literal
	;

array_literal: ARRAY OpenRoundBracket element_list CloseRoundBracket ;

element_list
	: expr Comma element_list
	| expr
	;

// KEYWORDS
// PROGRAM     : 'Program';
// MAIN        : 'main';
CLASS       : 'Class';
SELF        : 'Self';
VAL         : 'Val';
VAR         : 'Var';
BREAK       : 'Break';
CONTINUE    : 'Continue';
IF          : 'If';
ELSEIF      : 'Elseif';
ELSE        : 'Else';
FOREACH     : 'Foreach';
ARRAY       : 'Array';
IN          : 'In';
INT         : 'Int';
FLOAT       : 'Float';
BOOL        : 'Boolean';
STRING      : 'String';
RETURN      : 'Return';
NULL        : 'Null';
CONSTRUCTOR : 'Constructor';
DESTRUCTOR  : 'Destructor';
NEW         : 'New';
BY          : 'By';
fragment TRUE        : 'True';
fragment FALSE       : 'False';

// OPERATORS
Plus               : '+';
Minus              : '-';
Asterisk           : '*';
Divide             : '/';
Percent            : '%';
Bang               : '!';
AAmpersand         : '&&';
PPipe              : '||';
EEq                : '==';
Eq                 : '=';
BangEq             : '!=';
Greater            : '>';
GreaterEq          : '>=';
Less               : '<';
LessEq             : '<=';
EEqDot             : '==.';
PlusDot            : '+.';
CColon             : '::';
Colon              : ':';
Comma              : ',';
Semi               : ';';
DDot               : '..';
OpenRoundBracket   : '(';
CloseRoundBracket  : ')';
OpenSquareBracket  : '[';
CloseSquareBracket : ']';
OpenBracket        : '{';
CloseBracket       : '}';



fragment Digits: [0-9]+;

Intliteral: ('0' | Decliteral | Hexliteral | Octliteral | Binliteral)
{
self.text = self.text.replace('_', '')
}
;

fragment Decliteral: [1-9] [0-9_]* ;
fragment Hexliteral: '0' [xX] [0-9A-F_]+ ;
fragment Octliteral: '0' [0-7_]+ ;
fragment Binliteral: '0' [bB] [01_]+ ;

Boolliteral: TRUE | FALSE;

Identifier: [a-zA-Z_] [a-zA-Z0-9_]* ;
DolarIdentifier: Dolar [a-zA-Z0-9_]+;
fragment Dolar              : '$';

fragment RealDecPart: Dot [0-9]*;
fragment RealExpPart: [eE] [+-]? Digits;
Realliteral: (Decliteral | '0') (RealDecPart RealExpPart? | RealExpPart)
{
self.text = self.text.replace('_','').replace('+','')
}
;

// fragement 

// SEPARATORS
Dot                : '.';

COMMENT: '##' (~[EOF])*? '##' -> skip;

Stringliteral: '"' STR_CHAR* '"'
{
y = str(self.text)
self.text = y[1:-1].replace('\'"','"')
}
;


WS: [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines


UNCLOSE_STRING: '"' STR_CHAR* ( [\b\t\n\f\r"'\\] | EOF )
{
possible = ['\b', '\t', '\n', '\f', '\r', '"', "'", '\\']
if self.text[-1] in possible:
    raise UncloseString(self.text[1:-1])
else:
    raise UncloseString(self.text[1:])
}
;
ILLEGAL_ESCAPE: '"' STR_CHAR* ESC_ILLEGAL
{
raise IllegalEscape(self.text[1:])
}
;
fragment STR_CHAR: ~[\b\t\n\f\r"'\\] | ESC_SEQ | '\'"';

fragment ESC_SEQ: '\\' [btnfr"'\\] ;
fragment ESC_ILLEGAL: '\\' ~[btnfr"'\\] | ~'\\' ;
ERROR_CHAR: .
{
raise ErrorToken(self.text)
}
;