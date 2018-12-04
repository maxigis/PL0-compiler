import sys, getopt
from main.Compiler import build_program

def main(argv):
    build_program("../resources/mal/MAL-02.PL0", "program")


if __name__ == "__main__":
   main(sys.argv[1:])
