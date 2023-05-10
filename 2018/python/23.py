#  Key Notes:
#
#  1) So that we can add ScanCubes directly to the priority queue, we have to define __lt__ and __eq__ magic methods to allow comparison/sorting.
#  2) Because heapq sorts asc by default, we have to negate bots_in_range and size in the __lt__ method to effect a descending sort on those 2 attributes
#  3) The octree split always splits a larger cube into 8 smaller cubes of equal size - even if the size of the larger cube is not divisible by two.
#     It does this by creating overlapping smaller cubes e.g. one 11x11x11 cube will be split into 8 slightly overlapping 6x6x6 cubes.
#  4) The (x,y,z) coordinates that identify each cube are always (min(x), min(y), min(z)). (x1, y1, z1) == (max(x), max(y), max(z))

from heapq import heapify, heappush, heappop

class Nanobot:

    def __init__(self,radius,coords):

        self.radius, self.c = radius, coords;  self.x, self.y, self.z = coords

    def __str__(self):
        
        return f"Coords: {self.c}, Signal Radius: {self.radius}"


class ScanCube:

    def __init__(self,size,coords,nanobots):

        self.size, self.c = size, coords
        self.x, self.y, self.z = coords
        self.x1, self.y1, self.z1 = (c+size-1 for c in coords)

        self.dist_to_origin = abs(self.x) + abs(self.y) + abs(self.z)

        self.nanobots = nanobots
        self.bots_in_range = sum([1 for bot in self.nanobots if self._manhattan_from_bot_to_cube(bot) <= bot.radius])


    def __str__(self):
        
        return f"Size: {self.size}, Key Coords: {self.c}, Distance Key Coords > Origin: {self.dist_to_origin}, Nanobots in Range: {self.bots_in_range}"


    def __lt__(self, other):

         this = (-self.bots_in_range, -self.size, self.dist_to_origin, self.c)
         compare_to = (-other.bots_in_range, -other.size, other.dist_to_origin, other.c)

         return this < compare_to


    def __eq__(self, other):

         return (self.c, self.size) == (other.c, other.size)


    def _manhattan_from_bot_to_cube(self,bot):

        return (max(self.x-bot.x,0) + max(self.y-bot.y,0) + max(self.z-bot.z,0) +
                max(bot.x-self.x1,0) + max(bot.y-self.y1,0) + max(bot.z-self.z1,0))


    def octree_split(self):

        s,r = self.size//2, self.size%2

        x_vals, y_vals, z_vals = [(n,n+s) for n in self.c]

        return [ScanCube(s+r,(x,y,z),self.nanobots) for x in x_vals for y in y_vals for z in z_vals]


def parse_input(filepath):

    bots = [(d,(a,b,c)) for a,b,c,d in [tuple(map(int,x[5:].replace('>, r=',',').split(','))) for x in open(filepath).read().split('\n')]]

    return [Nanobot(*bot) for bot in sorted(bots)]


def nanobots_in_range_of_other_nanobot(nanobots,from_idx):

    src = nanobots[from_idx] 
    
    return sum([1 for bot in nanobots if sum([abs(src.x-bot.x), abs(src.y-bot.y), abs(src.z-bot.z)]) <= src.radius])


def determine_start_cube(nanobots):

    get = lambda n,func: func([v+(r*func(-1,1)) for r,v in [(bot.radius,bot.c[n]) for bot in nanobots]])

    coords = (get(0,min), get(1,min), get(2,min))
    size = max([get(n,max)-get(n,min)+1 for n in range(3)])

    return ScanCube(size,coords,nanobots)


def coords_with_most_nanobots_in_range(nanobots):

    start_cube = determine_start_cube(nanobots)

    queue = [start_cube]; heapify(queue)

    while queue:

        cube = heappop(queue)

        if cube.size == 1: break        
        else:
            new_cubes = cube.octree_split()
            for cube in new_cubes:
                if cube.bots_in_range > 0 and cube not in queue:
                    heappush(queue,cube)

    return cube.dist_to_origin

    
def main(filepath):
    
    nanobots = parse_input(filepath)
    pt1 = nanobots_in_range_of_other_nanobot(nanobots,-1)
    pt2 = coords_with_most_nanobots_in_range(nanobots)

    return pt1, pt2


print(main('23.txt'))