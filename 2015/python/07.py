def read_file(filepath):
    
    with open(filepath,'r') as f:
        
        data = [];  op = {'LSHIFT':'<<', 'RSHIFT':'>>', 'AND':'&', 'OR':'|'}

        for x in sorted([x.split(' -> ')[::-1] for x in f.read().split('\n')]):
            
            y = x[1].split(' ')
            
            if   len(y) == 1: data += [[x[0], int(y[0]) if y[0].isnumeric() else y[0],'=']]
            elif len(y) == 2: data += [[x[0], int(y[1]) if y[1].isnumeric() else y[1],'~']]
            else:             data += [[x[0],(int(y[0]) if y[0].isnumeric() else y[0],int(y[2]) if y[2].isnumeric() else y[2]), op[y[1]]]]
            
        cmds = [x for x in data if x[2] == '=' and type(x[1]) is int];
        
        while len(data) > 0:
            data =  [x for x in data if x[0] not in [y[0] for y in cmds]]
            
            cmds += [x for x in data if (type(x[1]) is tuple and (type(x[1][0]) is int or x[1][0] in [y[0] for y in cmds])
                                                             and (type(x[1][1]) is int or x[1][1] in [y[0] for y in cmds]))
                     
                                     or (type(x[1]) is not tuple and (type(x[1]) is int or x[1] in [y[0] for y in cmds]))]

    return cmds


def get_signal(op,x,wires):

    if op == '=':
        return x if type(x) is int else wires[x]
    elif op == '~':
        x = x if type(x) is int else wires[x]
        return int(bin(x)[2:].translate(''.maketrans('01','10','')).rjust(16,'1'),2)
    else:
        x,y = (x[0] if type(x[0]) is int else wires[x[0]], x[1] if type(x[1]) is int else wires[x[1]])
        return eval(str(x) + op + str(y))
    
         
def main(filepath):
    
     cmds = read_file(filepath);  signals = []
     
     for i in range(2):
         wires = {}
         for c in cmds: wires[c[0]] = get_signal(c[2],c[1],wires)
         signals += [wires['a']]
         for ix,c in enumerate(cmds): 
             if c[0] == 'b': cmds[ix] = [c[0], signals[i], c[2]]
         
     return tuple(signals)
    
     
print(main('7.txt'))
