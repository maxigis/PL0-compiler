from main.FileUtils import write_bin
from main.FileUtils import make_executable
from main.Parser import Parser
from main.Scanner import Scanner
from ParseError import ParseError
from main.Semantic import Semantic
from main.CodeGenerator import CodeGenerator
from main.CompilationResult import CompilationResult


def compile(data, output=None):
    tokenizer = Scanner(data)

    try:
        semantic = Semantic()
        code_generator = CodeGenerator()
        parser = Parser(tokenizer, semantic, code_generator)
        return parser.parse()
    except ParseError as e:
        print('Error de sintaxis, en linea ' + str(
            e.token.lineno) + ' se esperaba ' + e.expected + ' y se encontro ' + e.token.value)
        print(str.splitlines(data)[e.token.lineno - 1])
        return CompilationResult(False, None, [e])
