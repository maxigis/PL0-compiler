import unittest
from os import listdir
from os.path import isfile, join
from main.Compiler import compile

OK_FOLDER = "../../resources/bien"
FAIL_FOLDER = "../../resources/mal"


class ExampleSourceFilesTest(unittest.TestCase):

    def test_file_00(self):
        file = open(join(OK_FOLDER, "BIEN-06.PL0"), "r")
        code = file.read()
        file.close()
        comp_result = compile(code)

        self.assertTrue(comp_result.success)

    def test_files_ok(self):
        files_ok = [join(OK_FOLDER, f) for f in listdir(OK_FOLDER) if isfile(join(OK_FOLDER, f))]
        for filename in files_ok:
            file = open(filename, "r")
            code = file.read()
            file.close()
            comp_result = compile(code)
            self.assertTrue(comp_result.success, "Error in file " + filename)

    def test_files_fail(self):
        files_ok = [join(FAIL_FOLDER, f) for f in listdir(FAIL_FOLDER) if isfile(join(FAIL_FOLDER, f))]
        for filename in files_ok:
            file = open(filename, "r")
            code = file.read()
            file.close()
            comp_result = compile(code)
            self.assertFalse(comp_result.success)

    def test_fail_six(self):
        file = open(join(FAIL_FOLDER, "MAL-04.PL0"), "r")
        code = file.read()
        file.close()
        comp_result = compile(code)
        self.assertFalse(comp_result.success)


if __name__ == '__main__':
    unittest.main()
