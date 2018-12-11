import unittest
from main.CodeGenerator import CodeGenerator


class CodeGeneratorTest(unittest.TestCase):

    def test_fix_block_jmp_none(self):
        code_gen = CodeGenerator()
        base = code_gen.len()
        code_gen.block_jmp()
        self.assertEqual(code_gen.len(), base + 5)
        code_gen.fix_block_jmp()
        self.assertEqual(code_gen.len(), base)

    def test_fix_block_jmp(self):
        code_gen = CodeGenerator()
        base = code_gen.len()
        code_gen.block_jmp()
        for i in range(10):
            code_gen.buffer.append([0x0])
        code_gen.fix_block_jmp()
        expected = [0xE9, 0x0A, 0x0, 0x0, 0x0]
        for index, byte in enumerate(expected):
            self.assertEqual(code_gen.buffer[base + index], byte)

    def test_fix_block_code_reference(self):
        code_gen = CodeGenerator()
        base = code_gen.len()
        code_gen.block_jmp()
        code_gen.block_jmp()
        code_gen.block_jmp()
        code_gen.fix_block_jmp()

        code_gen.buffer.extend([0xB8, 0x02, 0x00, 0x00, 0x00])
        code_gen.buffer.extend([0x89, 0x87, 0x00, 0x00, 0x00, 0x00])
        code_gen.buffer.extend([0xC3])
        code_gen.fix_block_jmp()

        code_gen.buffer.extend([0xE8, 0xEF, 0xFF, 0xFF, 0xFF])
        code_gen.buffer.extend([0xC3])
        code_gen.fix_block_jmp()

        expected = [0xE9, 0x17, 0x00, 0x00, 0x00, 0xE9, 0x0C, 0x00, 0x00, 0x00]
        for index, byte in enumerate(expected):
            self.assertEqual(code_gen.buffer[base + index], byte)

    def test_readln(self):
        code_gen = CodeGenerator()
        base = code_gen.len()
        code_gen.readln(4)
        expected = [0xE8, 0x86, 0xFE, 0xFF, 0xFF, 0x89, 0x87, 0x10, 0x00, 0x00, 0x00]
        self.assertEquals(len(code_gen.buffer[base:]), len(expected))
        for index, byte in enumerate(expected):
            self.assertEqual(code_gen.buffer[base + index], byte)

    def test_writeln_string(self):
        code_gen = CodeGenerator()
        base = code_gen.len()
        code_gen.write_string('hola mundo hola mundo!')
        expected = [0xB9, 0x99, 0x84, 0x04, 0x08,   # Ubicacion de la cadena: 1157 + 20 + 134512640 = 08 04 84 99
                    0xBA, 0x16, 0x00, 0x00, 0x00,   # Longitud de la cadena
                    0xE8, 0xDC, 0xFC, 0xFF, 0xFF,   # Llamado para mostrar la cadena: 368 - 1172
                    0xE9, 0x16, 0x00, 0x00, 0x00]   # Salto incondicional
        expected.extend([0x68, 0x6F, 0x6C, 0x61, 0x20, 0x6D, 0x75, 0x6E, 0x64, 0x6F, 0x20,
                         0x68, 0x6F, 0x6C, 0x61, 0x20, 0x6D, 0x75, 0x6E, 0x64, 0x6F, 0x21])
        self.assertEquals(len(code_gen.buffer[base:]), len(expected))
        for index, byte in enumerate(expected):
            self.assertEqual(code_gen.buffer[base + index], byte)

    def test_writeln_exp_num(self):
        code_gen = CodeGenerator()
        base = code_gen.len()
        code_gen.write_exp()
        expected = [0x58, 0xE8, 0x05, 0xFD, 0xFF, 0xFF]
        self.assertEquals(len(code_gen.buffer[base:]), len(expected))
        for index, byte in enumerate(expected):
            self.assertEqual(code_gen.buffer[base + index], byte)

    def test_writeln_empty(self):
        code_gen = CodeGenerator()
        base = code_gen.len()
        code_gen.writeln()
        expected = [0xe8, 0xf6, 0xfc, 0xff, 0xff]
        self.assertEquals(len(code_gen.buffer[base:]), len(expected))
        for index, byte in enumerate(expected):
            self.assertEqual(code_gen.buffer[base + index], byte)


if __name__ == '__main__':
    unittest.main()
