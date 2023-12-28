#  Lots of learning in this one. Part 1 is 99% pure maths - the code is just a wrapper for that. Didn't know any of
#  that maths... another one where I assume I was taught this back at school but I have no recollection of it!
#  The bulk of the code is heavily annotated as a result - if I don't explain the maths, I'll never be able to 
#  recall what any of this is doing in the future just from the equations/notation.

#  Part 2, I took the opportunity to solve it with z3. Never used z3 before but had seen it mentioned on reddit
#  megathreads over the last couple of AoCs. The idea is: if you can encapsulate your problem into one or more
#  equations with common unknown variables, it'll figure out for you what values fit your unknowns.
#  Trying to get it to work wasn't much fun: the docs aren't great, the results format is bleurgh, and I couldn't get it 
#  to run with the real input using Int objects (it hangs for ever), yet it runs almost immediately with Real numbers.
#  It does however return the right answer in impressively quick time when you can get it working!

#  On a related note, there's a bit of an anti-solver vibe on the megathread for this puzzle which I don't quite get. 
#  Nobody is complaining about the use of networkx to solve Day 25, yet that makes Part 2 of that puzzle even more 
#  trivial than z3 does here. Nobody complains about the use of itertools, but pretty much everything in that library 
#  can easily be implemented with your own bespoke code... which nobody does unless explictly trying to avoid imports
#  for their own AoC challenge. So, what makes one convenience package acceptable and another not? Plus this puzzle
#  specifically screams maths challenge much more than it does code challenge - if you've got a complaint, that's a
#  more obvious target surely?

#  Anyway, for what it's worth... I think I've also figured out a solution to Part 2 that reuses the intersections
#  determined in Part 1. Whether I'll be able to get that to run in a reasonable amount of time: no idea - I've got
#  a bit of AoC fatigue right now, so definitely won't be trying that out immediately!

from z3 import Real, Solver

class Hailstone:

    def __init__(self,input):

        #  We start with (x,y,z) coordinates & (vx,vy,vz) velocity values that allow us to trace a line of travel

        self.x, self.y, self.z, self.vx, self.vy, self.vz = input
        self.input = input

        #  The relationship between x & y on any line, and thus the line itself, can be represented by the equation
        #  y = mx + b (where m is the gradient and b is the value where the line intercepts the y axis).

        #  Thus we can also represent the line by the constants in that equation i.e. for two points on the line...
        #  y = mx + b  >>  y = ((diff_in_y_axis / diff_in_x_axis) * x) + y_axis_intercept  >>  (diff_y, diff_x, intercept)

        #  Velocity is movement between 2 points on the line over time, so we already have the diff (gradient) values.
        #  To calculate the intercept, we simply rearrange the line equation  >>  b = y - mx

        self.intercept = self.y - ((self.vy/self.vx) * self.x)

        #  For easy visual comparison, we can reduce the diff values (gradient numerator & denominator) to their min values
        #  and if one of the values is negative, ensure that it is always the numerator that is signed.
        #  Strictly speaking, this is unnecessary for this puzzle, but it ensures that two representations of a line such as 
        #  (-3,12,5) and (12,-48,5) are identified as the same line i.e. (-1,4,5)

        gcd = lambda a,b: abs(a) if b == 0 else gcd(b,a % b)

        self.numerator   = (-self.vy if self.vy >= 0 and self.vx < 0 else self.vy)  // gcd(self.vy,self.vx)
        self.denominator = (-self.vx if self.vy >= 0 and self.vx < 0 else self.vx)  // gcd(self.vy,self.vx)
        self.gradient    = self.numerator/self.denominator

        self.line_id = (self.numerator, self.denominator, self.intercept)


    def __str__(self):

        current  = f"coordinates: {self.x,self.y,self.z}\n"
        velocity = f"   velocity: {self.vx,self.vy,self.vz}\n"
        line_id  = f"       line: {self.line_id}"

        return '\n' + current + velocity + line_id


    def values(self):

        return (self.input, self.line_id)


class Intersection:

    def __init__(self,a,b):

        self.a = (a.numerator,a.denominator,a.intercept)
        self.b = (b.numerator,b.denominator,b.intercept)

        #  To calculate the intersection of 2 lines, we first check whether they have equal gradients (are parallel).
        #  If so, they will never intersect.
        #  We do this by cross multiplication, as this will rule out false diffs due to floating point calculations.

        if (a.numerator * b.denominator) == (b.numerator * a.denominator):

            self.status = 'parallel'
            self.intersect = (None,None)

        else:

        #  We can calculate the x coordinate of an intersection with the equation x = (b2-b1) / (m1-m2)
        #  We can then calculate the y coordinate, with y = mx + b for one of the lines

            x = (b.intercept - a.intercept) / (a.gradient - b.gradient)
            y = (a.gradient * x) + a.intercept

            self.intersect = (x,y)

        #  Use manhattan distance from the current coordinates on each line to the point of intersection
        #  to determine whether the intersection was in the past or will happen in the future

            statuses = []
            for line in (a,b):
                current_manhattan = (abs(line.y-y) + abs(line.x-x))
                future_manhattan  = (abs(line.y + line.vy - y) + abs(line.x + line.vx - x))
                statuses += ['intersected' if current_manhattan < future_manhattan else 'intersecting']

            self.status = min(statuses)


    def __str__(self):

        lines     = f"{self.a} x {self.b}\n"
        status    = f"   status: {self.status}\n"
        intersect = f"   intersection: {self.intersect}"

        return '\n' + lines + status + intersect


    def values(self):

        return (self.intersect,self.status)


def parse_input(filepath):

    return [tuple(map(int,x.split(','))) for x in open(filepath).read().replace('@',',').split('\n')]


def z3_solver(hailstones):

    # Set up unknown variables we'll be using in our equations as z3 objects
    # Using Real rather than Int; z3 wouldn't return an answer using Int for the real input (example worked fine)

    rock = [Real(i) for i in 'x,y,z,vx,vy,vz'.split(',')]
    time = [Real('ns' + str(i)) for i in range(len(hailstones))]

    # Instantiate Solver and add equations to solve...

    equations = []
    for i,(hailstone, _) in enumerate([stone.values() for stone in hailstones]):
        for dim in range(3):
            equations += [rock[dim] + (rock[dim+3] * time[i]) == hailstone[dim] + (hailstone[dim+3] * time[i])]

    solver = Solver()
    solver.add(*equations)

    # Solve...

    status = solver.check()
    if status == 'unsat':
        raise ValueError("Equations supplied to z3 do not have a common satisfiable solution")
    else:
        results = solver.model()
        return sum([int(str(results[key])) for key in results if str(key) in ('x','y','z')])


def main(filepath,window=(2*10**14, 4*10**14)):

    a,b = window
    input = parse_input(filepath)
    hailstones = [Hailstone(hailstone) for hailstone in input]

    intersections   = [Intersection(a,b).values() for i,a in enumerate(hailstones[:-1]) for b in hailstones[i+1:]]
    within_window   = sum([1 for (x,y),status in intersections if status == 'intersecting' and a <= x <= b and a <= y <= b])
    sum_rock_coords = z3_solver(hailstones)

    return within_window, sum_rock_coords


print(main('24.txt'))
