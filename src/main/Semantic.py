
TYPE = 0
NAME = 1
VALUE = 2


class Semantic(object):
    def __init__(self):
        self.table = []
        self.var_amount = 0

    def id_exists(self, name, base, offset):
        return self._find(name, base, offset)

    def id_not_exists(self, name, base, offset):
        return not self.id_exists(name, base, offset)

    def add_id(self, base, offset, id_type, id_name, id_value=None):
        if len(self.table) < base + offset:
            raise ValueError("Index out of range: base + offset = " + str(base + offset) + " - Table size = " + str(len(self.table)))
        if self._find_in_context(id_name, base, offset):
            raise ValueError("Id already defined: " + id_name)

        if id_type == "var":
            id_value = self.var_amount
            self.var_amount += 1

        if len(self.table) == base + offset:
            self.table.append((id_type, id_name, id_value))
        else:
            self.table[base + offset] = (id_type, id_name, id_value) # ???

    def _find_in_context(self, name, base, offset):
        for i in range(base, base + offset):
            if self.table[i][NAME] == name:
                return True
        return False

    def _find(self, name, base, offset, types=None):
        for i in range(base + offset - 1, -1, -1):
            if self.table[i][NAME] == name:
                if not types or self.table[i][TYPE] in types:
                    return self.table[i]
                else:
                    return self.table[i]
        return None

    def _get(self, name, base, offset, elem):
        found = self._find(name, base, offset)
        return found[elem] if found else None

    def get_var_amount(self):
        return self.var_amount

    def cannot_assign(self, name, base, offset):
        return not self._find(name, base, offset, ["var"])

    def cannot_call(self, name, base, offset):
        return not self._find(name, base, offset, ["procedure"])

    def cannot_factor(self, name, base, offset):
        return not self._find(name, base, offset, ["var", "const"])

    def cannot_read(self, name, base, offset):
        return not self._find(name, base, offset, ["var"])

    def get_value(self, name, base, offset):
        return self._get(name, base, offset, VALUE)

    def get_type(self, name, base, offset):
        return self._get(name, base, offset, TYPE)

    def __str__(self):
        return str(self.table)
