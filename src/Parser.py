from ParseError import ParseError
from Utils import Utils
from CompilationResult import CompilationResult
import logging


class Parser(object):

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.logger = logging.getLogger('Parser')

    def parse_factor(self, semantic, generator, base, offset):
        self.logger.info('parse_factor')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type == 'LPAREN':
            tokenizer.next()
            self.parse_exp(semantic, generator, base, offset)
            if tokenizer.last_token.type != 'RPAREN':
                raise ParseError('RPAREN', tokenizer.last_token)
        elif tokenizer.last_token.type == 'ID':
            if semantic.cannot_factor(tokenizer.last_token.value, base, offset):
                raise ValueError("Invalid id for factor: " + tokenizer.last_token.value)
            id_type = semantic.get_type(tokenizer.last_token.value, base, offset)
            if id_type == 'const':
                generator.factor_number(semantic.get_value(tokenizer.last_token.value, base, offset))
            elif id_type == 'var':
                generator.factor_var(semantic.get_value(tokenizer.last_token.value, base, offset))
            else:
                raise ValueError("Invalid factor type: " + id_type)

        elif tokenizer.last_token.type == 'NUMBER':
            generator.factor_number(tokenizer.last_token.value)
        else:
            raise ParseError('ID, NUMBER, LPAREN', tokenizer.last_token)
        tokenizer.next()
        return offset

    def parse_term(self, semantic, generator, base, offset):
        self.logger.info('parse_term')
        seguir = True
        tokenizer = self.tokenizer
        op = None
        while seguir:
            offset = self.parse_factor(semantic, generator, base, offset)
            if op == 'TIMES':
                generator.times()
            elif op == 'SLASH':
                generator.div()
            if tokenizer.last_token.type == 'TIMES' or tokenizer.last_token.type == 'SLASH':
                op = tokenizer.last_token.type
                tokenizer.next()
            else:
                seguir = False
        return offset

    def parse_cond(self, semantic, generator, base, offset):
        self.logger.info('parse_cond')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type == 'odd':
            tokenizer.next()
            offset = self.parse_exp(semantic, generator, base, offset)
            generator.odd()
        else:
            self.parse_exp(semantic, generator, base, offset)
            if (tokenizer.last_token.type != 'EQL' and tokenizer.last_token.type != 'NEQ' and
                    tokenizer.last_token.type != 'LSS' and tokenizer.last_token.type != 'LEQ' and
                    tokenizer.last_token.type != 'GTR' and tokenizer.last_token.type != 'GEQ'):

                raise ParseError('EQL,NEQ,LSS,LEQ,GTR,GEQ', tokenizer.last_token)
            comparator = tokenizer.last_token.type
            tokenizer.next()
            offset = self.parse_exp(semantic, generator, base, offset)
            generator.compare(comparator)
        return offset

    def parse_exp(self, semantic, generator, base, offset):
        self.logger.info('parse_exp')
        tokenizer = self.tokenizer
        cont = True
        invert = False
        op = None
        if tokenizer.last_token.type == 'PLUS' or tokenizer.last_token.type == 'MINUS':
            if tokenizer.last_token.type == 'MINUS':
                invert = True
            tokenizer.next()

        while cont:
            offset = self.parse_term(semantic, generator, base, offset)
            if invert:
                generator.invert()
                invert = False
            if op == 'PLUS' or op == 'MINUS':
                generator.add_or_minus(op)
            if tokenizer.last_token.type != 'PLUS' and tokenizer.last_token.type != 'MINUS':
                cont = False
            else:
                op = tokenizer.last_token.type
                tokenizer.next()

        return offset

    def parse_prop(self, semantic, generator, base, offset):
        self.logger.info('parse_prop')
        tokenizer = self.tokenizer
        if tokenizer.last_token.type == 'ID':
            if semantic.id_not_exists(tokenizer.last_token.value, base, offset):
                raise ParseError("Undefined id", tokenizer.last_token)
            if semantic.cannot_assign(tokenizer.last_token.value, base, offset):
                raise ParseError("Cant assign value to id", tokenizer.last_token)
            id_token = tokenizer.last_token
            if tokenizer.next().type != 'BECOMES':
                raise ParseError('BECOMES', tokenizer.last_token)
            tokenizer.next()
            offset = self.parse_exp(semantic, generator, base, offset)
            generator.becomes(semantic.get_value(id_token.value, base, offset))

        elif tokenizer.last_token.type == 'call':
            if tokenizer.next().type != 'ID':
                raise ParseError('ID', tokenizer.last_token)
            generator.call(semantic.get_value(tokenizer.last_token.value, base, offset))
            tokenizer.next()

        elif tokenizer.last_token.type == 'begin':
            seguir = True
            tokenizer.next()
            while seguir:
                offset = self.parse_prop(semantic, generator, base, offset)
                if tokenizer.last_token.type == 'end':
                    seguir = False
                elif tokenizer.last_token.type != 'SEMICOLON':
                    raise ParseError('end,SEMICOLON', tokenizer.last_token)
                tokenizer.next()

        elif tokenizer.last_token.type == 'if':
            tokenizer.next()
            offset = self.parse_cond(semantic, generator, base, offset)
            if tokenizer.last_token.type != 'then':
                raise ParseError('then', tokenizer.last_token)
            tokenizer.next()
            offset = self.parse_prop(semantic, generator, base, offset)
            generator.fix_up()

        elif tokenizer.last_token.type == 'while':
            generator.init_while()
            tokenizer.next()
            offset = self.parse_cond(semantic, generator, base, offset)
            if tokenizer.last_token.type != 'do':
                raise ParseError('do', tokenizer.last_token)
            tokenizer.next()
            offset = self.parse_prop(semantic, generator, base, offset)
            generator.fix_while()
            generator.fix_up()

        elif tokenizer.last_token.type == 'readln':
            if tokenizer.next().type != 'LPAREN':
                raise ParseError('LPAREN', tokenizer.last_token)
            seguir = True
            while seguir:
                if tokenizer.next().type != 'ID':
                    raise ParseError('ID', tokenizer.last_token)

                generator.readln(semantic.get_value(tokenizer.last_token.value, base, offset))
                if tokenizer.next().type == 'RPAREN':
                    seguir = False
                elif tokenizer.last_token.type != 'COMMA':
                    raise ParseError('RPAREN,COMMA', tokenizer.last_token)
            tokenizer.next()

        elif tokenizer.last_token.type == 'write' or tokenizer.last_token.type == 'writeln':
            is_writeln = tokenizer.last_token.type == 'writeln'
            if tokenizer.next().type != 'LPAREN':
                if is_writeln:
                    generator.writeln()
                    return offset
                else:
                    raise ParseError('LPAREN', tokenizer.last_token)
            seguir = True
            while seguir:
                if tokenizer.next().type != 'STRING':
                    offset = self.parse_exp(semantic, generator, base, offset)
                    generator.write()
                else:
                    generator.write(tokenizer.last_token.value)
                    tokenizer.next()
                if tokenizer.last_token.type == 'RPAREN':
                    seguir = False
                elif tokenizer.last_token.type != 'COMMA':
                    raise ParseError('RPAREN,COMMA', tokenizer.last_token)
            if is_writeln:
                generator.writeln()
            tokenizer.next()
        return offset

    def parse_block(self, semantic, generator, base):
        self.logger.info('parse_block')
        offset = 0
        generator.init_block()
        tokenizer = self.tokenizer
        token = tokenizer.last_token
        if token.type == 'const':
            seguir = True
            while seguir:
                if tokenizer.next().type != 'ID':
                    raise ParseError('ID', tokenizer.last_token)

                const_id = tokenizer.last_token.value
                if tokenizer.next().type != 'EQL':
                    raise ParseError('EQL', tokenizer.last_token)
                if tokenizer.next().type != 'NUMBER':
                    raise ParseError('NUMBER', tokenizer.last_token)

                semantic.add_id(base, offset, "const", const_id, tokenizer.last_token.value)
                offset = offset + 1

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

                semantic.add_id(base, offset, "var", tokenizer.last_token.value)
                offset = offset + 1

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

            semantic.add_id(base, offset, "procedure", tokenizer.last_token.value, generator.buffer_size())
            offset = offset + 1

            if tokenizer.next().type != 'SEMICOLON':
                raise ParseError('SEMICOLON', tokenizer.last_token)
            tokenizer.next()
            self.parse_block(semantic, generator, base + offset)
            generator.add_return()
            if tokenizer.last_token.type != 'SEMICOLON':
                raise ParseError('SEMICOLON', tokenizer.last_token)
            token = tokenizer.next()
            procedure = token.type == 'procedure'

        generator.fix_block()
        self.parse_prop(semantic, generator, base, offset)

    def parse(self, semantic, generator):
        self.logger.info('Starting parse')
        self.tokenizer.next()
        self.parse_block(semantic, generator, 0)
        if self.tokenizer.last_token.type != 'PERIOD':
            raise ParseError('PERIOD', self.tokenizer.last_token)
        self.logger.info('Parsing finished')
        generator.flush(semantic.get_var_amount())
        return CompilationResult()
