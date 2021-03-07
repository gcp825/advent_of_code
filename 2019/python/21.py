#  Worst 'puzzle' ever. Not just obtusely written, but blatantly untrue in places (the Springdroid DOES run Intcode - just IntCode generated from
#  SpringScript) and there's no logical reason why ['NOT A J','OR D J','WALK'] i.e. just keep jumping whenever you have to or won't die isn't valid
#  for Part 1 other than the fact that it doesn't give the right answer. 

#  I assume the solution is actually predicated on NOT jumping unless necessary, but there's not even an implication of that being the case in the
#  description, let alone that being explicit (I've reread it several times). Just... bad.

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
