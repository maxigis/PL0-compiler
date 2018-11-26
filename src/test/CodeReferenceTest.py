import unittest
from main.Compiler import compile

EXPECTED = [0x7f, 0x45, 0x4c, 0x46, 0x1, 0x1, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x2, 0x0, 0x3, 0x0, 0x1, 0x0, 0x0, 0x0, 0x80, 0x84, 0x4, 0x8, 0x34, 0x0, 0x0, 0x0, 0x65, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x34, 0x0, 0x20, 0x0, 0x1, 0x0, 0x28, 0x0, 0x3, 0x0, 0x1, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x80, 0x4, 0x8, 0x0, 0x80, 0x4, 0x8, 0x0a, 0x5, 0x0, 0x0, 0x0a, 0x5, 0x0, 0x0, 0x7, 0x0, 0x0, 0x0, 0x0, 0x10, 0x0, 0x0, 0x0, 0x2e, 0x73, 0x68, 0x73, 0x74, 0x72, 0x74, 0x61, 0x62, 0x0, 0x2e, 0x74, 0x65, 0x78, 0x74, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x3, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x54, 0x0, 0x0, 0x0, 0x11, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0b, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x6, 0x0, 0x0, 0x0, 0xe0, 0x80, 0x4, 0x8, 0xe0, 0x0, 0x0, 0x0, 0x2a, 0x4, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x52, 0x51, 0x53, 0x50, 0xb8, 0x4, 0x0, 0x0, 0x0, 0xbb, 0x1, 0x0, 0x0, 0x0, 0x89, 0xe1, 0xba, 0x1, 0x0, 0x0, 0x0, 0xcd, 0x80, 0x58, 0x5b, 0x59, 0x5a, 0xc3, 0x55, 0x89, 0xe5, 0x81, 0xec, 0x24, 0x0, 0x0, 0x0, 0x52, 0x51, 0x53, 0xb8, 0x36, 0x0, 0x0, 0x0, 0xbb, 0x0, 0x0, 0x0, 0x0, 0xb9, 0x1, 0x54, 0x0, 0x0, 0x8d, 0x55, 0xdc, 0xcd, 0x80, 0x81, 0x65, 0xe8, 0xf5, 0xff, 0xff, 0xff, 0xb8, 0x36, 0x0, 0x0, 0x0, 0xbb, 0x0, 0x0, 0x0, 0x0, 0xb9, 0x2, 0x54, 0x0, 0x0, 0x8d, 0x55, 0xdc, 0xcd, 0x80, 0x31, 0xc0, 0x50, 0xb8, 0x3, 0x0, 0x0, 0x0, 0xbb, 0x0, 0x0, 0x0, 0x0, 0x89, 0xe1, 0xba, 0x1, 0x0, 0x0, 0x0, 0xcd, 0x80, 0x81, 0x4d, 0xe8, 0x0a, 0x0, 0x0, 0x0, 0xb8, 0x36, 0x0, 0x0, 0x0, 0xbb, 0x0, 0x0, 0x0, 0x0, 0xb9, 0x2, 0x54, 0x0, 0x0, 0x8d, 0x55, 0xdc, 0xcd, 0x80, 0x58, 0x5b, 0x59, 0x5a, 0x89, 0xec, 0x5d, 0xc3, 0xb8, 0x4, 0x0, 0x0, 0x0, 0xbb, 0x1, 0x0, 0x0, 0x0, 0xcd, 0x80, 0xc3, 0x90, 0x90, 0x90, 0xb0, 0x0a, 0xe8, 0x59, 0xff, 0xff, 0xff, 0xc3, 0x4, 0x30, 0xe8, 0x51, 0xff, 0xff, 0xff, 0xc3, 0x3d, 0x0, 0x0, 0x0, 0x80, 0x75, 0x4e, 0xb0, 0x2d, 0xe8, 0x42, 0xff, 0xff, 0xff, 0xb0, 0x2, 0xe8, 0xe3, 0xff, 0xff, 0xff, 0xb0, 0x1, 0xe8, 0xdc, 0xff, 0xff, 0xff, 0xb0, 0x4, 0xe8, 0xd5, 0xff, 0xff, 0xff, 0xb0, 0x7, 0xe8, 0xce, 0xff, 0xff, 0xff, 0xb0, 0x4, 0xe8, 0xc7, 0xff, 0xff, 0xff, 0xb0, 0x8, 0xe8, 0xc0, 0xff, 0xff, 0xff, 0xb0, 0x3, 0xe8, 0xb9, 0xff, 0xff, 0xff, 0xb0, 0x6, 0xe8, 0xb2, 0xff, 0xff, 0xff, 0xb0, 0x4, 0xe8, 0xab, 0xff, 0xff, 0xff, 0xb0, 0x8, 0xe8, 0xa4, 0xff, 0xff, 0xff, 0xc3, 0x3d, 0x0, 0x0, 0x0, 0x0, 0x7d, 0x0b, 0x50, 0xb0, 0x2d, 0xe8, 0xec, 0xfe, 0xff, 0xff, 0x58, 0xf7, 0xd8, 0x3d, 0x0a, 0x0, 0x0, 0x0, 0x0f, 0x8c, 0xef, 0x0, 0x0, 0x0, 0x3d, 0x64, 0x0, 0x0, 0x0, 0x0f, 0x8c, 0xd1, 0x0, 0x0, 0x0, 0x3d, 0xe8, 0x3, 0x0, 0x0, 0x0f, 0x8c, 0xb3, 0x0, 0x0, 0x0, 0x3d, 0x10, 0x27, 0x0, 0x0, 0x0f, 0x8c, 0x95, 0x0, 0x0, 0x0, 0x3d, 0xa0, 0x86, 0x1, 0x0, 0x7c, 0x7b, 0x3d, 0x40, 0x42, 0x0f, 0x0, 0x7c, 0x61, 0x3d, 0x80, 0x96, 0x98, 0x0, 0x7c, 0x47, 0x3d, 0x0, 0xe1, 0xf5, 0x5, 0x7c, 0x2d, 0x3d, 0x0, 0xca, 0x9a, 0x3b, 0x7c, 0x13, 0xba, 0x0, 0x0, 0x0, 0x0, 0xbb, 0x0, 0xca, 0x9a, 0x3b, 0xf7, 0xfb, 0x52, 0xe8, 0x30, 0xff, 0xff, 0xff, 0x58, 0xba, 0x0, 0x0, 0x0, 0x0, 0xbb, 0x0, 0xe1, 0xf5, 0x5, 0xf7, 0xfb, 0x52, 0xe8, 0x1d, 0xff, 0xff, 0xff, 0x58, 0xba, 0x0, 0x0, 0x0, 0x0, 0xbb, 0x80, 0x96, 0x98, 0x0, 0xf7, 0xfb, 0x52, 0xe8, 0x0a, 0xff, 0xff, 0xff, 0x58, 0xba, 0x0, 0x0, 0x0, 0x0, 0xbb, 0x40, 0x42, 0x0f, 0x0, 0xf7, 0xfb, 0x52, 0xe8, 0xf7, 0xfe, 0xff, 0xff, 0x58, 0xba, 0x0, 0x0, 0x0, 0x0, 0xbb, 0xa0, 0x86, 0x1, 0x0, 0xf7, 0xfb, 0x52, 0xe8, 0xe4, 0xfe, 0xff, 0xff, 0x58, 0xba, 0x0, 0x0, 0x0, 0x0, 0xbb, 0x10, 0x27, 0x0, 0x0, 0xf7, 0xfb, 0x52, 0xe8, 0xd1, 0xfe, 0xff, 0xff, 0x58, 0xba, 0x0, 0x0, 0x0, 0x0, 0xbb, 0xe8, 0x3, 0x0, 0x0, 0xf7, 0xfb, 0x52, 0xe8, 0xbe, 0xfe, 0xff, 0xff, 0x58, 0xba, 0x0, 0x0, 0x0, 0x0, 0xbb, 0x64, 0x0, 0x0, 0x0, 0xf7, 0xfb, 0x52, 0xe8, 0xab, 0xfe, 0xff, 0xff, 0x58, 0xba, 0x0, 0x0, 0x0, 0x0, 0xbb, 0x0a, 0x0, 0x0, 0x0, 0xf7, 0xfb, 0x52, 0xe8, 0x98, 0xfe, 0xff, 0xff, 0x58, 0xe8, 0x92, 0xfe, 0xff, 0xff, 0xc3, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0xb8, 0x1, 0x0, 0x0, 0x0, 0xbb, 0x0, 0x0, 0x0, 0x0, 0xcd, 0x80, 0x90, 0x90, 0x90, 0x90, 0xb9, 0x0, 0x0, 0x0, 0x0, 0xb3, 0x3, 0x51, 0x53, 0xe8, 0xde, 0xfd, 0xff, 0xff, 0x5b, 0x59, 0x3c, 0x0a, 0x0f, 0x84, 0x34, 0x1, 0x0, 0x0, 0x3c, 0x7f, 0x0f, 0x84, 0x94, 0x0, 0x0, 0x0, 0x3c, 0x2d, 0x0f, 0x84, 0x9, 0x1, 0x0, 0x0, 0x3c, 0x30, 0x7c, 0xdb, 0x3c, 0x39, 0x7f, 0xd7, 0x2c, 0x30, 0x80, 0xfb, 0x0, 0x74, 0xd0, 0x80, 0xfb, 0x2, 0x75, 0x0c, 0x81, 0xf9, 0x0, 0x0, 0x0, 0x0, 0x75, 0x4, 0x3c, 0x0, 0x74, 0xbf, 0x80, 0xfb, 0x3, 0x75, 0x0a, 0x3c, 0x0, 0x75, 0x4, 0xb3, 0x0, 0xeb, 0x2, 0xb3, 0x1, 0x81, 0xf9, 0xcc, 0xcc, 0xcc, 0x0c, 0x7f, 0xa8, 0x81, 0xf9, 0x34, 0x33, 0x33, 0xf3, 0x7c, 0xa0, 0x88, 0xc7, 0xb8, 0x0a, 0x0, 0x0, 0x0, 0xf7, 0xe9, 0x3d, 0x8, 0x0, 0x0, 0x80, 0x74, 0x11, 0x3d, 0xf8, 0xff, 0xff, 0x7f, 0x75, 0x13, 0x80, 0xff, 0x7, 0x7e, 0x0e, 0xe9, 0x7f, 0xff, 0xff, 0xff, 0x80, 0xff, 0x8, 0x0f, 0x8f, 0x76, 0xff, 0xff, 0xff, 0xb9, 0x0, 0x0, 0x0, 0x0, 0x88, 0xf9, 0x80, 0xfb, 0x2, 0x74, 0x4, 0x1, 0xc1, 0xeb, 0x3, 0x29, 0xc8, 0x91, 0x88, 0xf8, 0x51, 0x53, 0xe8, 0xcb, 0xfd, 0xff, 0xff, 0x5b, 0x59, 0xe9, 0x53, 0xff, 0xff, 0xff, 0x80, 0xfb, 0x3, 0x0f, 0x84, 0x4a, 0xff, 0xff, 0xff, 0x51, 0x53, 0xb0, 0x8, 0xe8, 0x0a, 0xfd, 0xff, 0xff, 0xb0, 0x20, 0xe8, 0x3, 0xfd, 0xff, 0xff, 0xb0, 0x8, 0xe8, 0xfc, 0xfc, 0xff, 0xff, 0x5b, 0x59, 0x80, 0xfb, 0x0, 0x75, 0x7, 0xb3, 0x3, 0xe9, 0x25, 0xff, 0xff, 0xff, 0x80, 0xfb, 0x2, 0x75, 0x0f, 0x81, 0xf9, 0x0, 0x0, 0x0, 0x0, 0x75, 0x7, 0xb3, 0x3, 0xe9, 0x11, 0xff, 0xff, 0xff, 0x89, 0xc8, 0xb9, 0x0a, 0x0, 0x0, 0x0, 0xba, 0x0, 0x0, 0x0, 0x0, 0x3d, 0x0, 0x0, 0x0, 0x0, 0x7d, 0x8, 0xf7, 0xd8, 0xf7, 0xf9, 0xf7, 0xd8, 0xeb, 0x2, 0xf7, 0xf9, 0x89, 0xc1, 0x81, 0xf9, 0x0, 0x0, 0x0, 0x0, 0x0f, 0x85, 0xe6, 0xfe, 0xff, 0xff, 0x80, 0xfb, 0x2, 0x0f, 0x84, 0xdd, 0xfe, 0xff, 0xff, 0xb3, 0x3, 0xe9, 0xd6, 0xfe, 0xff, 0xff, 0x80, 0xfb, 0x3, 0x0f, 0x85, 0xcd, 0xfe, 0xff, 0xff, 0xb0, 0x2d, 0x51, 0x53, 0xe8, 0x8d, 0xfc, 0xff, 0xff, 0x5b, 0x59, 0xb3, 0x2, 0xe9, 0xbb, 0xfe, 0xff, 0xff, 0x80, 0xfb, 0x3, 0x0f, 0x84, 0xb2, 0xfe, 0xff, 0xff, 0x80, 0xfb, 0x2, 0x75, 0x0c, 0x81, 0xf9, 0x0, 0x0, 0x0, 0x0, 0x0f, 0x84, 0xa1, 0xfe, 0xff, 0xff, 0x51, 0xe8, 0x4, 0xfd, 0xff, 0xff, 0x59, 0x89, 0xc8, 0xc3, 0xbf, 0x2, 0x85, 0x4, 0x8, 0xe9, 0x17, 0x0, 0x0, 0x0, 0xe9, 0x0c, 0x0, 0x0, 0x0, 0xb8, 0x2, 0x0, 0x0, 0x0, 0x89, 0x87, 0x0, 0x0, 0x0, 0x0, 0xc3, 0xe8, 0xef, 0xff, 0xff, 0xff, 0xc3, 0xb9, 0xb5, 0x84, 0x4, 0x8, 0xba, 0x4, 0x0, 0x0, 0x0, 0xe8, 0xc0, 0xfc, 0xff, 0xff, 0xe9, 0x4, 0x0, 0x0, 0x0, 0x4e, 0x55, 0x4d, 0x3d, 0xe8, 0x52, 0xfe, 0xff, 0xff, 0x89, 0x87, 0x4, 0x0, 0x0, 0x0, 0xe8, 0xc1, 0xff, 0xff, 0xff, 0xb9, 0xdd, 0x84, 0x4, 0x8, 0xba, 0x6, 0x0, 0x0, 0x0, 0xe8, 0x98, 0xfc, 0xff, 0xff, 0xe9, 0x6, 0x0, 0x0, 0x0, 0x4e, 0x55, 0x4d, 0x2a, 0x32, 0x3d, 0x8b, 0x87, 0x4, 0x0, 0x0, 0x0, 0x50, 0x8b, 0x87, 0x0, 0x0, 0x0, 0x0, 0x5b, 0xf7, 0xeb, 0xe8, 0x98, 0xfc, 0xff, 0xff, 0xe8, 0x83, 0xfc, 0xff, 0xff, 0xe9, 0xfe, 0xfd, 0xff, 0xff, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
code = '''
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


class CodeReferenceTest(unittest.TestCase):

    def test_compare_generated_code(self):
        result = compile(code)
        binary = result.bytes
        self.assertEqual(len(EXPECTED), len(binary), "Binary size don't match! ")
        errors = []
        msg = " ".join([str(b) for b in binary])
        exp = " ".join([str(b) for b in EXPECTED])
        for index, byte in enumerate(binary):
            msg += str(byte) + " "
            if index == len(EXPECTED):
                break
            if EXPECTED[index] != byte:
                errors.append("Value mismatch: expected " + str(EXPECTED[index]) + " found " + str(byte))
        print(msg)
        print(exp)
        self.assertFalse(errors, '\n'.join(errors))


if __name__ == '__main__':
    unittest.main()
