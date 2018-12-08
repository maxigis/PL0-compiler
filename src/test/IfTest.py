import unittest
from main.Compiler import compile


if_ok = '''
var X;
begin
    readln(X);
    IF X > 5 THEN WRITE (X, '..')
end.
'''


class IfTest(unittest.TestCase):

    def test_if_ok(self):
        result = compile(if_ok)
        self.assertTrue(result.success)


if __name__ == '__main__':
    unittest.main()
