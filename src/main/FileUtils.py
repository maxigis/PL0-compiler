import os
import stat
from pathlib import Path


def read_lines(filename):
    lines = []
    try:
        file = open(filename)
    except IOError:
        raise IOError("Error reading file")
    for line in file:
        lines.append(line)
    file.close()
    return lines


def read_binary(filename):
    file = open(filename, 'rb')

    try:
        content = file.read()
    finally:
        file.close()
    return content


def file_exists(filename):
    return Path(filename).is_file()


def read_file(filename):
    lines = read_lines(filename)
    return "".join(lines)


def write_bin(filename, content):
    output_file = open(filename, "wb")
    output_file.write(content)
    output_file.close()


def make_executable(filename):
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


def write_lines(filename, lines):
    output_file = open(filename, "w")
    for line in lines:
        output_file.write(line)
    output_file.close()
