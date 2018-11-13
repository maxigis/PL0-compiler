import os
import stat

HEADER_BYTES = [127, 69, 76, 70, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 1, 0, 0, 0, 128, 132, 4, 8, 52, 0, 0, 0, 101, 0, 0, 0, 0, 0, 0, 0, 52, 0, 32, 0, 1, 0, 40, 0, 3, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 128, 4, 8, 0, 128, 4, 8, 151, 5, 0, 0, 151, 5, 0, 0, 7, 0, 0, 0, 0, 16, 0, 0, 0, 46, 115, 104, 115, 116, 114, 116, 97, 98, 0, 46, 116, 101, 120, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 84, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 1, 0, 0, 0, 6, 0, 0, 0, 224, 128, 4, 8, 224, 0, 0, 0, 183, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 82, 81, 83, 80, 184, 4, 0, 0, 0, 187, 1, 0, 0, 0, 137, 225, 186, 1, 0, 0, 0, 205, 128, 88, 91, 89, 90, 195, 85, 137, 229, 129, 236, 36, 0, 0, 0, 82, 81, 83, 184, 54, 0, 0, 0, 187, 0, 0, 0, 0, 185, 1, 84, 0, 0, 141, 85, 220, 205, 128, 129, 101, 232, 245, 255, 255, 255, 184, 54, 0, 0, 0, 187, 0, 0, 0, 0, 185, 2, 84, 0, 0, 141, 85, 220, 205, 128, 49, 192, 80, 184, 3, 0, 0, 0, 187, 0, 0, 0, 0, 137, 225, 186, 1, 0, 0, 0, 205, 128, 129, 77, 232, 10, 0, 0, 0, 184, 54, 0, 0, 0, 187, 0, 0, 0, 0, 185, 2, 84, 0, 0, 141, 85, 220, 205, 128, 88, 91, 89, 90, 137, 236, 93, 195, 184, 4, 0, 0, 0, 187, 1, 0, 0, 0, 205, 128, 195, 144, 144, 144, 176, 10, 232, 89, 255, 255, 255, 195, 4, 48, 232, 81, 255, 255, 255, 195, 61, 0, 0, 0, 128, 117, 78, 176, 45, 232, 66, 255, 255, 255, 176, 2, 232, 227, 255, 255, 255, 176, 1, 232, 220, 255, 255, 255, 176, 4, 232, 213, 255, 255, 255, 176, 7, 232, 206, 255, 255, 255, 176, 4, 232, 199, 255, 255, 255, 176, 8, 232, 192, 255, 255, 255, 176, 3, 232, 185, 255, 255, 255, 176, 6, 232, 178, 255, 255, 255, 176, 4, 232, 171, 255, 255, 255, 176, 8, 232, 164, 255, 255, 255, 195, 61, 0, 0, 0, 0, 125, 11, 80, 176, 45, 232, 236, 254, 255, 255, 88, 247, 216, 61, 10, 0, 0, 0, 15, 140, 239, 0, 0, 0, 61, 100, 0, 0, 0, 15, 140, 209, 0, 0, 0, 61, 232, 3, 0, 0, 15, 140, 179, 0, 0, 0, 61, 16, 39, 0, 0, 15, 140, 149, 0, 0, 0, 61, 160, 134, 1, 0, 124, 123, 61, 64, 66, 15, 0, 124, 97, 61, 128, 150, 152, 0, 124, 71, 61, 0, 225, 245, 5, 124, 45, 61, 0, 202, 154, 59, 124, 19, 186, 0, 0, 0, 0, 187, 0, 202, 154, 59, 247, 251, 82, 232, 48, 255, 255, 255, 88, 186, 0, 0, 0, 0, 187, 0, 225, 245, 5, 247, 251, 82, 232, 29, 255, 255, 255, 88, 186, 0, 0, 0, 0, 187, 128, 150, 152, 0, 247, 251, 82, 232, 10, 255, 255, 255, 88, 186, 0, 0, 0, 0, 187, 64, 66, 15, 0, 247, 251, 82, 232, 247, 254, 255, 255, 88, 186, 0, 0, 0, 0, 187, 160, 134, 1, 0, 247, 251, 82, 232, 228, 254, 255, 255, 88, 186, 0, 0, 0, 0, 187, 16, 39, 0, 0, 247, 251, 82, 232, 209, 254, 255, 255, 88, 186, 0, 0, 0, 0, 187, 232, 3, 0, 0, 247, 251, 82, 232, 190, 254, 255, 255, 88, 186, 0, 0, 0, 0, 187, 100, 0, 0, 0, 247, 251, 82, 232, 171, 254, 255, 255, 88, 186, 0, 0, 0, 0, 187, 10, 0, 0, 0, 247, 251, 82, 232, 152, 254, 255, 255, 88, 232, 146, 254, 255, 255, 195, 144, 144, 144, 144, 144, 144, 144, 144, 144, 184, 1, 0, 0, 0, 187, 0, 0, 0, 0, 205, 128, 144, 144, 144, 144, 185, 0, 0, 0, 0, 179, 3, 81, 83, 232, 222, 253, 255, 255, 91, 89, 60, 10, 15, 132, 52, 1, 0, 0, 60, 127, 15, 132, 148, 0, 0, 0, 60, 45, 15, 132, 9, 1, 0, 0, 60, 48, 124, 219, 60, 57, 127, 215, 44, 48, 128, 251, 0, 116, 208, 128, 251, 2, 117, 12, 129, 249, 0, 0, 0, 0, 117, 4, 60, 0, 116, 191, 128, 251, 3, 117, 10, 60, 0, 117, 4, 179, 0, 235, 2, 179, 1, 129, 249, 204, 204, 204, 12, 127, 168, 129, 249, 52, 51, 51, 243, 124, 160, 136, 199, 184, 10, 0, 0, 0, 247, 233, 61, 8, 0, 0, 128, 116, 17, 61, 248, 255, 255, 127, 117, 19, 128, 255, 7, 126, 14, 233, 127, 255, 255, 255, 128, 255, 8, 15, 143, 118, 255, 255, 255, 185, 0, 0, 0, 0, 136, 249, 128, 251, 2, 116, 4, 1, 193, 235, 3, 41, 200, 145, 136, 248, 81, 83, 232, 203, 253, 255, 255, 91, 89, 233, 83, 255, 255, 255, 128, 251, 3, 15, 132, 74, 255, 255, 255, 81, 83, 176, 8, 232, 10, 253, 255, 255, 176, 32, 232, 3, 253, 255, 255, 176, 8, 232, 252, 252, 255, 255, 91, 89, 128, 251, 0, 117, 7, 179, 3, 233, 37, 255, 255, 255, 128, 251, 2, 117, 15, 129, 249, 0, 0, 0, 0, 117, 7, 179, 3, 233, 17, 255, 255, 255, 137, 200, 185, 10, 0, 0, 0, 186, 0, 0, 0, 0, 61, 0, 0, 0, 0, 125, 8, 247, 216, 247, 249, 247, 216, 235, 2, 247, 249, 137, 193, 129, 249, 0, 0, 0, 0, 15, 133, 230, 254, 255, 255, 128, 251, 2, 15, 132, 221, 254, 255, 255, 179, 3, 233, 214, 254, 255, 255, 128, 251, 3, 15, 133, 205, 254, 255, 255, 176, 45, 81, 83, 232, 141, 252, 255, 255, 91, 89, 179, 2, 233, 187, 254, 255, 255, 128, 251, 3, 15, 132, 178, 254, 255, 255, 128, 251, 2, 117, 12, 129, 249, 0, 0, 0, 0, 15, 132, 161, 254, 255, 255, 81, 232, 4, 253, 255, 255, 89, 137, 200, 195]
POS_RUTINA_SALIDA = [0x03, 0x00]
POS_RUTINA_IMPR_NUMEROS = [0x01, 0x90]
POS_RUTINA_IMPR_CADENA = [0x01, 0x70]
POS_RUTINA_SALTO_LINEA = [0x01, 0x80]
POS_RUTINA_LECTURA = [0x03, 0x10]
EDI = [0xbf]
EDI_INICIAL = [0x0, 0x0, 0x0, 0x0]
PUSH_EAX = [0x50]
MOV_EAX_CONS = [0xb8]
MOV_ECX_CONS = [0xb9]
MOV_EDX_CONS = [0xba]
MOV_EAX_VAR = [0x8B, 0x87]
POP_EAX = [0x58]
POP_EBX = [0x5B]
IMUL_EBX = [0xF7, 0xEB]
DIVISION = [0x93, 0x99, 0xF7, 0xFB] #93 99? ???????
NEG_EAX = [0xF7, 0xD8]
ADD = [0x01, 0xD8]
SUB = [0x93, 0x29, 0xD8] #no se para que el 93 ?????
JMP = [0xe9]
MOV_VAR = [0x89, 0x87]
ODD = [0xA8, 0x01, 0x7B, 0x05]
CMP_EAX_EBX = [0x39, 0xc3]
COD_CMP = {"LSS": [0x7C, 0x05], "GTR": [0x7F, 0x05], "EQL": [0x74, 0x05], "GEQ": [0x7D, 0x05], "LEQ": [0x7E,0x05], "NEQ": [0x75, 0x05]}
CALL = [0xE8]
RETURN = [0xC3]

