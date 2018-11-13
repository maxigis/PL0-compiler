class ParseError(Exception):
    def __init__(self, expected, token, message=None):
        self.message = message
        self.token = token
        self.expected = expected

    def __str__(self):
        return repr(self.message)