#  Wrote the right solution first time around - i.e. didn't even consider trying to expand the grid.
#  The only thing I had to refactor was determining the pairs of galaxies - I originally used a list
#  comprehension that joined the list of galaxies to itself, and that was slooow. I like a list
#  comprehension, but sometimes they encourage bad habits!

class Grid:

    def __init__(self, filepath):

        grid = dict([((y,x),c) for y,r in enumerate(open(filepath).read().split('\n')) for x,c in enumerate(r)])

        self.grid = grid
        self.items = grid.items()

        max_y, max_x = max(grid.keys())

        self.empty_y = self.empty(max_y,0)
        self.empty_x = self.empty(max_x,1)


    def empty(self,max,i):

        return [i for i,v in enumerate([len(set([c for yx,c in self.items if yx[i] == n])) for n in range(max+1)]) if v == 1]


    def paired_galaxies(self):

        galaxies = list(sorted([k for k,v in self.items if v == '#']))
        pairs = []

        for i, this_galaxy in enumerate(galaxies):
            pairs += [(this_galaxy, g) for g in galaxies[i+1:]]

        return pairs


def manhattan(grid,a,b,expansion_factor):
        
    ay, ax = a; by, bx = b

    distance = (abs(by-ay) + abs(bx-ax) + 
               (len([y for y in grid.empty_y if min(ay,by) <= y <= max(ay,by)]) * (expansion_factor-1)) +
               (len([x for x in grid.empty_x if min(ax,bx) <= x <= max(ax,bx)]) * (expansion_factor-1)))

    return distance


def sum_distance(grid,pairs,expansion_factor):

    return sum([manhattan(grid,a,b,expansion_factor) for a,b in pairs])


def main(filepath):

    grid = Grid(filepath)
    pairs = grid.paired_galaxies()

    return sum_distance(grid,pairs,2), sum_distance(grid,pairs,10**6)


print(main('11.txt'))