VAR_SIZE = 4
WORD_SIZE = 2**32

POSICION_FILESIZE = 68
POSICION_MEMORYSIZE = 72
POSICION_SIZE = 201
TAM_HEADER = 224

VIRTUAL_ADDRESS = 134512640
ADDR = 134512864


class LinuxGen(object):

    def __init__(self, output_filename):
        self.filename = output_filename
        self.stack = []
        self.stack_while = []
        self.stack_blocks = []
        self.buffer += HEADER_BYTES
        self.pos_edi = len(self.buffer) - 1
        self.buffer += EDI
        self.buffer += EDI_INICIAL

    @staticmethod
    def _calc_jump(target, current):
        return WORD_SIZE + target - current

    @staticmethod
    def _l_endian(value):
        binary = format(value, '032b')
        return [int(binary[24:32], 2), int(binary[16:24], 2), int(binary[8:16], 2), int(binary[0:8], 2)]

    @staticmethod
    def _var_padding(cant):
        return [0 for i in range(cant * VAR_SIZE)]

    def finalizar(self, cant_variables):
        # Pongo jum de salida de prograa
        self.buffer += JMP + self._l_endian(self._calc_jump(POS_RUTINA_SALIDA, len(self.buffer) + 5))
        # Modifico el edi
        self.buffer = self.buffer[:self.pos_edi + 1] + EDI + self._l_endian(VIRTUAL_ADDRESS + len(self.buffer)) + self.buffer[self.pos_edi + 6:]
        # agrego los 0s para cada variable
        self.buffer += self._var_padding(cant_variables)
        # Pongo en filesize y memory size el valor del tam del archivo
        self.buffer = self.buffer[0: POSICION_FILESIZE] + self._l_endian(len(self)) + self.buffer[POSICION_FILESIZE + 4:]

        self.buffer = self.buffer[0: POSICION_MEMORYSIZE] + self._l_endian(len(self)) + self.buffer[POSICION_MEMORYSIZE + 4:]

        # Pongo en size el tam de la porcion text
        self.buffer = self.buffer[0: POSICION_SIZE] + self._l_endian(len(self) - TAM_HEADER) + self.buffer[POSICION_SIZE + 4:]
        output_file = open(self.filename, "w")
        output_file.write(bytearray(self.buffer))
        output_file.close()
        st = os.stat(self.filename)
        os.chmod(self.filename, st.st_mode | stat.S_IEXEC)

    def _push_eax(self):
        self.buffer += PUSH_EAX

    def _pop_eax(self):
        # Optimizacion de push-pop
        if ord(self.buffer[-1]) == PUSH_EAX:
            self.buffer = self.buffer[:-1]
        else:
            self.buffer += POP_EAX

    def factor_numero(self, valor):
        valor = int(valor)
        self.buffer += MOV_EAX_CONS + self._l_endian(valor)
        self._push_eax()

    def factor_variable(self, num_var):
        self.buffer += MOV_EAX_VAR + self._l_endian(VAR_SIZE * num_var)
        self._push_eax()

    def multiplicar(self):
        self._pop_eax()
        self.buffer += POP_EBX + IMUL_EBX
        self._push_eax()

    def dividir(self):
        self._pop_eax()
        self.buffer += POP_EBX + DIVISION
        self._push_eax()

    def negar(self):
        self._pop_eax()
        self.buffer += NEG_EAX
        self._push_eax()

    def sumar(self):
        self._pop_eax()
        self.buffer += POP_EBX + ADD
        self._push_eax()

    def restar(self):
        self._pop_eax()
        self.buffer += POP_EBX + SUB
        self._push_eax()

    def asignar(self, numero_var):
        self._pop_eax()
        self.buffer += MOV_VAR + self._l_endian(VAR_SIZE * numero_var)

    def write(self, valor=None):
        if valor is None:
            # Valor desde expresion
            self._pop_eax()
            self.buffer += CALL + self._l_endian(self._calc_jump(POS_RUTINA_IMPR_NUMEROS, (len(self.buffer) + 5)))
        else:
            # Valor desde cadena
            offset = 20
            self.buffer += MOV_ECX_CONS + self._l_endian(ADDR - 0xe0 + len(self.buffer) + offset)  # revisar
            self.buffer += MOV_EDX_CONS + self._l_endian(len(valor))
            self.buffer += CALL + self._l_endian(self._calc_jump(POS_RUTINA_IMPR_CADENA, len(self.buffer) + 5))
            self.buffer += JMP + self._l_endian(len(valor) + 1)
            self.buffer += valor + chr(0)

    def writeln(self):
        self.buffer += CALL + self._l_endian(self._calc_jump(POS_RUTINA_SALTO_LINEA, (len(self.buffer) + 5)))

    def odd(self):
        self._pop_eax()
        self.buffer += ODD
        self.buffer += JMP + [0x0, 0x0, 0x0, 0x0]
        self.stack.append(len(self.buffer))

    def compare(self, comparator):
        self._pop_eax()
        self.buffer += POP_EBX + CMP_EAX_EBX + COD_CMP[comparator]
        self.buffer += JMP + [0x0, 0x0, 0x0, 0x0]
        self.stack.append(len(self.buffer))

    def fix_up(self):
        long_ult = self.stack.pop()
        long_actual = len(self.buffer)
        distance = long_actual - long_ult
        self.buffer = self.buffer[0: long_ult - 5] + JMP + self._l_endian(distance) + self.buffer[long_ult:]

    def push_while(self):
        self.stack_while.append(len(self.buffer))

    def jump_while(self):
        pos_while = self.stack_while.pop()
        self.buffer += JMP + self._l_endian(self._calc_jump(pos_while, len(self.buffer) + 5))

    def read_ln(self, var):
        self.buffer += CALL + self._l_endian(self._calc_jump(POS_RUTINA_LECTURA, len(self.buffer) + 5))
        self.buffer += MOV_VAR + self._l_endian(VAR_SIZE * var)

    def call(self, position):
        self.buffer += CALL + self._l_endian(self._calc_jump(position, len(self.buffer) + 5))

    def push_block(self):
        self.buffer += JMP + [0, 0, 0, 0]
        self.stack_blocks.append(len(self))

    def fix_block(self):
        block_address = self.stack_blocks.pop()
        distance = len(self.buffer) - int(block_address)
        # optimizacion de saltos de distancia 0
        if distance == 0:
            self.buffer = self.buffer[0: block_address - 5] + self.buffer[block_address + 5:]
        else:
            self.buffer = self.buffer[0: block_address - 4] + self._l_endian(distance) + self.buffer[block_address:]

    def add_return(self):
        self.buffer += [RETURN]

    def __len__(self):
        return len(self.buffer)
