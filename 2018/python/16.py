def read_input(filepath):

    parts = open(filepath).read().split('\n\n\n\n')

    sample_lines = [list(map(int,x.split(' '))) for x in
                       [y if '[' not in y else y[y.find('[')+1:y.find(']')].replace(',','') for y in
                           parts[0].replace('\n\n','\n').split('\n')]]

    samples = [sample_lines[x:x+3] for x in range(0,len(sample_lines),3)]
    instructions = [tuple(map(int,x.split(' '))) for x in parts[-1].split('\n')]

    return samples, instructions


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


def try_operation(registers, instr, results):

    return [opname for opname, operation in operations().items() if operation(registers,*tuple(instr[1:])) == results]


def determine_opcodes(samples):

    opcodes = dict()

    while len(opcodes) < 16:
    
        for sample in samples:
            unmatched_opnames = [x for x in try_operation(*sample) if x not in opcodes.values()]
            if len(unmatched_opnames) == 1:
                opcodes[sample[1][0]] = unmatched_opnames[0]

    return opcodes


def run_program(instructions,opcode_lookup):

    registers = [0]*4
    operation_lookup = operations()

    for opcode, a, b, c in instructions:
        operation = operation_lookup[opcode_lookup[opcode]]
        registers = operation(registers,a,b,c)

    return registers


def main(filepath):

    samples, instructions = read_input(filepath)

    pt1 = sum([1 if len(try_operation(*sample)) >= 3 else 0 for sample in samples])
    pt2 = run_program(instructions,determine_opcodes(samples))[0]

    return pt1, pt2


print(main('16.txt'))