from ParseError import ParseError
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
        self.tokenizer.next()
        self._parse_block(0)
        if self.tokenizer.last_token.type != 'PERIOD':
            raise ParseError('PERIOD', self.tokenizer.last_token)
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

    def _parse_factor(self, base, offset):
        tokenizer = self.tokenizer
        self.logger.info('_parse_factor')
        if tokenizer.last_token.type == 'LPAREN':
            tokenizer.next()
            self._parse_exp(base, offset)
            if tokenizer.last_token.type != 'RPAREN':
                raise ParseError('RPAREN', tokenizer.last_token)
        elif tokenizer.last_token.type == 'ID':
            if self.semantic.cannot_factor(tokenizer.last_token.value, base, offset):
                raise ValueError("Invalid id for factor: " + tokenizer.last_token.value)
            id_type = self.semantic.get_type(tokenizer.last_token.value, base, offset)
            if id_type == 'const':
                self.generator.factor_number(self.semantic.get_value(tokenizer.last_token.value, base, offset))
            elif id_type == 'var':
                self.generator.factor_var(self.semantic.get_value(tokenizer.last_token.value, base, offset))
            else:
                raise ValueError("Invalid factor type: " + id_type)

        elif tokenizer.last_token.type == 'NUMBER':
            self.generator.factor_number(tokenizer.last_token.value)
        else:
            raise ParseError('ID, NUMBER, LPAREN', tokenizer.last_token)
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

                raise ParseError('EQL,NEQ,LSS,LEQ,GTR,GEQ', tokenizer.last_token)
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
                raise ParseError("Undefined id", tokenizer.last_token)
            if self.semantic.cannot_assign(tokenizer.last_token.value, base, offset):
                raise ParseError("Cant assign value to id", tokenizer.last_token)
            id_token = tokenizer.last_token
            if tokenizer.next().type != 'BECOMES':
                raise ParseError('BECOMES', tokenizer.last_token)
            tokenizer.next()
            offset = self._parse_exp(base, offset)
            self.generator.becomes(self.semantic.get_value(id_token.value, base, offset))

        elif tokenizer.last_token.type.lower() == 'call':
            if tokenizer.next().type != 'ID':
                raise ParseError('ID', tokenizer.last_token)
            self.generator.call(self.semantic.get_value(tokenizer.last_token.value, base, offset))
            tokenizer.next()

        elif tokenizer.last_token.type.lower() == 'begin':
            seguir = True
            tokenizer.next()
            while seguir:
                offset = self._parse_prop(base, offset)
                if tokenizer.last_token.type.lower() == 'end':
                    seguir = False
                    tokenizer.next()
                elif tokenizer.last_token.type != 'SEMICOLON':
                    self._add_error(('end,SEMICOLON', tokenizer.last_token, 'proposition'))
                else:
                    tokenizer.next()

        elif tokenizer.last_token.type.lower() == 'if':
            tokenizer.next()
            offset = self._parse_cond(base, offset)
            if tokenizer.last_token.type.lower() != 'then':
                raise ParseError('then', tokenizer.last_token)
            tokenizer.next()
            offset = self._parse_prop(base, offset)
            self.generator.fix_up()

        elif tokenizer.last_token.type.lower() == 'while':
            self.generator.init_while()
            tokenizer.next()
            offset = self._parse_cond(base, offset)
            if tokenizer.last_token.type.lower() != 'do':
                raise ParseError('do', tokenizer.last_token)
            tokenizer.next()
            offset = self._parse_prop(base, offset)
            self.generator.fix_while()
            self.generator.fix_up()

        elif tokenizer.last_token.type.lower() == 'readln':
            if tokenizer.next().type != 'LPAREN':
                raise ParseError('LPAREN', tokenizer.last_token)
            seguir = True
            while seguir:
                if tokenizer.next().type != 'ID':
                    raise ParseError('ID', tokenizer.last_token)

                self.generator.readln(self.semantic.get_value(tokenizer.last_token.value, base, offset))
                if tokenizer.next().type == 'RPAREN':
                    seguir = False
                elif tokenizer.last_token.type != 'COMMA':
                    raise ParseError('RPAREN,COMMA', tokenizer.last_token)
            tokenizer.next()

        elif tokenizer.last_token.type.lower() == 'write' or tokenizer.last_token.type.lower() == 'writeln':
            is_writeln = tokenizer.last_token.type.lower() == 'writeln'
            if tokenizer.next().type != 'LPAREN':
                if is_writeln:
                    self.generator.writeln()
                    return offset
                else:
                    raise ParseError('LPAREN', tokenizer.last_token)
            seguir = True
            while seguir:
                if tokenizer.next().type != 'STRING':
                    offset = self._parse_exp(base, offset)
                    self.generator.write()
                else:
                    self.generator.write(tokenizer.last_token.value)
                    tokenizer.next()
                if tokenizer.last_token.type == 'RPAREN':
                    seguir = False
                elif tokenizer.last_token.type != 'COMMA':
                    raise ParseError('RPAREN,COMMA', tokenizer.last_token)
            if is_writeln:
                self.generator.writeln()
            tokenizer.next()
        return offset

    def _parse_block(self, base):
        self.logger.info('_parse_block')
        offset = 0
        self.generator.init_block()
        tokenizer = self.tokenizer
        token = tokenizer.last_token
        if token.type.lower() == 'const':
            seguir = True
            while seguir:
                const_id = None
                if tokenizer.next().type != 'ID':
                    if tokenizer.last_token.type == 'EQL':
                        self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'const', 'ID'))
                    else:
                        self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'const', 'ID'))
                        tokenizer.next()
                else:
                    const_id = tokenizer.last_token.value
                    tokenizer.next()

                if tokenizer.last_token.type != 'EQL':
                    if tokenizer.last_token.type == 'BECOMES':
                        self._add_error(CompilationError(CompilationError.EQL_BECOMES_MISMATCH, tokenizer.last_token, 'const'))
                        tokenizer.next()
                    elif tokenizer.last_token.type == 'NUMBER':
                        self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'const', 'EQL'))
                    else:
                        self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'const', 'EQL'))
                        tokenizer.next()
                else:
                    tokenizer.next()

                value = 0
                if tokenizer.last_token.type != 'NUMBER':
                    if tokenizer.last_token == 'SEMICOLON':
                        self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'const', 'NUMBER'))
                    else:
                        self._add_error(CompilationError(CompilationError.INVALID_TOKEN, tokenizer.last_token, 'const', 'NUMBER'))
                        token = tokenizer.next()
                else:
                    value = tokenizer.last_token.value
                    token = tokenizer.next()

                if const_id:
                    self.semantic.add_id(base, offset, 'const', const_id, value)
                    offset = offset + 1

                if token.type == 'SEMICOLON':
                    seguir = False
                    token = tokenizer.next()
                elif token.type != 'COMMA':
                    self._add_error(CompilationError(CompilationError.MISSING_TOKEN, tokenizer.last_token, 'const', 'SEMICOLON'))
                    seguir = False

        if token.type.lower() == 'var':
            seguir = True
            while seguir:
                if tokenizer.next().type != 'ID':
                    raise ParseError('ID', tokenizer.last_token)

                self.semantic.add_id(base, offset, "var", tokenizer.last_token.value)
                offset = offset + 1

                token = tokenizer.next()
                if token.type == 'SEMICOLON':
                    seguir = False
                elif token.type != 'COMMA':
                    raise ParseError('SEMICOLON, COMMA', tokenizer.last_token)
            token = tokenizer.next()

        procedure = token.type.lower() == 'procedure'
        while procedure:
            if tokenizer.next().type != 'ID':
                self._add_error(('ID', tokenizer.last_token, 'procedure'))
            else:
                self.semantic.add_id(base, offset, "procedure", tokenizer.last_token.value, self.generator.buffer_size())
                offset = offset + 1

            if tokenizer.next().type != 'SEMICOLON':
                self._add_error(('SEMICOLON', tokenizer.last_token))
            else:
                tokenizer.next()

            self._parse_block(base + offset)
            self.generator.add_return()

            if tokenizer.last_token.type != 'SEMICOLON':
                self._add_error(('SEMICOLON', tokenizer.last_token))
            else:
                tokenizer.next()

            procedure = tokenizer.last_token.type.lower() == 'procedure'

        self.generator.fix_block()
        self._parse_prop(base, offset)

    def _add_error(self, error):
        self.generator.disable()
        self.errors.append(error)

