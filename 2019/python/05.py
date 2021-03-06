from copy import deepcopy

def run_opcodes(codes,**kwargs):

    def _parse_instr(n):

        param = {1:4,2:4,3:2,4:2,5:3,6:3,7:4,8:4,99:0}
        op = int(('0'+str(n))[-2:])
        p = param[op]
        modes = str(n).zfill(p+min(p,1))[:-2][::-1]

        return op, p, modes

    def _apply_mode(addr,i,n,modes):

        return addr[i+n] if modes[n-1:n] == '1' else addr[addr[i+n]]

    def _process(addr,stdin):
        
        i = 0; end = len(addr);  logs = []

        while 0 <= i < end:

            op, p, m = _parse_instr(addr[i]);  reset = False
            try:
                if   op == 99: break
                elif op == 1:  addr[addr[i+p-1]] = _apply_mode(addr,i,1,m) + _apply_mode(addr,i,2,m)
                elif op == 2:  addr[addr[i+p-1]] = _apply_mode(addr,i,1,m) * _apply_mode(addr,i,2,m)
                elif op == 3:  addr[addr[i+p-1]] = stdin
                elif op == 4:  logs += ['Instruction ' + str(i) +': ' + str(_apply_mode(addr,i,p-1,m))]
                elif op == 5:  reset, i = (True, _apply_mode(addr,i,2,m)) if _apply_mode(addr,i,1,m) != 0 else (False,i)
                elif op == 6:  reset, i = (True, _apply_mode(addr,i,2,m)) if _apply_mode(addr,i,1,m) == 0 else (False,i)
                elif op == 7:  addr[addr[i+p-1]] = 1 if _apply_mode(addr,i,1,m) < _apply_mode(addr,i,2,m) else 0
                elif op == 8:  addr[addr[i+p-1]] = 1 if _apply_mode(addr,i,1,m) == _apply_mode(addr,i,2,m) else 0

            except KeyError:  i = -99
            else:
                if not reset: i += p

        return addr, logs

   
    #  Process Input
    addresses, logs = _process(codes,kwargs.get('stdin',None))

    #  Output logs if requested
    if kwargs.get('stdout',False) is True:
        for log in logs: print(log)

    #  Print memory addresses requested
    pm = kwargs.get('print_memory',None)
    print_memory = kwargs['print_memory'] if type(pm) in (list,tuple) else list(sorted(addresses.keys())) if pm is True else []
    for addr in print_memory: print('addr:',addr,'contents:',addresses.get(addr,'Specified Address does not exist'))

    #  Output either the dict of memory addresses, the list of log records or both
    output = (addresses, logs) if kwargs.get('output',0) == 2 else logs if kwargs.get('output',0) == 1 else addresses

    return output

def main(f):

    codes = dict([(i,int(x)) for i,x in enumerate(open(f,'r').read().strip('\n').split(','))])

    pt1 = run_opcodes(deepcopy(codes),stdin=1,stdout=True,output=1)
    pt2 = run_opcodes(deepcopy(codes),stdin=5,output=1)

    return pt1[-1], pt2[-1]

print(main('05.txt'))
