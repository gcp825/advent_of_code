#  Going to have to think about Part 2... so just Part 1 for now.
#  Heavily annotated/explained; if I just use mathematical notation or formulae without comment, I'll never remember 
#  how the maths works!

class Stone:

    def __init__(self,input):

        #  We start with (x,y,z) coordinates & (vx,vy,vz) velocity values that allow us to trace a line of travel

        self.x, self.y, self.z, self.vx, self.vy, self.vz = input

        #  The relationship between x & y on any line, and thus the line itself, can be represented by the equation
        #  y = mx + b (where m is the gradient and b is the value where the line intercepts the y axis).

        #  Thus we can also represent the line by the 3 constants in that equation i.e. for two points on the line...
        #  y = mx + b  >>  y = ((diff_in_y_axis / diff_in_x_axis) * x) + y_axis_intercept  >>  (diff_y, diff_x, intercept)

        #  Velocity is movement between 2 points on the line over time, so we already have the diff (gradient) values.
        #  To calculate the intercept, we simply rearrange the line equation  >>  b = y - mx

        self.intercept = self.y - ((self.vy/self.vx) * self.x)

        #  For easy visual comparison, we can reduce the diff values (gradient numerator & denominator) to their min values
        #  and if one of the values is negative, ensure that it is always the numerator that is signed.

        gcd = lambda a,b: abs(a) if b == 0 else gcd(b,a % b)

        self.numerator   = (-self.vy if self.vy >= 0 and self.vx < 0 else self.vy)  // gcd(self.vy,self.vx)
        self.denominator = (-self.vx if self.vy >= 0 and self.vx < 0 else self.vx)  // gcd(self.vy,self.vx)

        self.gradient = self.numerator/self.denominator


    def __str__(self):

        current  = f"coordinates: {self.x,self.y,self.z}\n"
        velocity = f"   velocity: {self.vx,self.vy,self.vz}\n"
        line_id  = f"       line: {self.numerator, self.denominator, self.intercept}"

        return '\n' + current + velocity + line_id


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


def main(filepath,window=(2*10**14,4*10**14)):

    a,b = window
    input = parse_input(filepath)
    hailstones = [Stone(hailstone) for hailstone in input]

    intersections = [Intersection(a,b).values() for i,a in enumerate(hailstones[:-1]) for b in hailstones[i+1:]]
    within_window = sum([1 for (x,y),status in intersections if status == 'intersecting' and a <= x <= b and a <= y <= b])

    return within_window


print(main('24.txt'))
