#  Meh. This one was pointless and virtually identical to 2015 Day 23. And annoying too: I killed the second part assuming
#  it was stuck in an infinite loop... but it's actually doing something and just designed to run 31x longer than part 1.

def main(filepath,part):

    instr = [(x[0],x[2],x[1]) if x[0] == 'cpy' else (x[0],x[1],x[2]) if x[0] == 'jnz' else (x[0],x[1],'')
                              for x in [x.split(' ') for x in open(filepath,'r').read().replace(',','').split('\n')]]
 
    register = {'c':1} if part == 2 else {}
 
    i = 0    
    while i < len(instr):
        
        action, reg, val = instr[i]

        if   action == 'inc':  register[reg] = register.get(reg,0)+1
        elif action == 'dec':  register[reg] = register.get(reg,0)-1
        elif action == 'cpy':  register[reg] = register.get(val,0) if str(val).isalpha() else int(val)
        elif action == 'jnz':
            if str(reg).isalpha():
                reg = register.get(reg,0)
            if int(reg) != 0:
                i += (int(val)-1)
        i += 1

    return register['a']

print(main('12.txt',1))  # pt1
print(main('12.txt',2))  # pt2
