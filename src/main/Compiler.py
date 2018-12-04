import traceback

from main.FileUtils import write_bin
from main.FileUtils import make_executable
from main.FileUtils import read_lines
from main.FileUtils import write_lines
from main.FileUtils import file_exists
from main.Parser import Parser
from main.Scanner import Scanner
from main.Semantic import Semantic
from main.CodeGenerator import CodeGenerator
from main.CompilationError import CompilationError


def compile(code):
    tokenizer = Scanner(code)
    semantic = Semantic()
    code_generator = CodeGenerator()
    parser = Parser(tokenizer, semantic, code_generator)
    return parser.parse()


def build_program(input, output=None):
    if not file_exists(input):
        print('File ' + input + ' not found')
        return -1

    if not input or not input.lower().endswith('.pl0'):
        print('Wrong file extension, file ' + input + ' does not end with .pl0')
        return -2

    if not output:
        output = input[:-4]
    lines = read_lines(input)
    code = "".join(lines)

    try:
        result = compile(code)
        write_result(result, lines, output)
    except Exception as e:
        print("Error inesperado!")
        print(traceback.format_exc())


def write_result(result, lines, output=None):
    if result.success:

        write_bin(output, bytearray(result.bytes))
        make_executable(output)
    else:
        output_lines = []
        lines_code_written = 0
        char_code_written = 0
        for error in result.errors:
            while lines_code_written < error.token.lineno:
                output_lines += lines[lines_code_written]
                char_code_written += len(lines[lines_code_written])
                lines_code_written += 1
            error_pos = error.token.lexpos - (char_code_written - len(lines[lines_code_written - 1]))
            padding = len(lines[lines_code_written - 1]) - error_pos
            msg_line = spaces_padding(error_pos) + '^' + spaces_padding(padding) + build_error_msg(error) + '\n'
            output_lines += msg_line

        output_lines += lines[lines_code_written:]
        if output:
            write_lines(output + '.lst', output_lines)
        else:
            for l in output_lines:
                print(l)


def build_error_msg(error):
    msg =  'Error: ' + CompilationError.MSG_DICT[error.error_type]
    if error.token:
        if error.expected:
            msg += ' - Se esperaba ' + error.expected + ' y se encontró ' + error.token.value
        else:
            msg += ' - ' + error.token.value
    return msg


def spaces_padding(size):
    return '{message: <{fill}}'.format(message='', fill=size)


