from main.CompilationResult import CompilationResult
from main.CompilationError import CompilationError
import logging


class Parser(object):

    def __init__(self, tokenizer, semantic, generator):
        self.logger = logging.getLogger('Parser')
        self.errors = []
        self._tokenizer = tokenizer
        self._semantic = semantic
        self._generator = generator

    def parse(self):
        self.logger.info('Starting parse')
        try:
            self.tokenizer.next()
            self._parse_block(0)
            if self.tokenizer.last_token.type != 'PERIOD':
                self._add_error(CompilationError(CompilationError.INVALID_TOKEN, self.tokenizer.last_token, 'program', 'PERIOD'))
        except StopIteration as s:
            self._add_error(CompilationError(CompilationError.UNEXPECTED_EOF, self.tokenizer.last_token, 'program'))

        self.logger.info('Parsing finished')
        if self.errors:
            return CompilationResult(False, None, self.errors)
        else:
            self.generator.finalize(self.semantic.get_var_amount())
            return CompilationResult(True, self.generator.buffer, None)

    @property
    def generator(self):
        return self._generator

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
            if self.semantic.cannot_factor(tokenizer.last_token.value, base, offset):
                self._add_error(CompilationError(CompilationError.ID_NOT_FACTOR, tokenizer.last_token, 'factor'))
            else:
                id_type = self.semantic.get_type(tokenizer.last_token.value, base, offset)
                if id_type == 'const':
                    self.generator.factor_number(self.semantic.get_value(tokenizer.last_token.value, base, offset))
                elif id_type == 'var':
                    self.generator.factor_var(self.semantic.get_value(tokenizer.last_token.value, base, offset))
                else:
                    raise ValueError("Invalid factor type: " + id_type)  # this should be unreachable

            # tokenizer.next()
        elif tokenizer.last_token.type == 'NUMBER':
            if self.is_int32(tokenizer.last_token.value):
                self.generator.factor_number(tokenizer.last_token.value)
            else:
                self._add_error(CompilationError(CompilationError.INT_TOO_LARGE, tokenizer.last_token, 'factor', 'RPAREN'))
            # tokenizer.next()
        elif tokenizer.last_token.type == 'LPAREN':
            tokenizer.next()
            self._parse_exp(base, offset)
            if tokenizer.last_token.type != 'RPAREN':
                self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'factor', 'RPAREN'))
            # else:
                # tokenizer.next()
        else:
            self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'factor', 'ID,NUMBER,LPAREN'))

        tokenizer.next()

        return offset

    def _parse_term(self, base, offset):
        self.logger.info('_parse_term')
        seguir = True
        tokenizer = self.tokenizer
        op = None
        while seguir:
            offset = self._parse_factor(base, offset)
            if op == 'TIMES':
                self.generator.times()
            elif op == 'SLASH':
                self.generator.div()
            if tokenizer.last_token.type == 'TIMES' or tokenizer.last_token.type == 'SLASH':
                op = tokenizer.last_token.type
                tokenizer.next()
            else:
                seguir = False
        return offset

    def _parse_cond(self, base, offset):
        self.logger.info('_parse_cond')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type.lower() == 'odd':
            tokenizer.next()
            offset = self._parse_exp(base, offset)
            self.generator.odd()
        else:
            self._parse_exp(base, offset)
            if (tokenizer.last_token.type != 'EQL' and tokenizer.last_token.type != 'NEQ' and
                    tokenizer.last_token.type != 'LSS' and tokenizer.last_token.type != 'LEQ' and
                    tokenizer.last_token.type != 'GTR' and tokenizer.last_token.type != 'GEQ'):

                self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'cond', 'comparator'))
                comparator = None
            else:
                comparator = tokenizer.last_token.type
                tokenizer.next()
            offset = self._parse_exp(base, offset)
            self.generator.compare(comparator)
        return offset

    def _parse_exp(self, base, offset):
        self.logger.info('_parse_exp')
        tokenizer = self.tokenizer
        cont = True
        invert = False
        op = None
        if tokenizer.last_token.type == 'PLUS' or tokenizer.last_token.type == 'MINUS':
            if tokenizer.last_token.type == 'MINUS':
                invert = True
            tokenizer.next()

        while cont:
            offset = self._parse_term(base, offset)
            if invert:
                self.generator.invert()
                invert = False
            if op == 'PLUS' or op == 'MINUS':
                self.generator.add_or_minus(op)
            if tokenizer.last_token.type != 'PLUS' and tokenizer.last_token.type != 'MINUS':
                cont = False
            else:
                op = tokenizer.last_token.type
                tokenizer.next()

        return offset

    def _parse_prop(self, base, offset):
        self.logger.info('_parse_prop')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type == 'ID':
            if self.semantic.id_not_exists(tokenizer.last_token.value, base, offset):
                self._add_error(CompilationError(CompilationError.ID_NOT_EXISTS, tokenizer.last_token, 'assignment', 'ID'))
            if self.semantic.cannot_assign(tokenizer.last_token.value, base, offset):
                self._add_error(CompilationError(CompilationError.ID_NOT_ASSIGNABLE, tokenizer.last_token, 'assignment', 'ID'))
            id_token = tokenizer.last_token
            tokenizer.next()
            if tokenizer.last_token.type == 'BECOMES' or tokenizer.last_token.type == 'EQL':
                if tokenizer.last_token.type == 'EQL':
                    self._add_error(CompilationError(CompilationError.EQL_BECOMES_MISMATCH, tokenizer.last_token, 'assignment', 'BECOMES'))
                tokenizer.next()
                offset = self._parse_exp(base, offset)
                self.generator.becomes(self.semantic.get_value(id_token.value, base, offset))
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
                else:
                    self.generator.call(self.semantic.get_value(tokenizer.last_token.value, base, offset))

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
                offset = self._parse_prop(base, offset)
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
            offset = self._parse_cond(base, offset)
            if tokenizer.last_token.type.lower() != 'then':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'if', 'then'))
            else:
                tokenizer.next()
            offset = self._parse_prop(base, offset)
            self.generator.fix_up()

        elif tokenizer.last_token.type.lower() == 'while':
            self.generator.init_while()
            tokenizer.next()
            offset = self._parse_cond(base, offset)
            if tokenizer.last_token.type.lower() != 'do':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'while', 'do'))
            else:
                tokenizer.next()
            offset = self._parse_prop(base, offset)
            self.generator.fix_while()
            self.generator.fix_up()

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
                    self.generator.readln(self.semantic.get_value(tokenizer.last_token.value, base, offset))
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
            if tokenizer.next().type == 'LPAREN':
                tokenizer.next()
            elif is_writeln:
                self.generator.writeln()
                return offset
            else:
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'write', 'LPAREN'))
            seguir = True
            while seguir:
                if tokenizer.last_token.type != 'STRING':
                    offset = self._parse_exp(base, offset)
                    self.generator.write()
                else:
                    self.generator.write(tokenizer.last_token.value)
                    tokenizer.next()
                if tokenizer.last_token.type == 'RPAREN':
                    seguir = False
                    tokenizer.next()
                elif tokenizer.last_token.type == 'COMMA':
                    tokenizer.next()
                else:
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, self._tokenizer.last_token, 'write', 'RPAREN'))
                    seguir = False
            if is_writeln:
                self.generator.writeln()
        return offset

    def _parse_block(self, base):
        self.logger.info('_parse_block')
        self.generator.init_block()
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
                self.semantic.add_id(base, offset, "procedure", tokenizer.last_token.value, self.generator.buffer_size())
                offset = offset + 1

            if tokenizer.next().type != 'SEMICOLON':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'procedure', 'SEMICOLON'))
            else:
                tokenizer.next()

            self._parse_block(base + offset)
            self.generator.add_return()

            if tokenizer.last_token.type != 'SEMICOLON':
                self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'procedure', 'SEMICOLON'))
            else:
                tokenizer.next()

            procedure = tokenizer.last_token.type.lower() == 'procedure'
# next() ?
        self.generator.fix_block()
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
        self.generator.disable()
        self.errors.append(error)

