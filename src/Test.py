import unittest
from Utils import Utils


class Test(unittest.TestCase):

    def test_existe_si(self):
        self.assertTrue(Utils.existe([('CONST', 'var1', 0), ('CONST', 'var2', 4), ('CONST', 'var3', 8), ('CONST', 'var4', 12)], 'var3', 2, 2))

    def test_existe_no(self):
        self.assertFalse(Utils.existe([('CONST', 'var1', 0), ('CONST', 'var2', 4), ('CONST', 'var3', 8), ('CONST', 'var4', 12)], 'var1', 2, 2))

    def test_no_existe_true(self):
        self.assertTrue(Utils.no_existe([('CONST', 'var1', 0), ('CONST', 'var2', 4), ('CONST', 'var3', 8), ('CONST', 'var4', 12)], 'var10'))

    def test_no_existe_false(self):
        self.assertFalse(Utils.no_existe([('CONST', 'var1', 0), ('CONST', 'var2', 4), ('CONST', 'var3', 8), ('CONST', 'var4', 12)], 'var1'))


if __name__ == '__main__':
    unittest.main()