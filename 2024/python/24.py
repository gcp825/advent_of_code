#  Originally solved with a combination of brute-force and manual inspection... but have since spent some time to
#  understand the valid structure of an adder, and used that to automatically inspect, validate and fix the
#  connections between gates and nodes.

from operator import and_, or_, xor

def parse_input(filepath):

    values, conns = open(filepath).read().split('\n\n')
    values = {k:int(v) for k,v in [tuple(v.split(': ')) for v in values.split('\n')]}
    conns = [(x[3],x[1],min(x[::2]),max(x[::2])) for x in [tuple(c.replace('-> ','').split(' ')) for c in conns.split('\n')]]

    return conns, values


def run_program(conns, values):

    funcs = {'AND' : and_ ,'OR' : or_ ,'XOR' : xor}
    connections = [] + conns

    while connections:

        target, op, a, b = connections.pop(0)

        if a in values and b in values:
            values[target] = funcs[op](values[a],values[b])
        else:
            connections += [(target, op, a, b)]

    return int(''.join(str(v) for k,v in sorted(values.items()) if k.startswith('z'))[::-1],2)


def fix_connections(conns, values):

    swapped = []
    carry = [c2 for c1 in conns for c2 in conns if c1[1:] == ('AND','x01','y01') and c1[0] in c2[2:] and c2[1] == 'OR'][0]

    for n in range(2,int(max(values)[1:])):

        n = ('0' + str(n))[-2:]
        adder = get_adder(n, conns, carry)

        if len(adder) < 5 or adder[2][0] != f'z{n}':
            swaps = (adder[2:3], [c for c in adder if c[0][0] == 'z']) if len(adder) >= 3 and adder[2][0] != f'z{n}' else (adder, adder[1:])
            conns, swapped = swap_connections(conns, list(zip(*swaps)), swapped)
            adder = get_adder(n, conns, carry)

        carry = adder[-1]

    return ','.join(list(sorted(swapped)))


def get_adder(n, conns, carry):

    Xor1  = [c for c in conns if tuplify(f'x{n}',f'y{n}') == c[2:] and c[1] == 'XOR']
    And1  = [c for c in conns if tuplify(f'x{n}',f'y{n}') == c[2:] and c[1] == 'AND']
    Xor2  = [c for c in conns if tuplify(Xor1, carry) == c[2:] and c[1] == 'XOR']
    And2  = [c for c in conns if tuplify(Xor1, carry) == c[2:] and c[1] == 'AND']
    Or    = [c for c in conns if tuplify(And1, And2) == c[2:] and c[1] == 'OR']

    return [x[0] for x in (Xor1, And1, Xor2, And2, Or) if x]


def tuplify(a,b):

    tup = lambda x: x[0][0] if type(x) is list and x else x[0] if type(x) is tuple else x if type(x) is str else ''

    return tuple(sorted((tup(a),tup(b))))


def swap_connections(conns, swaps, swapped):

    for a,b in swaps:
        conns.remove(a)
        conns.remove(b)
        conns.append((a[0],*b[1:]))
        conns.append((b[0],*a[1:]))

    return conns, swapped + sum([[c[0] for c in pair] for pair in swaps],[])


def main(filepath):

    conns, values = parse_input(filepath)

    return run_program(conns, values), fix_connections(conns, values)


print(main('24.txt'))