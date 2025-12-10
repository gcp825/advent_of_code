from itertools import combinations

class Rectangle:

    def __init__(self,a,b):

        self.a, self.b = tuple(sorted((a,b)))

        self.min_x, self.max_x = min(a[1],b[1]), max(a[1],b[1])
        self.min_y, self.max_y = min(a[0],b[0]), max(a[0],b[0])

        self.area = (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1)


    def __lt__(self, other):

        return (self.area, self.min_y, self.min_x) < (other.area, other.min_y, other.min_x)


    def __str__(self):

        return f"Area: {self.area} Corners: {self.a},{self.b}"


def parse_input(filepath):

    return [tuple(map(int,line.split(',')))[::-1] for line in open(filepath).read().split('\n')]


def overlap(r,v):

    return 1 if r.min_x < v.max_x and r.min_y < v.max_y and r.max_x > v.min_x and r.max_y > v.min_y else 0


def main(filepath):

    coords = parse_input(filepath)

    rectangles = list(sorted(Rectangle(a,b) for a,b in combinations(coords, 2)))[::-1]
    vertices = [Rectangle(a,b) for a,b in zip(coords,coords[1:]+coords[:1])]

    for r in rectangles:
        if not any(overlap(r,v) for v in vertices):
            break

    return rectangles[0].area, r.area


print(main('09.txt'))
