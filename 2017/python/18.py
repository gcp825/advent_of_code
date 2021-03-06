#  I decided this was a good opportunity to write a coroutine using two instances of a python generator and using the send method to pass data
#  between them. It works! And man, was it painful to get working! The send+next construct seems really illogical and took me way too long to 
#  figure out - which was at least partly due to me forgetting that for all the stackoverflow examples with a for loop, the next() is implicit!

def realise(register,v): return int(v) if v.replace('-','').isnumeric() else register[v]

def process(instr):

    register = dict([(r,0) for r in set([y for x,y,z in instr if y.isalpha()])])
    sounds = []
    i = 0    

    while i < len(instr):
        
        action, x, y = instr[i]

        if   action == 'set':  register[x] = realise(register,y)
        elif action == 'add':  register[x] = register[x] + realise(register,y)
        elif action == 'mul':  register[x] = register[x] * realise(register,y)
        elif action == 'mod':  register[x] = register[x] % realise(register,y)
        elif action == 'snd':  sounds += [register[x]]

        elif action == 'jgz' and register[x] > 0:   i += realise(register,y) - 1 
        elif action == 'rcv' and register[x] != 0:  break    

        i += 1   

    return sounds[-1]   

def program(program_id,instr):

    register = dict([(r,0) for r in set([y for x,y,z in instr if y.isalpha()])])
    register['p'] = program_id
    input_q = [];  output_q = [];  i = 0;  wait_ct = 0;  sent_ct = 0

    while True: 

        received = yield
        if type(received) is list:  input_q += received

        while 0 <= i < len(instr):  

            action, x, y = instr[i]
            i += 1

            if action == 'snd':
                output_q += [realise(register,x)]

            elif action == 'rcv':

                if len(input_q) > 0:
                    register[x] = input_q.pop(0)
                else:
                    i -= 1;  wait_ct += 1
                    break
            else:

                if   action == 'set':                               register[x] = realise(register,y)
                elif action == 'add':                               register[x] = register[x] + realise(register,y)
                elif action == 'mul':                               register[x] = register[x] * realise(register,y)
                elif action == 'mod':                               register[x] = register[x] % realise(register,y)
                elif action == 'jgz' and realise(register,x) > 0:   i += realise(register,y) - 1 

        if len(output_q) > 0:          sent = output_q; wait_ct = 0;  sent_ct += len(sent);  output_q = []
        elif i < 0 or i >= len(instr): sent = sent_ct;  wait_ct = 0
        elif wait_ct >= 5:             sent = sent_ct
        else:                          sent = None

        yield sent


def main(filepath):

    instr = [tuple(x+['']) if len(x) == 2 else tuple(x) for x in [x.split(' ') for x in open(filepath,'r').read().split('\n')]]

    input_a, input_b, output_a, output_b = (None,None,None,None)

    p = process(instr)

    a = program(0,instr);  next(a)
    b = program(1,instr);  next(b)    

    while type(output_a) is not int or type(output_b) is not int:

        output_a = a.send(input_a);  next(a)
        output_b = b.send(input_b);  next(b)

        input_a, input_b = output_b, output_a

    return p, output_b

print(main('18.txt'))
