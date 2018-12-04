import unittest
from main.Compiler import compile
from main.CompilationError import CompilationError


term_incomplete = '''
const X = 3;
IF X* <> X THEN WRITE (X, '..')
'''

int_too_large = '''
var X;

begin
  X := 100000000000000000;
  writeln(X)
end.
'''

int_limit_ok = '''
var X;

begin
  X := 4294967295;
  writeln(X)
end.
'''


class FactorTest(unittest.TestCase):

    def test_term_incomplete(self):
        result = compile(term_incomplete)
        self.assertFalse(result.success)

    def test_int_limit_ok(self):
        result = compile(int_limit_ok)
        self.assertTrue(result.success)

    def test_int_too_large(self):
        result = compile(int_too_large)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.INT_TOO_LARGE, result.errors[0].error_type)


if __name__ == '__main__':
    unittest.main()
