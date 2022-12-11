def read_file(filepath):
    
    instr = []
    for x in [x.split(' ') for x in [x for x in open(filepath,'r').read().replace(',','').split('\n')]]:
        instr += [(x[0],'',int(x[1])) if x[0] == 'jmp' else (x[0],x[1],int(x[2])) if x[0].startswith('j') else (x[0],x[1],0)]
    return instr

def process(instr,init):
    
    a,b = init    
    register = {'a': a, 'b': b};  i = 0
    
    while i < len(instr):
        
        action, r, offset = instr[i]

        if   action == 'jmp':  i += offset
        elif action == 'jie':  i = i + offset if register[r] % 2 == 0 else i + 1
        elif action == 'jio':  i = i + offset if register[r] == 1 else i + 1
        else:
            i += 1;  reg = register[r]
            register[r] = reg//2 if action == 'hlf' else reg*3 if action == 'tpl' else reg+1

    return register

def main(filepath,init):
    
    return process(read_file(filepath),init)

print(main('23.txt',(0,0)))  #  pt1
print(main('23.txt',(1,0)))  #  pt2
