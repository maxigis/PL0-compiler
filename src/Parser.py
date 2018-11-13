from ParseError import ParseError
from Utils import Utils
from CompilationResult import CompilationResult
import logging


class Parser(object):

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse_factor(self):
        logging.info('parse_factor')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type == 'LPAREN':
            tokenizer.next()
            self.parse_exp()
            if tokenizer.last_token.type != 'RPAREN':
                raise ParseError('RPAREN', tokenizer.last_token)
        elif tokenizer.last_token.type != 'ID' and tokenizer.last_token.type != 'NUMBER':
            raise ParseError('ID, NUMBER, LPAREN', tokenizer.last_token)
        tokenizer.next()

    def parse_termino(self):
        logging.info('parse_termino')
        seguir = True
        tokenizer = self.tokenizer
        while seguir:
            self.parse_factor()
            if tokenizer.last_token.type != 'TIMES' and tokenizer.last_token.type != 'SLASH':
                seguir = False
            else:
                tokenizer.next()

    def parse_cond(self):
        logging.info('parse_cond')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type == 'odd':
            tokenizer.next()
            self.parse_exp()
        else:
            self.parse_exp()
            if (tokenizer.last_token.type != 'EQL' and tokenizer.last_token.type != 'NEQ' and
                tokenizer.last_token.type != 'LSS' and tokenizer.last_token.type != 'LEQ' and
                    tokenizer.last_token.type != 'GTR' and tokenizer.last_token.type != 'GEQ'):

                raise ParseError('EQL,NEQ,LSS,LEQ,GTR,GEQ', tokenizer.last_token)
            tokenizer.next()
            self.parse_exp()

    def parse_exp(self):
        logging.info('parse_exp')
        tokenizer = self.tokenizer
        seguir = True
        while seguir:
            if tokenizer.last_token.type == 'PLUS' or tokenizer.last_token.type == 'MINUS':
                tokenizer.next()
            self.parse_termino()
            if tokenizer.last_token.type != 'PLUS' and tokenizer.last_token.type != 'MINUS':
                seguir = False

    def parse_prop(self, tabla):
        logging.info('parse_prop')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type == 'ID':
            if Utils.no_existe(tabla, tokenizer.last_token.value):
                raise ParseError("Undefined id", tokenizer.last_token)
            if tokenizer.next().type != 'BECOMES':
                raise ParseError('BECOMES', tokenizer.last_token)
            tokenizer.next()
            self.parse_exp()

        elif tokenizer.last_token.type == 'call':
            if tokenizer.next().type != 'ID':
                raise ParseError('ID', tokenizer.last_token)
            if Utils.no_existe(tabla, tokenizer.last_token.value):
                raise ParseError("Undefined id", tokenizer.last_token)
            tokenizer.next()

        elif tokenizer.last_token.type == 'begin':
            seguir = True
            tokenizer.next()
            while seguir:
                self.parse_prop(tabla)
                if tokenizer.last_token.type == 'end':
                    seguir = False
                elif tokenizer.last_token.type != 'SEMICOLON':
                    raise ParseError('end,SEMICOLON', tokenizer.last_token)
                tokenizer.next()

        elif tokenizer.last_token.type == 'if':
            tokenizer.next()
            self.parse_cond()
            if tokenizer.last_token.type != 'then':
                raise ParseError('then', tokenizer.last_token)
            tokenizer.next()
            self.parse_prop(tabla)

        elif tokenizer.last_token.type == 'while':
            tokenizer.next()
            self.parse_cond()
            if tokenizer.last_token.type != 'do':
                raise ParseError('do', tokenizer.last_token)
            tokenizer.next()
            self.parse_prop(tabla)

        elif tokenizer.last_token.type == 'readln':
            if tokenizer.next().type != 'LPAREN':
                raise ParseError('LPAREN', tokenizer.last_token)
            seguir = True
            while seguir:
                if tokenizer.next().type != 'ID':
                    raise ParseError('ID', tokenizer.last_token)
                if tokenizer.next().type == 'RPAREN':
                    seguir = False
                elif tokenizer.last_token.type != 'COMMA':
                    raise ParseError('RPAREN,COMMA', tokenizer.last_token)
            tokenizer.next()

        elif tokenizer.last_token.type == 'write' or tokenizer.last_token.type == 'writeln':
            is_writeln = tokenizer.last_token.type == 'writeln'
            if tokenizer.next().type != 'LPAREN':
                if is_writeln:
                    return
                else:
                    raise ParseError('LPAREN', tokenizer.last_token)
            seguir = True
            while seguir:
                if tokenizer.next().type != 'STRING':
                    self.parse_exp()
                else:
                    tokenizer.next()
                if tokenizer.last_token.type == 'RPAREN':
                    seguir = False
                elif tokenizer.last_token.type != 'COMMA':
                    raise ParseError('RPAREN,COMMA', tokenizer.last_token)
            tokenizer.next()

    def parse_bloque(self, tabla, base):
        logging.info('parse_bloque')
        desp = 0
        tokenizer = self.tokenizer
        token = tokenizer.last_token
        if token.type == 'const':
            seguir = True
            while seguir:
                if tokenizer.next().type != 'ID':
                    raise ParseError('ID', tokenizer.last_token)
                if Utils.existe(tabla, tokenizer.last_token.value, base, desp):
                    raise ParseError("Id already defined", tokenizer.last_token)
                const_id = tokenizer.last_token.value
                if tokenizer.next().type != 'EQL':
                    raise ParseError('EQL', tokenizer.last_token)
                if tokenizer.next().type != 'NUMBER':
                    raise ParseError('NUMBER', tokenizer.last_token)

                tabla.append(("const", const_id, tokenizer.last_token.value))
                desp = desp + 1

                token = tokenizer.next()
                if token.type == 'SEMICOLON':
                    seguir = False
                elif token.type != 'COMMA':
                    raise ParseError('SEMICOLON, COMMA', tokenizer.last_token)
            token = tokenizer.next()

        if token.type == 'var':
            seguir = True
            while seguir:
                if tokenizer.next().type != 'ID':
                    raise ParseError('ID', tokenizer.last_token)
                if Utils.existe(tabla, tokenizer.last_token.value, base, desp):
                    raise ParseError("Id already defined", tokenizer.last_token)

                tabla.append(("var", tokenizer.last_token.value, 0))
                desp = desp + 1

                token = tokenizer.next()
                if token.type == 'SEMICOLON':
                    seguir = False
                elif token.type != 'COMMA':
                    raise ParseError('SEMICOLON, COMMA', tokenizer.last_token)
            token = tokenizer.next()

        procedure = token.type == 'procedure'
        while procedure:
            if tokenizer.next().type != 'ID':
                raise ParseError('ID', tokenizer.last_token)
            if Utils.existe(tabla, tokenizer.last_token.value, base, desp):
                raise ParseError("Id already defined", tokenizer.last_token)

            tabla.append(("procedure", tokenizer.last_token.value, 0))
            desp = desp + 1

            if tokenizer.next().type != 'SEMICOLON':
                raise ParseError('SEMICOLON', tokenizer.last_token)
            tokenizer.next()
            self.parse_bloque(tabla, base + desp)
            if tokenizer.last_token.type != 'SEMICOLON':
                raise ParseError('SEMICOLON', tokenizer.last_token)
            token = tokenizer.next()
            procedure = token.type == 'procedure'

        self.parse_prop(tabla)

    def parse(self):
        try:
            logging.info('Starting parse')
            self.tokenizer.next()
            self.parse_bloque([], 0)
            if self.tokenizer.last_token.type != 'PERIOD':
                raise ParseError('PERIOD', self.tokenizer.last_token)
            logging.info('Parsing finished')
            return CompilationResult()
        except Exception as e:
            logging.info('Error!')
            return CompilationResult([e])
