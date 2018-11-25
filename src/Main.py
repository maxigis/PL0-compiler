from Parser import Parser
from Scanner import Scanner
from ParseError import ParseError
from Semantic import Semantic
from CodeGenerator import CodeGenerator
import logging


def read_file(archivo):
    lines = []
    try:
        file = open(archivo)
    except IOError:
        raise IOError("Error reading file")
    for line in file:
        lines.append(line)
    file.close()
    return " ".join(lines)


data = read_file('../resources/bien/BIEN-01.PL0')

tokenizer = Scanner(data)

parser = Parser(tokenizer)
logging.basicConfig(level=logging.INFO)

try:
    semantic = Semantic()
    codeGenerator = CodeGenerator("program")
    parser.parse(semantic, codeGenerator)
except ParseError as e:
    print('Error de sintaxis, en linea ' + str(
        e.token.lineno) + ' se esperaba ' + e.expected + ' y se encontro ' + e.token.value)
    print(str.splitlines(data)[e.token.lineno - 1])
