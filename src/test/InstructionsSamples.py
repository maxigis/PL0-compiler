import unittest
from os import listdir
from os.path import isfile, join
from main.Compiler import compile
from main.FileUtils import read_binary
from main.FileUtils import read_lines


FOLDER = "../../resources/codegen/"


class ConstErrors(unittest.TestCase):

    def test_one(self):
        source_filename = FOLDER + 'while.pl0'
        compiled_filename = source_filename.replace('.pl0', '')
        bytecode = read_binary(compiled_filename)
        lines = read_lines(source_filename)
        code = "".join(lines)
        comp_result = compile(code)
        self.assertTrue(comp_result.success)

        for index, byte in enumerate(bytecode):
            self.assertEqual(byte, comp_result.bytes[index], 'Failed byte number ' + str(index))

    def test_all(self):
        source_files = [join(FOLDER, f) for f in listdir(FOLDER) if isfile(join(FOLDER, f)) and f.endswith('.pl0')]
        for source_filename in source_files:
            compiled_filename = source_filename.replace('.pl0', '')
            bytecode = read_binary(compiled_filename)

            lines = read_lines(source_filename)
            code = "".join(lines)
            comp_result = compile(code)
            self.assertTrue(comp_result.success)
            for index, byte in enumerate(bytecode):
                self.assertEqual(byte, comp_result.bytes[index], source_filename + ': Failed byte number ' + str(index))


if __name__ == '__main__':
    unittest.main()
