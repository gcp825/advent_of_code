import re

def parse_input(filepath):

    numbers = list(map(int,re.findall('\d+', open(filepath).read())))

    return numbers[:3], numbers[3:]


def combo(operand, register):

    return register[operand-4] if operand >= 4 else operand


def operations(i, opcode, operand, register):

    output = []

    if opcode == 0:
        register[0] = register[0] // 2**combo(operand, register)

    if opcode == 1:
        register[1] = register[1] ^ operand

    if opcode == 2:
        register[1] = combo(operand, register) % 8

    if opcode == 3:
        if register[0] != 0:
            i = operand-2

    if opcode == 4:
        register[1] = register[1] ^ register[2]

    if opcode == 5:
        output += [combo(operand, register) % 8]

    if opcode == 6:
        register[1] = register[0] // 2**combo(operand, register)

    if opcode == 7:
        register[2] = register[0] // 2**combo(operand, register)

    return i+2, register, output


def run(register, instr):

    i, output = 0, []

    while i < len(instr):
        i, register, out = operations(i, instr[i], instr[i+1], register)
        output += out

    return ','.join(str(x) for x in output)


def main(filepath):

    return run(*parse_input(filepath))


print(main('17.txt'))