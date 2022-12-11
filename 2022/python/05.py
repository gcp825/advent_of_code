def main(filepath,rules):

    stacks, instr = tuple([x.split('\n') for x in open(filepath,'r').read().split('\n\n')])

    stacks = [[y for y in list(x[1:]) if y != ' ']  
                   for x in [''.join([line[i] for line in stacks[::-1]]) for i in range(len(stacks[0]))] if x[0].isnumeric()]

    instr =  [(int(a),int(b)-1,int(c)-1) for a,b,c in [y.replace('from','to').split(' to ') for y in [x[5:] for x in instr]]]

    for qty, src, tgt in instr:

        stacks[tgt] = stacks[tgt] + stacks[src][-qty:][::rules]
        stacks[src] = stacks[src][:-qty]            

    return ''.join([x[-1] for x in stacks])
  
print((main('05.txt',-1),main('05.txt',1)))