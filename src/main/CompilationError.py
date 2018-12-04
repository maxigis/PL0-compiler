class CompilationError(object):

    FATAL = -1
    INVALID_TOKEN = 1
    MISSING_TOKEN = 2
    MISMATCH_TOKEN = 3
    INT_TOO_LARGE = 4
    ID_NOT_EXISTS = 5
    ID_NOT_ASSIGNABLE = 6
    ID_NOT_CALLABLE = 7
    ID_ALREADY_DEFINED = 8
    ID_NOT_FACTOR = 9
    BECOMES_EQL_MISMATCH = 10
    EQL_BECOMES_MISMATCH = 11
    UNEXPECTED_EOF = 12
    MSG_DICT = {
        1: 'Token inválido',
        2: 'Token no encontrado',
        3: 'Token equivocado',
        4: 'Id no se encuentra definido',
        5: 'Entero demasiado largo',
        6: 'Id no es asignable',
        7: 'Id no invocable',
        8: 'Id ya se encuentra definido en este contexto',
        9: 'Id no se puede usar como factor',
        10: 'Se esperaba = y se encontro :=',
        11: 'Se esperaba := y se encontro =',
        12: 'Final del archivo inesperado',
    }

    def __init__(self, error_type, token, context, expected=None, mismatch=None):
        self.error_type = error_type
        self.token = token
        self.expected = expected
        self.context = context
        self.mismatch = mismatch
