#  Attempted some future-proofing. We'll see how that goes...

from copy import deepcopy

def run_opcodes(codes,request,printout):

    def _process(addr):

        instr = {1:4,2:4,99:0}
        i = 0; end = len(addr)

        while 0 <= i < end:
            op = addr[i]
            if   op == 99: break
            elif op == 1:  
                try: addr[addr[i+3]] = addr[addr[i+1]] + addr[addr[i+2]] 
                except KeyError: break
            elif op == 2:  
                try: addr[addr[i+3]] = addr[addr[i+1]] * addr[addr[i+2]] 
                except KeyError: break
            i += instr[op]

        return addr

    addresses = _process(codes)
    if printout: print([v for k,v in sorted(addresses.items())])
    return tuple(addresses[i] for i in request) if len(request) > 1 else addresses[request[0]]

def main(f,request,p=False):

    codes = dict([(i,int(x)) for i,x in enumerate(open(f,'r').read().strip('\n').split(','))])

    opcodes = deepcopy(codes);  opcodes[1], opcodes[2] = 12,2
    part1   = run_opcodes(opcodes,request,p)

    for i in range(100):
        for j in range(100):
            opcodes = deepcopy(codes);  opcodes[1], opcodes[2] = i,j
            part2 = run_opcodes(opcodes,request,p)
            if part2 == 19690720: break
        if part2 == 19690720: break

    return part1, i*100+j

print(main('02.txt',[0]))
