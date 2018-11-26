import unittest
from main.Scanner import Scanner

OK_FOLDER = "../resources/bien"
FAIL_FOLDER = "../resources/mal"


class ExampleSourceFilesTest(unittest.TestCase):

    def test_integer_var_int_assign(self):
        tokenizer = Scanner("var mi_variable := 16")
        tokenizer.next()
        self.assertTrue(tokenizer.last_token.type == "var")
        tokenizer.next()
        self.assertTrue(tokenizer.last_token.type == "ID")
        tokenizer.next()
        self.assertTrue(tokenizer.last_token.type == "BECOMES")
        tokenizer.next()
        self.assertTrue(tokenizer.last_token.type == "NUMBER")

    def test_integer_var_str_assign(self):
        tokenizer = Scanner("var mi_variable := 'Hola Mundo' \"hey\"")
        tokenizer.next()
        self.assertTrue(tokenizer.last_token.type == "var")
        tokenizer.next()
        self.assertTrue(tokenizer.last_token.type == "ID")
        tokenizer.next()
        self.assertTrue(tokenizer.last_token.type == "BECOMES")
        tokenizer.next()
        self.assertTrue(tokenizer.last_token.type == "STRING")
        tokenizer.next()
        self.assertTrue(tokenizer.last_token.type == "STRING")
