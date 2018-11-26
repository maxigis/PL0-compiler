from ParseError import ParseError
from main.Compiler import compile
from main.FileUtils import read_file
from main.FileUtils import write_bin
from main.FileUtils import make_executable
import logging


logging.basicConfig(level=logging.INFO)

try:
    output = 'program'
    data = read_file('../resources/bien/BIEN-01.PL0')
    result = compile(data)
    if result.success:
        write_bin(output, bytearray(result.bytes))
        make_executable(output)
    else:
        e = result.errors[0]
        print('Error de sintaxis, en linea ' + str(e.token.lineno) + ' se esperaba ' + e.expected + ' y se encontro ' + e.token.value)
except ParseError as e:
    print('Error de sintaxis, en linea ' + str(e.token.lineno) + ' se esperaba ' + e.expected + ' y se encontro ' + e.token.value)
