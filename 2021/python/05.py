#  There was a big enough clue in Part 1 that I gambled on building a solution for that which would give me the imagined Part 2 answer as well.
#  And it did... otherwise the Vent class and it's mapping function may have been slightly wasted.

from collections import Counter
from itertools   import chain

class Vent:

    def __init__(self,start,end): 

        self.startpos, self.endpos, self.coords = (start, end, [])
        self.map()
        
    def __str__(self):
        return f"startpos: {self.startpos}, endpos: {self.endpos}, coords: {self.coords}"

    def map(self):

        x,y = self.startpos;  xx, yy = self.endpos

        self.coords += [(x,y)]
        while self.coords[-1] != self.endpos:
            x = x+1 if x < xx else x-1 if x > xx else x
            y = y+1 if y < yy else y-1 if y > yy else y
            self.coords += [(x,y)]

def main(filepath):

    coords  = [((x[0],x[1]),(x[2],x[3])) for x in [list(map(int,x.replace(' -> ',',').split(','))) for x in open(filepath,'r').read().split('\n')]]
    vents   = [Vent(*c) for c in coords]

    vent_map_pt1 = Counter(list(chain(*[v.coords for v in vents if 1 in [v.startpos[x]/v.endpos[x] for x in (0,1)]])))
    vent_map_pt2 = Counter(list(chain(*[v.coords for v in vents])))

    return len([v for v in vent_map_pt1.values() if v > 1]), len([v for v in vent_map_pt2.values() if v > 1])

print(main('05.txt'))