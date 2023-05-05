# Ugh. Another one of these... I have no interest in reverse-engineering deliberately inefficient assembly code, so this is pure brute force.
# Part 2 runs in about 11 mins using pypy & who knows how long using regular python (my laptop is cheap + underpowered though!)

def read_input(filepath):

    input = [(x[0],*tuple(map(int,x[1:]))) for x in [x.split(' ') for x in open(filepath).read().split('\n')]]

    return input[0][1], input[1:], len(input)-2


def operations():

    return {
        'addr' :  lambda reg,a,b,c : [reg[a] + reg[b] if i == c else x for i,x in enumerate(reg)],
        'addi' :  lambda reg,a,b,c : [reg[a] + b if i == c else x for i,x in enumerate(reg)],
        'mulr' :  lambda reg,a,b,c : [reg[a] * reg[b] if i == c else x for i,x in enumerate(reg)],
        'muli' :  lambda reg,a,b,c : [reg[a] * b if i == c else x for i,x in enumerate(reg)],
        'banr' :  lambda reg,a,b,c : [reg[a] & reg[b] if i == c else x for i,x in enumerate(reg)],
        'bani' :  lambda reg,a,b,c : [reg[a] & b if i == c else x for i,x in enumerate(reg)],
        'borr' :  lambda reg,a,b,c : [reg[a] | reg[b] if i == c else x for i,x in enumerate(reg)],
        'bori' :  lambda reg,a,b,c : [reg[a] | b if i == c else x for i,x in enumerate(reg)],
        'setr' :  lambda reg,a,b,c : [reg[a] if i == c else x for i,x in enumerate(reg)],
        'seti' :  lambda reg,a,b,c : [a if i == c else x for i,x in enumerate(reg)],
        'gtir' :  lambda reg,a,b,c : [1 if i == c and a > reg[b] else 0 if i == c else x for i,x in enumerate(reg)],
        'gtri' :  lambda reg,a,b,c : [1 if i == c and reg[a] > b else 0 if i == c else x for i,x in enumerate(reg)],
        'gtrr' :  lambda reg,a,b,c : [1 if i == c and reg[a] > reg[b] else 0 if i == c else x for i,x in enumerate(reg)],
        'eqir' :  lambda reg,a,b,c : [1 if i == c and a == reg[b] else 0 if i == c else x for i,x in enumerate(reg)],
        'eqri' :  lambda reg,a,b,c : [1 if i == c and reg[a] == b else 0 if i == c else x for i,x in enumerate(reg)],
        'eqrr' :  lambda reg,a,b,c : [1 if i == c and reg[a] == reg[b] else 0 if i == c else x for i,x in enumerate(reg)]
    }


def run(filepath,part):

    pointer, register, ops, seen = (0, [0]*6, operations(), [])

    bound_register, instructions, max_idx = read_input(filepath)

    while pointer <= max_idx:

        pointer, register, exit_value = apply_instructions(instructions,pointer,register,bound_register,ops)

        if exit_value:

            if exit_value in seen: break
            seen += [exit_value]
            if part == 1: break

    return seen[-1]


def apply_instructions(instructions,pointer,register,bound_register,ops):

    instr,a,b,c = instructions[pointer]
    operation = ops[instr]

    register[bound_register] = pointer
    register = operation(register,a,b,c)
    pointer = register[bound_register] + 1

    return pointer, register, register[4] if instr == 'eqrr' else False



def main(filepath):

    return run(filepath,1), run(filepath,2)


print(main('21.txt'))