#  Love this solution. All about the parsing... will work for all inputs and as many states as can be expressed as a single character

from collections import deque

def mapper(x): return int(x) if x.isnumeric() else 1 if x == 'left' else -1 if x == 'right' else ord(x)

def main(f):

    rm = ''.maketrans('','',':.');  rp = ' steps';  p = '|'
    instr = [tuple(map(mapper,x)) for x in [x.split(p) for x in p.join([x.translate(rm).replace(rp,'').split(' ')[-1] for x in open(f,'r').read().split('\n')]).split(2*p)]]

    rules = dict([((x[0],x[1]),tuple(x[2:5][::-1])) for x in instr[1:]] + [((x[0],x[5]),tuple(x[6:9][::-1])) for x in instr[1:]])
    state, cycles = instr[0]
    tape = deque([0]*cycles)

    for _ in range(cycles):
        state, move, tape[0] = rules[(state,tape[0])]
        tape.rotate(move)

    return tape.count(1)

print(main('25.txt'))
