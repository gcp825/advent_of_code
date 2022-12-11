#  Part 2 approach basically consists of turning the instructions into code:
#
#  A backwards jump is a while loop (you have to move the instruction up from the bottom when codifying this)
#  A fowards jump is an if
#  Set just assigns a value to a variable
#  Sub is a calculation, and multiple subs within a loop can be refactored into a single arithmetic expression
#  A combination of forward jumps with set/sub can act as a break from a loop
#
#  Taking the instructions, rewriting as code based on the above and indenting for clarity should give a working code approximation
#  With that you should start to see what the intention of the code is (i.e. count non prime numbers in a strided range) and can start optimising
#  e.g. add breaks, remove the spurious loop, check for primality with a modulo calculation, add the square root optimisation and
#    remove registers not required in the code version (e,f & g not needed as they're just constants or control registers to make the assembly code work)
#
#  The final solution consists of running the instructions up to the beginning of the outer while loop - this just sets the constants and
#  keeps the solution generic for any input... followed by running the code version of the loop logic to perform the calculation.

from math import sqrt

def realise(register,v): return int(v) if v.replace('-','').isnumeric() else register[v]

def process(instr,register):

    i = 0;  ct = 0

    while i < len(instr):

        action, x, y = instr[i]

        if   action == 'set':  register[x] = realise(register,y)
        elif action == 'sub':  register[x] = register[x] - realise(register,y)
        elif action == 'mul':  
            register[x] = register[x] * realise(register,y)
            ct += 1
        elif action == 'jnz' and realise(register,x) !=0:   i += realise(register,y) - 1 
        i += 1

    register['mul'] = ct

    return register

def part2(instr,register):

    reg = process(instr[:8],register)
    b = reg['b'];  c = reg['c'];  h = reg['h']
    stride = abs(int(instr[-2][2]))

    for x in range(b,c+1,stride):
        for d in range(2,int(sqrt(x))+1):
            if x%d == 0:
                h += 1
                break
    return h

def main(filepath):

    instr = [tuple(x+['']) if len(x) == 2 else tuple(x) for x in [x.split(' ') for x in open(filepath,'r').read().split('\n')]]
    reg1  = dict([(r,0) for r in set([y for x,y,z in instr if y.isalpha()])])
    reg2  = dict(reg1.items());  reg2['a'] = 1

    pt1 = process(instr,reg1)    
    pt2 = part2(instr,reg2)

    return pt1['mul'], pt2

print(main('23.txt'))
