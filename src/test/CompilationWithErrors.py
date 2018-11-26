import unittest

from main.CompilationError import CompilationError
from main.Compiler import compile

eql_becomes = '''
var X, Y;

procedure INICIAR;
    const Y := 2;
    procedure ASIGNAR;
    X := Y;
    call ASIGNAR;

begin
    write ('NUM=');
    readln (Y);
    call INICIAR;
    writeln ('NUM*2=',Y*X)
end.
'''


class CompilationWithErrors(unittest.TestCase):

    def test_compare_generated_code(self):
        result = compile(eql_becomes)
        self.assertFalse(result.success)
        self.assertEquals(1, len(result.errors))
        self.assertEquals(CompilationError.EQL_BECOMES_MISMATCH, result.errors[0].error_type)


if __name__ == '__main__':
    unittest.main()
