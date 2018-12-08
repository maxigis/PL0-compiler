import unittest

from main.CompilationError import CompilationError
from main.Compiler import compile

ok = '''
const Y = 2;
var X;
.
'''

scope_ok = '''
const Y = 2;
var X;
procedure TEST;
    const Y = 3;
    X := Y;
    
CALL TEST
.
'''

const_eql_becomes = '''
const Y := 2;
var X;
.
'''

const_miss_value = '''
const Y = ;
var X;
.
'''

const_miss_eql = '''
const Y 3;
var X;
.
'''

const_miss_all = '''
const Y
var X;
.
'''

already_defined = '''
const Y = 1, Y = 0;
.
'''


class ConstErrors(unittest.TestCase):

    def test_ok(self):
        result = compile(ok)
        self.assertTrue(result.success)

    def test_scope_ok(self):
        result = compile(scope_ok)
        self.assertTrue(result.success)

    def test_const_eql_becomes(self):
        result = compile(const_eql_becomes)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.BECOMES_EQL_MISMATCH, result.errors[0].error_type)

    def test_const_miss_value(self):
        result = compile(const_miss_value)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('NUMBER', result.errors[0].expected)

    def test_const_miss_eql(self):
        result = compile(const_miss_eql)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.MISSING_TOKEN, result.errors[0].error_type)
        self.assertEqual('EQL', result.errors[0].expected)

    def test_const_miss_all(self):
        result = compile(const_miss_all)
        self.assertFalse(result.success)
        self.assertEqual(3, len(result.errors))
        self.assertEqual(CompilationError.INVALID_TOKEN, result.errors[0].error_type)
        self.assertEqual('EQL', result.errors[0].expected)
        self.assertEqual('NUMBER', result.errors[1].expected)
        self.assertEqual('SEMICOLON', result.errors[2].expected)

    def test_already_defined(self):
        result = compile(already_defined)
        self.assertFalse(result.success)
        self.assertEqual(1, len(result.errors))
        self.assertEqual(CompilationError.ID_ALREADY_DEFINED, result.errors[0].error_type)


if __name__ == '__main__':
    unittest.main()
