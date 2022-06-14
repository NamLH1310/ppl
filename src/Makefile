TARGET=../target/main/d96/parser

all:
	python run.py gen 
	python run.py test LexerSuite
	python run.py test ParserSuite
	python run.py test ASTGenSuite
	python run.py test CheckerSuite
	python run.py test CodeGenSuite
gen:
	python run.py gen
ast:
	python run.py test ASTGenSuite
parser:
	python run.py test ParserSuite
checker:
	python run.py test CheckerSuite
codegen:
	python run.py test CodeGenSuite
clean:
	rm -rf ../target/*