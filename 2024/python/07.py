#  Kept my options open for whatever Part 2 might be... that did not help as my Part 1 code came to a crashing
#  halt due to the ridiculously large numbers being computed and stored that were already > the expected result.
#  I could have hacked about with it to shoehorn in dropping anything too large... but I just felt it was cleaner
#  and easier to completely rewrite based on what was now known. And for the hell of it, I decided to implement
#  a pure maths approach to the concatenation (which does run a bit quicker than string manipulation).

from math import floor, log10
from operator import add, mul

def solve(equations, part, tally=0):

    operations = (add, mul, lambda a,b: a*(10**(floor(log10(b))+1))+b)[:part+1]

    for expected_result, start, terms in equations:

        totals = [start]

        for n in terms:
            totals = [t for t in [op(t,n) for t in totals for op in operations] if t <= expected_result]

        if expected_result in totals:
            tally += expected_result

    return tally


def main(filepath):

    equations = [(a,b,c) for a,b,*c in [map(int,x.split()) for x in open(filepath).read().replace(':','').split('\n')]]

    return tuple(solve(equations,i) for i in (1,2))


print(main('07.txt'))