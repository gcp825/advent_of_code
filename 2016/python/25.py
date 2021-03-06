#  Day12 & 23 retread. Ho-hum.

def search(instr,initial_value,break_at=10):

    register = {'a':initial_value};  i = 0;  out = []
    
    while i < len(instr):
        
        action, reg, val = instr[i]

        if   action == 'out':                    out += [register.get(reg,0)]
        elif action == 'inc':                    register[reg] = register.get(reg,0)+1
        elif action == 'dec':                    register[reg] = register.get(reg,0)-1
        elif action == 'cpy' and reg.isalpha():  register[reg] = register.get(val,0) if str(val).isalpha() else int(val)
        elif action == 'jnz':
            if str(reg).isalpha():
                reg = register.get(reg,0)
            if int(reg) != 0:
                if str(val).isalpha():
                    val = register.get(val,0)
                i += (int(val)-1)
        elif action == 'tgl':
            if str(reg).isalpha():
                reg = register.get(reg,0)
            idx = i + int(reg)
            a, r, v = instr[idx] if len(instr[idx:idx+1]) > 0 else ('skip','','')
            if a != 'skip':
                if a == 'inc':           instr[idx] = ('dec',r,v)
                elif a in ('dec','tgl'): instr[idx] = ('inc',r,v)
                elif a == 'jnz':         instr[idx] = ('cpy',v,r)
                elif a == 'cpy':         instr[idx] = ('jnz',v,r) 
        i += 1

        if action == 'out':       
            if ((len(out)%2 == 1 and out[-1] != 0)
            or  (len(out)%2 == 0 and out[-1] != 1)
            or  (len(out) == break_at)):
                break

    return True if len(out) == break_at else False


def main(filepath):

    instr = [(x[0],x[2],x[1]) if x[0] == 'cpy' else (x[0],x[1],x[2]) if x[0] == 'jnz' else (x[0],x[1],'')
                              for x in [x.split(' ') for x in open(filepath,'r').read().replace(',','').split('\n')]]
    
    for n in range(1000000):
        break_now = search(instr,n)
        if break_now: break 

    return n

print(main('25.txt'))
