from main.CompilationResult import CompilationResult
from main.CompilationError import CompilationError
from main.Scanner import Scanner
import logging


class Parser(object):

    def __init__(self, tokenizer, semantic, generator):
        self.logger = logging.getLogger('Parser')
        self.errors = []
        self._tokenizer = tokenizer
        self._semantic = semantic
        self._code_gen = generator

    def parse(self):
        self.logger.info('Starting parse')
        try:
            self.tokenizer.next()
            self._parse_block()
            if self.tokenizer.last_token.type != 'PERIOD':
                self._add_error(CompilationError(CompilationError.INVALID_TOKEN, self.tokenizer.last_token, 'program', 'PERIOD'))
        except StopIteration as s:
            self._add_error(CompilationError(CompilationError.UNEXPECTED_EOF, self.tokenizer.last_token, 'program'))

        self.logger.info('Parsing finished')
        if self.errors:
            return CompilationResult(False, None, self.errors)
        else:
            code = self.code_gen.finish(self.semantic.get_var_amount())
            return CompilationResult(True, code, None)

    @property
    def code_gen(self):
        return self._code_gen

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def semantic(self):
        return self._semantic

    @staticmethod
    def is_int32(number):
        try:
            return not (int(number) >> 32)
        except ValueError:
            return False

    def _parse_factor(self, base, offset):
        tokenizer = self.tokenizer
        self.logger.info('_parse_factor')

        if tokenizer.last_token.type == 'ID':
            id_type = self.semantic.get_type(tokenizer.last_token.value, base, offset)
            if id_type == 'const':
                value = self.semantic.get_value(tokenizer.last_token.value, base, offset)
                self.code_gen.factor_number(value)
            elif id_type == 'var':
                value = self.semantic.get_value(tokenizer.last_token.value, base, offset)
                self.code_gen.factor_var(value)
            else:
                if self.semantic.id_not_exists(tokenizer.last_token.value, base, offset):
                    self._add_error(CompilationError(CompilationError.ID_NOT_EXISTS, tokenizer.last_token, 'factor'))
                else:
                    self._add_error(CompilationError(CompilationError.ID_NOT_FACTOR, tokenizer.last_token, 'factor'))

        elif tokenizer.last_token.type == 'NUMBER':
            if self.is_int32(tokenizer.last_token.value):
                self.code_gen.factor_number(tokenizer.last_token.value)
            else:
                self._add_error(CompilationError(CompilationError.INT_TOO_LARGE, tokenizer.last_token, 'factor', 'RPAREN'))
        elif tokenizer.last_token.type == 'LPAREN':
            tokenizer.next()
            self._parse_exp(base, offset)
            if tokenizer.last_token.type != 'RPAREN':
                self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'factor', 'RPAREN'))
        else:
            self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'factor', 'ID,NUMBER,LPAREN'))

        tokenizer.next()

    def _parse_term(self, base, offset):
        self.logger.info('_parse_term')
        tokenizer = self.tokenizer
        cont = True
        op = None

        while cont:
            self._parse_factor(base, offset)
            if op == 'TIMES':
                self.code_gen.mult()
                op = None
            elif op == 'SLASH':
                self.code_gen.div()
                op = None

            if tokenizer.last_token.type == 'TIMES' or tokenizer.last_token.type == 'SLASH':
                op = tokenizer.last_token.type
                tokenizer.next()
            else:
                cont = False

    def _parse_cond(self, base, offset):
        self.logger.info('_parse_cond')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type.lower() == 'odd':
            tokenizer.next()
            self._parse_exp(base, offset)
            self.code_gen.comp_odd()
        else:
            op = None
            self._parse_exp(base, offset)
            if tokenizer.last_token.type not in Scanner.COMPARATORS:
                self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'cond', 'comparator'))
            else:
                op = tokenizer.last_token.type
                tokenizer.next()
            self._parse_exp(base, offset)
            if op:
                self.code_gen.condition(op)

    def _parse_exp(self, base, offset):
        self.logger.info('_parse_exp')
        tokenizer = self.tokenizer
        cont = True
        negate = False
        op = None
        if tokenizer.last_token.type == 'PLUS':
            tokenizer.next()
        if tokenizer.last_token.type == 'MINUS':
            negate = True
            tokenizer.next()

        while cont:
            self._parse_term(base, offset)
            if negate:
                self.code_gen.neg()
                negate = False
            if op == 'PLUS':
                self.code_gen.add()
            elif op == 'MINUS':
                self.code_gen.sub()
            if tokenizer.last_token.type == 'PLUS' or tokenizer.last_token.type == 'MINUS':
                op = tokenizer.last_token.type
                tokenizer.next()
            else:
                cont = False

    def _parse_prop(self, base, offset):
        self.logger.info('_parse_prop')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type == 'ID':
            if self.semantic.id_not_exists(tokenizer.last_token.value, base, offset):
                self._add_error(CompilationError(CompilationError.ID_NOT_EXISTS, tokenizer.last_token, 'assignment', 'ID'))
            if self.semantic.cannot_assign(tokenizer.last_token.value, base, offset):
                self._add_error(CompilationError(CompilationError.ID_NOT_ASSIGNABLE, tokenizer.last_token, 'assignment', 'ID'))

            var_index = self.semantic.get_value(tokenizer.last_token.value, base, offset)
            tokenizer.next()
            if tokenizer.last_token.type == 'BECOMES' or tokenizer.last_token.type == 'EQL':
                if tokenizer.last_token.type == 'EQL':
                    self._add_error(CompilationError(CompilationError.EQL_BECOMES_MISMATCH, tokenizer.last_token, 'assignment', 'BECOMES'))
                tokenizer.next()
                self._parse_exp(base, offset)
                self.code_gen.assign(var_index)
            else:
                self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'assignment', 'BECOMES'))
                if tokenizer.last_token.type != 'SEMICOLON':
                    tokenizer.next()

        elif tokenizer.last_token.type.lower() == 'call':
            if tokenizer.next().type == 'ID':
                if self.semantic.id_not_exists(tokenizer.last_token.value, base, offset):
                    self._add_error(CompilationError(CompilationError.ID_NOT_EXISTS, tokenizer.last_token, 'call', 'ID'))
                elif self.semantic.cannot_call(tokenizer.last_token.value, base, offset):
                    self._add_error(CompilationError(CompilationError.ID_NOT_CALLABLE, tokenizer.last_token, 'call', 'ID'))

                address = self.semantic.get_value(tokenizer.last_token.value, base, offset)
                self.code_gen.call(address)
                tokenizer.next()
            elif tokenizer.last_token.type == 'SEMICOLON':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'call', 'ID'))
            else:
                self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'call', 'ID'))
                tokenizer.next()

        elif tokenizer.last_token.type.lower() == 'begin':
            seguir = True
            tokenizer.next()
            while seguir:
                token = tokenizer.last_token
                self._parse_prop(base, offset)
                if tokenizer.last_token.type.lower() == 'end':
                    seguir = False
                    tokenizer.next()
                elif tokenizer.last_token.type == 'SEMICOLON':
                    tokenizer.next()
                elif tokenizer.last_token.lexpos == token.lexpos:
                    self._add_error(CompilationError(CompilationError.INVALID_TOKEN, self._tokenizer.last_token, 'proposition', 'SEMICOLON'))
                    tokenizer.next()
                else:
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'proposition', 'SEMICOLON'))

        elif tokenizer.last_token.type.lower() == 'if':
            tokenizer.next()
            self._parse_cond(base, offset)
            if tokenizer.last_token.type.lower() != 'then':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'if', 'then'))
            else:
                tokenizer.next()
            offset = self._parse_prop(base, offset)

            self.code_gen.fix_if_jmp()

        elif tokenizer.last_token.type.lower() == 'while':
            self.code_gen.init_while()
            tokenizer.next()
            self._parse_cond(base, offset)
            if tokenizer.last_token.type.lower() != 'do':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'while', 'do'))
            else:
                tokenizer.next()
            offset = self._parse_prop(base, offset)

            self.code_gen.while_loop()
            self.code_gen.fix_if_jmp()

        elif tokenizer.last_token.type.lower() == 'readln':
            if tokenizer.next().type != 'LPAREN':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'readln', 'LPAREN'))
            else:
                tokenizer.next()
            seguir = True
            while seguir:
                if tokenizer.last_token.type == 'ID':
                    if self.semantic.id_not_exists(tokenizer.last_token.value, base, offset):
                        self._add_error(CompilationError(CompilationError.ID_NOT_EXISTS, tokenizer.last_token, 'readln', 'ID'))
                    elif self.semantic.cannot_assign(tokenizer.last_token.value, base, offset):
                        self._add_error(CompilationError(CompilationError.ID_NOT_ASSIGNABLE, tokenizer.last_token, 'readln', 'ID'))

                    var_index = self.semantic.get_value(tokenizer.last_token.value, base, offset)
                    self.code_gen.readln(var_index)
                    tokenizer.next()
                else:
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'readln', 'ID'))

                if tokenizer.last_token.type == 'RPAREN':
                    seguir = False
                    tokenizer.next()
                elif tokenizer.last_token.type == 'COMMA':
                    tokenizer.next()
                elif tokenizer.last_token.type == 'ID':
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'readln', 'COMMA'))
                else:
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'readln', 'RPAREN'))
                    seguir = False

        elif tokenizer.last_token.type.lower() == 'write' or tokenizer.last_token.type.lower() == 'writeln':
            is_writeln = tokenizer.last_token.type.lower() == 'writeln'
            seguir = True
            if tokenizer.next().type == 'LPAREN':
                tokenizer.next()
            elif is_writeln:
                self.code_gen.writeln()
                seguir = False
            else:
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'write', 'LPAREN'))
            while seguir:
                if tokenizer.last_token.type == 'STRING':
                    self.code_gen.write_string(tokenizer.last_token.value)
                    tokenizer.next()
                else:
                    self._parse_exp(base, offset)
                    self.code_gen.write_exp()
                if tokenizer.last_token.type == 'RPAREN':
                    seguir = False
                    tokenizer.next()
                elif tokenizer.last_token.type == 'COMMA':
                    tokenizer.next()
                else:
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'write', 'RPAREN'))
                    seguir = False
            if is_writeln:
                self.code_gen.writeln() # Revisar!!!!!!
        return offset

    def _parse_block(self, base=0):
        self.logger.info('_parse_block')
        self.code_gen.block_jmp()
        offset = 0
        tokenizer = self.tokenizer
        if tokenizer.last_token.type.lower() == 'const':
            seguir = True
            tokenizer.next()
            while seguir:
                const_id = None

                if tokenizer.last_token.type == 'ID':
                    if self.semantic.id_not_exists_in_context(tokenizer.last_token.value, base, offset):
                        const_id = self._tokenizer.last_token.value
                    else:
                        self._add_error(CompilationError(CompilationError.ID_ALREADY_DEFINED, tokenizer.last_token, 'const'))
                    tokenizer.next()
                elif tokenizer.last_token.type == 'EQL':
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'const', 'ID'))
                else:
                    self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'const', 'ID'))

                if tokenizer.last_token.type == 'EQL':
                    tokenizer.next()
                elif tokenizer.last_token.type == 'BECOMES':
                    self._add_error(CompilationError(CompilationError.BECOMES_EQL_MISMATCH, tokenizer.last_token, 'const', 'EQL', 'BECOMES'))
                    tokenizer.next()
                elif tokenizer.last_token.type == 'NUMBER':
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'const', 'EQL'))
                else:
                    self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'const', 'EQL'))

                value = 0
                if tokenizer.last_token.type == 'NUMBER':
                    value = tokenizer.last_token.value
                    tokenizer.next()
                elif tokenizer.last_token.type == 'SEMICOLON':
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'const', 'NUMBER'))
                else:
                    self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'const', 'NUMBER'))

                if const_id:
                    self.semantic.add_id(base, offset, 'const', const_id, value)
                    offset = offset + 1

                if tokenizer.last_token.type == 'SEMICOLON':
                    seguir = False
                    tokenizer.next()
                elif tokenizer.last_token.type == 'COMMA':
                    tokenizer.next()
                elif tokenizer.last_token.type == 'ID':
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'const', 'COMMA'))
                else:
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'const', 'SEMICOLON'))
                    seguir = False

        if tokenizer.last_token.type.lower() == 'var':
            seguir = True
            tokenizer.next()
            while seguir:
                if tokenizer.last_token.type == 'ID':
                    if self.semantic.id_not_exists_in_context(tokenizer.last_token.value, base, offset):
                        self.semantic.add_id(base, offset, "var", tokenizer.last_token.value)
                        offset = offset + 1
                    else:
                        self._add_error(CompilationError(CompilationError.ID_ALREADY_DEFINED, tokenizer.last_token, 'const'))
                    tokenizer.next()
                else:
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'var', 'ID'))

                if tokenizer.last_token.type == 'SEMICOLON':
                    seguir = False
                    tokenizer.next()
                elif tokenizer.last_token.type == 'COMMA':
                    tokenizer.next()
                elif tokenizer.last_token.type == 'ID':
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'var', 'COMMA'))
                else:
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'var', 'SEMICOLON'))
                    seguir = False

        procedure = tokenizer.last_token.type.lower() == 'procedure'
        while procedure:
            if tokenizer.next().type != 'ID':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'procedure', 'ID'))
            else:
                self.semantic.add_id(base, offset, "procedure", tokenizer.last_token.value, self.code_gen.len())
                offset = offset + 1

            if tokenizer.next().type != 'SEMICOLON':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'procedure', 'SEMICOLON'))
            else:
                tokenizer.next()

            self._parse_block(base + offset)
            self.code_gen.ret()

            if tokenizer.last_token.type != 'SEMICOLON':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'procedure', 'SEMICOLON'))
            else:
                tokenizer.next()

            procedure = tokenizer.last_token.type.lower() == 'procedure'

        self.code_gen.fix_block_jmp()
        self._parse_prop(base, offset)

    def _process_next(self, expected_token, next_token, context, default=None, mismatch=None):
        value = default
        if self._tokenizer.last_token.type != expected_token:
            if mismatch and self._tokenizer.last_token.type == mismatch:
                self._add_error(CompilationError(CompilationError.MISMATCH_TOKEN, self._tokenizer.last_token, context, expected_token, mismatch))
                self._tokenizer.next()
            elif self._tokenizer.last_token.type == next_token:
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, context, expected_token))
            else:
                self._add_error(CompilationError(CompilationError.INVALID_TOKEN, self._tokenizer.last_token, context, expected_token))
        else:
            value = self._tokenizer.last_token.value
            self._tokenizer.next()
        return value

    def _add_error(self, error):
        self.code_gen.disable()
        self.errors.append(error)

