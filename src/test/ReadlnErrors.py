import unittest

from main.CompilationError import CompilationError
from main.Compiler import compile

ok = '''
var X;
readln (X)
.
'''

miss_lparent = '''
var X;
begin
    write ('NUM=');
    readln X);
    writeln ('NUM=',X)
end.
'''

miss_rparent = '''
var X;
begin
    write ('NUM=');
    readln (X;
    writeln ('NUM=',X)
end.
'''

miss_parents = '''
var X;
begin
    write ('NUM=');
    readln X;
    writeln ('NUM=',X)
end.
'''

miss_semicolon = '''
var X;
begin
    write ('NUM=');
    readln (X)
    writeln ('NUM=',X)
end.
'''

miss_parents_and_semicolon = '''
var X;
begin
    write ('NUM=');
    readln X
    writeln ('NUM=',X)
end.
'''

miss_comma = '''
var X, Y;
begin
    write ('NUM=');
    readln (X Y);
    writeln ('NUM=',X)
end.
'''

const_assignment = '''
const X = 10;
begin
    write ('NUM=');
    readln (X);
    writeln ('NUM=',X)
end.
'''

procedure_assignment = '''
var X;

procedure Y;
    X:=2;

begin
    write ('NUM=');
    readln (Y);
    writeln ('NUM=',X)
end.
'''

undefined_var = '''
var X;
begin
    write ('NUM=');
    readln (Y);
    writeln ('NUM=',X)
end.
'''


class ReadlnErrors(unittest.TestCase):

    def test_ok(self):
        result = compile(ok)
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

    def test_miss_comma(self):
        result = compile(miss_comma)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('COMMA', result.errors[0].expected)

    def test_const_assignment(self):
        result = compile(const_assignment)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.ID_NOT_ASSIGNABLE, result.errors[0].error_type)

    def test_procedure_assignment(self):
        result = compile(procedure_assignment)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.ID_NOT_ASSIGNABLE, result.errors[0].error_type)

    def test_undefined_var(self):
        result = compile(undefined_var)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.ID_NOT_EXISTS, result.errors[0].error_type)


if __name__ == '__main__':
    unittest.main()
