
class Utils(object):
    @staticmethod
    def existe(tabla, value, base=0, desp=None):
        desp = len(tabla) if not desp else desp
        for t in reversed(tabla[base: base + desp]):
            if t[1] == value:
                return t[1]
        return None

    @staticmethod
    def no_existe(tabla, value, base=0, desp=None):
        return not Utils.existe(tabla, value, base, desp)
