# Refactored to remove the ternary stuff and add some unnecessarily complicated maths

def main(filepath):

    cmds    = [(x[:1],int(y)) for x,y in [x.split(' ') for x in open(filepath,'r').read().split('\n')]]
    results = []

    for p in [0,1]:

        x,y,z = (0,0,0)

        for i,v in cmds:
            if i == 'u':  z -= v ;  y -= (v*((p-1)**2))
            if i == 'd':  z += v ;  y += (v*((p-1)**2))
            if i == 'f':  x += v ;  y += (z*v*p)  

        results += [x*y]

    return results

print(main('02.txt'))