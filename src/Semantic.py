
class AnalizadorSemantico(object):
    def __init__(self, output):
        self.out = output
        self.table = []
        self.var_amount = 0

    def _exists_id(self, name, base, offset):
        for i in range(base, base + offset):
            if self.table[i][1] == name:
                return True
        return False

    def add_id(self, base, offset, name, type, value=None):
        if len(self.table) < base + offset:
            raise ValueError("Base + offset fuera de rango")
        if self._exists_id(name, base, offset):
            raise ValueError("Identificador en uso en este ambiente")

        if type == "var":
            value = self.var_amount
            self.var_amount += 1

        if len(self.table) == base + offset:
            self.table.append((name, type, value))
        else:
            self.table[base + offset] = (name, type, value)

    def _find(self, name, base, offset, tipos_correctos):
        for i in range(base + offset - 1, -1, -1):
            if self.table[i][NOMBRE] == name:
                if self.table[i][TIPO] in tipos_correctos or self.table[i][TIPO] == COMODIN:
                    return True
                else:
                    self.out.write("Error Semantico: " + mensaje_tipo_incorrecto + "\n")
                    return False
        self.out.write("Error Semantico: Identificador no encontrado ( "+ name +")\n")
        return False

    def can_assign(self, name, base, offset):
        return self._find(name, base, offset, ["var"],
                              "Solo pueden utilizarse variables del lado izquierdo de una asignacion")

    def can_call(self, name, base, offset):
        return self._find(name, base, offset, ["procedure"])

    def can_factor(self, name, base, offset):
        return self._find(name, base, offset, ["var", "const"])

    def can_read(self, name, base, offset):
        return self._find(name, base, offset, ["var"])

    def _get(self, name, base, offset, elem):
        for i in range(base + offset - 1, -1, -1):
            if self.table[i][1] == name:
                return self.table[i][elem]

    def get_value(self, name, base, offset):
        return self._get(name, base, offset, 2)

    def get_type(self, name, base, offset):
        return self._get(name, base, offset, 0)

    def get_var_amount(self):
        return self.var_amount

    def __str__(self):
        return str(self.table)

    def agregar_comodin(self, name, base, offset):
        for i in range(base + offset - 1, -1, -1):
            if self.table[i][1] == name:
                return False
        self.add_id(base, offset, name, COMODIN)
        return True