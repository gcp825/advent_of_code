#  Just too much copy a previous bit of code and adapt it in 2016 AoC. That might be close to real life but it ain't much fun.
#  And given that I wasn't enthused by Day 12 originally, no way I'm taking up the strong hint with this one to work out what the purpose
#  of the data is and redesign to work faster by adding a multiply action. That is far too much like real life... so applying real life
#  decision making to this: the code works and I only need to run it once. Therefore run the existing very slow code overnight, get the
#  answer the next day and forget about this forever (or at least until Day 25 where hopefully the lack of tuning won't matter).

def main(filepath,part):

    instr = [(x[0],x[2],x[1]) if x[0] == 'cpy' else (x[0],x[1],x[2]) if x[0] == 'jnz' else (x[0],x[1],'')
                              for x in [x.split(' ') for x in open(filepath,'r').read().replace(',','').split('\n')]]
 
    register = {'a':7} if part == 1 else {'a':12}
 
    i = 0    
    while i < len(instr):
        
        action, reg, val = instr[i]

        if   action == 'inc':                    register[reg] = register.get(reg,0)+1
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

    return register['a']

print(main('23.txt',1))
print(main('23.txt',2))  #  May run for > 4 hours on a pathetic netbook!
