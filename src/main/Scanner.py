from main import lex


class Scanner(object):

    COMPARATORS = ['=', '<>', '<', '>', '<=', '>=']

    def __init__(self, data):
        self.last_token = None
        self.build()
        self.input(data)

    keywords = (
        'begin', 'call', 'const', 'do', 'end', 'if', 'odd', 'procedure', 'then', 'var', 'while', 'write', 'writeln', 'readln'
    )

    tokens = keywords + (
        'STRING',
        'PLUS',
        'MINUS',
        'TIMES',
        'SLASH',
        'LPAREN',
        'RPAREN',
        'SEMICOLON',
        'COMMA',
        'PERIOD',
        'BECOMES',
        'EQL',
        'NEQ',
        'LSS',
        'GTR',
        'LEQ',
        'GEQ',
        'NUMBER',
        'ID',
        'NEWLINE',
    )

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_SLASH = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_SEMICOLON = r';'
    t_COMMA = r'\,'
    t_PERIOD = r'\.'
    t_BECOMES = r':='
    t_EQL = r'='
    t_NEQ = r'<>'
    t_LSS = r'<'
    t_GTR = r'>'
    t_LEQ = r'<='
    t_GEQ = r'>='
    t_STRING = r'\'(.*?)\'|\"(.*?)\"'

    def t_ID(self, t):
        r'[a-z|A-Z][a-zA-Z0-9\-_]*'
        if t.value.lower() in self.keywords:
            t.type = t.value.lower()
        return t

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Build the lexer
    def input(self, data):
        self.lexer.input(data)

    def next(self):
        self.last_token = self.lexer.next()
        return self.last_token

    # Build the lexer
    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token
