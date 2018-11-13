class SemanticError(Exception):
    def __init__(self, token, message=None):
        self.message = message
        self.token = token

    def __str__(self):
        return repr(self.message)