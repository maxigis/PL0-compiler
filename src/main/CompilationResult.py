

class CompilationResult(object):

    def __init__(self, success, code_bytes, errors):
        self.success = success
        self.bytes = code_bytes
        self.errors = errors
