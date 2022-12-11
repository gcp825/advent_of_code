#  Did not like this one bit. Overly wordy unclear puzzle, horrible input, recursion and my own incapability to stick with an approach...
#  just euuurrgh. The only thing I like is the way I maintain the leading zeroes on the hex string - which I failed at twice before getting it right.

from functools import reduce
from operator  import mul, gt, lt, eq

def parse_packet(raw):

    ver, typ, raw = parse_header(raw)

    if typ == 4:
        val, raw, sub = parse_literal(raw)
    else:
        if int(raw[0]) == 0:
            sub, raw = parse_by_length(raw[1:])
        else:
            sub, raw = parse_by_number(raw[1:])

        val = calculate_val(typ,sub)

    return (ver,typ,val,sub), raw


def parse_header(raw):

    return bin2int(raw[0:3]), bin2int(raw[3:6]), raw[6:]


def parse_literal(raw):

    i = ([raw[i] for i in range(0,len(raw),5)].index('0')*5)+5
    lit = int(''.join([x for j,x in enumerate(list(raw[:i])) if j%5 > 0]),2)

    return lit, raw[i:], []


def parse_by_length(raw):

    length = bin2int(raw[:15]);  raw = raw[15:];  sub = []
    target = len(raw)-length

    while len(raw) > target:
        packet, raw = parse_packet(raw)
        sub += [packet]

    return sub, raw


def parse_by_number(raw):

    ct = bin2int(raw[:11]);  raw = raw[11:];  sub = []

    for _ in range(ct):
        packet, raw = parse_packet(raw)
        sub += [packet]

    return sub, raw


def calculate_val(t,sub):

    ops = {0:sum,1:mul,2:min,3:max,5:gt,6:lt,7:eq}

    vals = [x[2] for x in sub];  op = ops[t]

    return op(vals) if t in (0,2,3) else (1 if op(*vals) else 0) if t in (5,6,7) else reduce(op,vals)  


def recursive_sum(packet,i,j):

    return packet[i] + sum(recursive_sum(subpacket,i,j) for subpacket in packet[j])


def bin2int(x): return int('0'+x,2) 


def main(filepath):

    raw = bin(int('1' + open(filepath,'r').read().strip('\n'),16))[3:]

    packet, _  = parse_packet(raw)

    return recursive_sum(packet,0,3), packet[2]
    
print(main('16.txt'))