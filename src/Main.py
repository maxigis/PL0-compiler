from Parser import Parser
from Scanner import Scanner
from ParseError import ParseError

data = '''
var r, n;

procedure inicializar;
const uno = 1;
r := -(-uno);

procedure raiz;
begin
  call inicializar;
  while r * r < n do r := r + 1
end;

begin
  if n < 0 then n := 0;
  if n = 0 then n := 1;, desp
  readln(n);
  if n > 0 then
    begin
      call raiz;
      if r*r<>n then r := 1;
    end;
end.
'''


tokenizer = Scanner(data)

parser = Parser(tokenizer)

try:
    parser.parse()
except ParseError as e:
    print('Error de sintaxis, en linea ' + str(
        e.token.lineno) + ' se esperaba ' + e.expected + ' y se encontro ' + e.token.value)
    print(str.splitlines(data)[e.token.lineno - 1])