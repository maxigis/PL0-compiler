import unittest

from main.CompilationError import CompilationError
from main.Compiler import compile

ok = '''
var X,Y, Z;
begin
    write ('NUM=');
    readln (Y);
    writeln ('NUM=',Y)
end.
'''

scope_ok = '''
const Y = 2;
var X;
procedure TEST;
    var X;
    X := Y;
    
CALL TEST
.
'''

missing_semicolon = '''
var Y
begin
    write ('NUM=');
    readln (Y);
    writeln ('NUM=',Y)
end.
'''

missing_comma = '''
var Y X Z;
begin
    write ('NUM=');
    readln (Y);
    writeln ('NUM*2=',Y*X)
end.
'''

missing_semicolon_and_comma = '''
var Y X Z
begin
    write ('NUM=');
    readln (Y);
    writeln ('NUM*2=',Y*X)
end.
'''

miss_all = '''
var 
begin
    write ('HELLO ');
    writeln ('WORLD');
end.
'''

already_defined = '''
var X, Y, X;
.
'''


class VarErrors(unittest.TestCase):

    def test_ok(self):
        result = compile(ok)
        self.assertTrue(result.success)

    def test_scope_ok(self):
        result = compile(scope_ok)
        self.assertTrue(result.success)

    def test_missing_semicolon(self):
        result = compile(missing_semicolon)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('SEMICOLON', result.errors[0].expected)

    def test_missing_comma(self):
        result = compile(missing_comma)
        self.assertFalse(result.success)
        self.assertEqual(2, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[1].error_type)
        self.assertEqual('COMMA', result.errors[0].expected)
        self.assertEqual('COMMA', result.errors[1].expected)

    def test_missing_semicolon_and_comma(self):
        result = compile(missing_semicolon_and_comma)
        self.assertFalse(result.success)
        self.assertEqual(3, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[1].error_type)
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[2].error_type)
        self.assertEqual('COMMA', result.errors[0].expected)
        self.assertEqual('COMMA', result.errors[1].expected)
        self.assertEqual('SEMICOLON', result.errors[2].expected)

    def test_miss_all(self):
        result = compile(miss_all)
        self.assertFalse(result.success)
        self.assertEqual(2, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('ID', result.errors[0].expected)
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[1].error_type)
        self.assertEqual('SEMICOLON', result.errors[1].expected)

    def test_already_defined(self):
        result = compile(already_defined)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.ID_ALREADY_DEFINED, result.errors[0].error_type)


if __name__ == '__main__':
    unittest.main()
