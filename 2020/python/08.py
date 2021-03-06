# Clunky first attempt. It works...

def read_file():

    with open('instructions.txt','r') as i:
        inst = i.read().split('\n')

    return [(x,int(y)) for x,y in [tuple(x.split(' ')) for x in inst]]


def loop(instructions):

    i = accumulator =  0
    x = len(instructions)-1
    counts = [0]*x    

    while max(counts) < 2 and i < x:
        
        counts[i] += 1
        
        if counts[i] < 2:
            if instructions[i][0] == 'acc':
                accumulator += instructions[i][1]
            if instructions[i][0] in ('nop','acc'):
                i += 1
            else:
                i += instructions[i][1]
                
    if max(counts) == 2 and i <= x:
        return ('fail', accumulator)
    else:
        return ('success', accumulator)
    
def part1(instructions):
    
    return loop(instructions)[1]
            

def part2(instructions):
    
    x = 0
    y = len(instructions)-1
    result = ''
    
    while x < y:
        
        x += 1
        if instructions[x][0] in ('nop','jmp'):
            
            inst = [] + instructions
            inst[x] = ('jmp' if instructions[x][0] == 'nop' else 'nop',instructions[x][1])
            
            result = loop(inst)
            
            if result[0] == 'success': break
            
    return result[1]

print(part1(read_file()), part2(read_file()))  #  parts 1 & 2
