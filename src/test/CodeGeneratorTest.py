import unittest
from main.CodeGenerator import CodeGenerator


class CodeGeneratorTest(unittest.TestCase):

    def test_calc_jump(self):
        expected = [238, 255, 255, 255]
        actual = CodeGenerator._calc_jump(1167, 1185)

        self.assertTrue(len(expected) == len(actual))
        self.assertTrue(expected[0] == actual[0])
        self.assertTrue(expected[1] == actual[1])
        self.assertTrue(expected[2] == actual[2])
        self.assertTrue(expected[3] == actual[3])



if __name__ == '__main__':
    unittest.main()
