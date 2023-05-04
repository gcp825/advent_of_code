#  Not a fan of the deconstruct assembly code type of problem, but ultimately that wasn't necessary for Part 2.
#
#  I simply printed the registers for a number of cycles to get a feel for when register zero was updated, then 
#  ran for a larger number of cycles (with far fewer prints) to capture multiple register zero updates. After 
#  nearly 2 billion cycles (left to run in the background) it was pretty clear from the output what was going on:
#  register zero was capturing the sum of all factors of the number stored in register two.
#
#  Thus for Part 2 I just run enough cycles for the Register 2 value to be set, then calculate all the factors + sum.

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


def part1(filepath):

    pointer, register, ops = (0, [0]*6, operations())

    bound_register, instructions, scope = read_input(filepath)
    
    while pointer <= scope:
        pointer, register = apply_instructions(instructions,pointer,register,bound_register,ops)

    return register[0]


def part2(filepath):

    pointer, register, ops = (0, [1]+[0]*5, operations())

    bound_register, instructions = read_input(filepath)[:2]

    for _ in range(17):
        pointer, register = apply_instructions(instructions,pointer,register,bound_register,ops)
    
    return sum([n for n in range(1,register[2]+1) if register[2]%n == 0])


def apply_instructions(instructions,pointer,register,bound_register,ops):

    instr,a,b,c = instructions[pointer]
    operation = ops[instr]

    register[bound_register] = pointer
    register = operation(register,a,b,c)
    pointer = register[bound_register] + 1

    return pointer, register  


def main(filepath):

    return part1(filepath), part2(filepath)


print(main('19.txt'))