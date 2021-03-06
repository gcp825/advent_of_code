from intcode import IntcodeComputer    # see intcode.py in this repo

def explore(f,instr):

    inp = [ord(x) for cmd in instr for x in list(cmd)+['\n']]
    damage = 0
    droid = IntcodeComputer(load=f,input=inp)
    while droid.active:
        out = droid.run()
        damage = out if droid.active else damage

    return damage

def main(f):

    #  If B/C is a hole can jump early if D is safe (and H is safe in Part 2); if A is a hole must jump now

    i1 = ['NOT B T','NOT C J','OR T J','AND D J','NOT A T','OR T J','WALK']
    i2 = ['NOT B T','NOT C J','OR T J','AND D J','AND H J','NOT A T','OR T J','RUN']

    pt1 = explore(f,i1)
    pt2 = explore(f,i2)

    return pt1, pt2 

print(main('21.txt'))
