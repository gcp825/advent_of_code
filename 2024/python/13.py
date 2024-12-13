#  Initially tried to reuse my 'find the intersection of two lines' code from Day 24 last year to calculate
#  where a line of button A presses from the origin intersects with a line of button B presses through the
#  target. This worked beautifully... for the example. But the size of the numbers and the associated floating
#  point errors with the real input absolutely sunk me... I just couldn't get it to produce the right number and
#  got to the point where I'd tried so many numbers (each rounded slightly differently) that I had to wait 5
#  minutes between submissions. So gave up on that, but had already figured out that this could be solved by
#  equations also. Hacked off after the line intersection nightmare, I almost resorted to just using the z3
#  solver to magic up the answer, but in the end pen-and-papered my way to the equations - which took me a while
#  because I'm very rusty at this...
#
#  We can represent the button presses as a pair of equations like so... where a and b are the number of
#  button presses we want to determine:
#
#  (a * ax) + (b * bx) == tx
#  (a * ay) + (b * by) == ty
#
#  We solve the equations by first eliminating one of the two unknown values. Lets remove b by multiplying
#  the first equation by 'by' and the second by 'bx'...
#
#  (a * ax * by) + (b * bx * by) == (tx * by)
#  (a * ay * bx) + (b * by * bx) == (ty + bx)
#
#  This allows us to remove (b * by * bx) from both, reducing the equations down, and forming a single equation:
#
#  (a * ax * by) == (tx * by)
#  (a * ay * bx) == (ty * bx)
#  (a * ax * by) - (a * ay * bx) == (tx * by) - (ty * bx)
#
#  We can now rearrange the remainder to get an equation that allows us to calculate a:
#
#  (a * ax * by) - (a * ay * bx) == (tx * by) - (ty * bx)
#  a * ((ax * by) - (ay * bx)) == (tx * by) - (ty * bx)
#  a == ((tx * by) - (ty * bx)) / ((ax * by) - (ay * bx))
#
#  And if we rearrange one of the initial two equations we can calculate b once we've calculated a...
#
#  (a * ax) + (b * bx) == tx
#  b == (tx - (a * ax)) / bx

import re

def solve(ax, ay, bx, by, tx, ty, adj):

    a = (((tx + adj) * by) - ((ty + adj) * bx)) / ((ax * by) - (ay * bx))
    b = ((tx + adj) - (a * ax)) / bx

    return int(3*a + b) if a == int(a) and b == int(b) else 0


def main(filepath):

    machines = [tuple(map(int,re.findall('\d+',machine))) for machine in open(filepath).read().split('\n\n')]
    tokens = [sum(solve(*machine,adj) for machine in machines) for adj in (0,10**13)]

    return tuple(tokens)


print(main('13.txt'))