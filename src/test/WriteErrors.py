import unittest

from main.CompilationError import CompilationError
from main.Compiler import compile

write_ok = '''
var X;
begin
    write ('NUM=')
end.
'''

writeln_ok = '''
var X;
begin
    writeln('NUM=');
    X := 10
end.
'''

writeln_only_ok = '''
var X;
begin
    writeln;
    X := 10
end.
'''

miss_lparent = '''
var X;
begin
    write 'NUM=');
    X := 10
end.
'''

miss_rparent = '''
var X;
begin
    write ('NUM=';
    X := 10
end.
'''

miss_parents = '''
var X;
begin
    write 'NUM=';
    X := 10
end.
'''

miss_semicolon = '''
var X;
begin
    write ('NUM=')
    X := 10
end.
'''

miss_parents_and_semicolon = '''
var X;
begin
    write 'NUM='
    X := 10
end.
'''


class ReadlnErrors(unittest.TestCase):

    def test_ok(self):
        result = compile(write_ok)
        self.assertTrue(result.success)
        self.assertEqual(None, result.errors)
        result = compile(writeln_ok)
        self.assertTrue(result.success)
        self.assertEqual(None, result.errors)
        result = compile(writeln_only_ok)
        self.assertTrue(result.success)
        self.assertEqual(None, result.errors)

    def test_miss_lparent(self):
        result = compile(miss_lparent)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('LPAREN', result.errors[0].expected)

    def test_miss_rparent(self):
        result = compile(miss_rparent)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('RPAREN', result.errors[0].expected)

    def test_miss_parents(self):
        result = compile(miss_parents)
        self.assertFalse(result.success)
        self.assertEqual(2, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('LPAREN', result.errors[0].expected)
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[1].error_type)
        self.assertEqual('RPAREN', result.errors[1].expected)

    def miss_semicolon(self):
        result = compile(miss_semicolon)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('SEMICOLON', result.errors[0].expected)

    def test_miss_parents_and_semicolon(self):
        result = compile(miss_parents_and_semicolon)
        self.assertFalse(result.success)
        self.assertEqual(3, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('LPAREN', result.errors[0].expected)
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[1].error_type)
        self.assertEqual('RPAREN', result.errors[1].expected)
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[2].error_type)
        self.assertEqual('SEMICOLON', result.errors[2].expected)


if __name__ == '__main__':
    unittest.main()
