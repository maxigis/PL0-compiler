import os
import stat


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


def read_file(filename):
    lines = read_lines(filename)
    return "\n".join(lines)


def write_bin(filename, content):
    output_file = open(filename, "wb")
    output_file.write(content)
    output_file.close()


def make_executable(filename):
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)

