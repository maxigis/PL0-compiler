class CompilationError(object):

    INVALID_TOKEN = 1
    MISSING_TOKEN = 2
    EQL_BECOMES_MISMATCH = 3
    BECOMES_EQL_MISMATCH = 4
    ID_TOO_LONG = 5
    NUMBER_OVERFLOW = 6
    MSG_DICT = {1: 'The id is too long'}

    def __init__(self, error_type, token, context, expected=None):
        self.error_type = error_type
        self.token = token
        self.expected = expected
        self.context = context
