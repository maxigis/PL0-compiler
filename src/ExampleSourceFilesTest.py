import unittest
from os import listdir
from os.path import isfile, join
from Parser import Parser
from Scanner import Scanner

OK_FOLDER = "../resources/bien"
FAIL_FOLDER = "../resources/mal"


class ExampleSourceFilesTest(unittest.TestCase):

    def test_file_00(self):
        file = open(join(OK_FOLDER, "BIEN-05.PL0"), "r")
        data = file.read()
        file.close()
        tokenizer = Scanner(data)
        parser = Parser(tokenizer)
        comp_result = parser.parse()

        self.assertTrue(comp_result)
        self.assertFalse(comp_result.errors)

    def test_files_ok(self):
        files_ok = [join(OK_FOLDER, f) for f in listdir(OK_FOLDER) if isfile(join(OK_FOLDER, f))]
        for filename in files_ok:
            file = open(filename, "r")
            data = file.read()
            file.close()
            tokenizer = Scanner(data)
            parser = Parser(tokenizer)
            comp_result = parser.parse()

            self.assertTrue(comp_result)
            self.assertFalse(comp_result.errors, filename)

    def test_files_fail(self):
        files_ok = [join(FAIL_FOLDER, f) for f in listdir(FAIL_FOLDER) if isfile(join(FAIL_FOLDER, f))]
        for filename in files_ok:
            file = open(filename, "r")
            data = file.read()
            file.close()
            tokenizer = Scanner(data)
            parser = Parser(tokenizer)
            comp_result = parser.parse()

            self.assertTrue(comp_result)
            self.assertTrue(comp_result.errors, filename)


if __name__ == '__main__':
    unittest.main()