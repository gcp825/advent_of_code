#  Decided to parse the input into a tuple of just the numeric values just to keep it simple... but that ended up a bit hacky when I then had to fudge the
#  output values to differentiate between them and bot values. Nevertheless, it doesn't look *too* bad, so have left it as is.

def read_file(filepath):

    instr = [tuple(map(int,filter(lambda x: x.isnumeric(),i)))
                 for i in [i.split(' ') for i in open(filepath,'r').read().replace('output ','100000').split('\n')]]
    
    return [i for i in instr if len(i) == 2], [i for i in instr if len(i) == 3]

def main(filepath):
    
    setup, instr = read_file(filepath)
    robot = {}; output = {}
    
    for val, bot in setup: robot[bot] = sorted(robot.get(bot,[]) + [val])

    while len(instr) > 0:
        
        remainder = []
        
        for bot, lo, hi in instr:
            
            chips = robot.get(bot,[]);  low = robot.get(lo,[]);  high = robot.get(hi,[]);
        
            if len(chips) == 2 and len(low) < 2 and len(high) < 2:
                
                if chips == [17,61]:  pt1 = bot
                
                if lo >= 1000000: output[int(str(lo)[6:])] = chips[0]
                else:             robot[lo]                = sorted(low + [chips[0]]) 
    
                if hi >= 1000000: output[int(str(hi)[6:])] = chips[1]
                else:             robot[hi]                = sorted(high + [chips[1]])
                
                robot[bot] = []
                
            else:                
                remainder += [(bot,lo,hi)]
                
        instr = [] + remainder
       
    return pt1, output[0]*output[1]*output[2]
    
                
print(main('10.txt'))
