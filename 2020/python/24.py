# It's just Day 17 with two fewer dimensions and some hexagons. Ho hum.

from itertools import product

def read_file(filepath):
    
    with open(filepath,'r') as f:
        
        compass = {'w':(-2,0),'e':(2,0),'nw':(-1,-1),'ne':(1,-1),'sw':(-1,1),'se':(1,1)}
        
        paths = []
        for x in f.read().split('\n'):
            i = 0; path = []
            while i < len(x):
                d = x[i] if x[i] in 'we' else x[i:i+2]
                path += [compass[d]]
                i += len(d)
            paths += [path]
                
    return paths


def starting_configuration(paths):
    
    floor = {}
    for path in paths:
        tile = (0,0)
        for step in path:
            tile = tuple(map(sum,zip(tile,step)))
        floor[tile] = (floor.get(tile,0) + 1) % 2                         # flips 0 to 1 (white to black) and vice versa

    return floor, sum(floor.values())

        
def cycle(floor):
    
    next_state = {} 
    xr = range(min([x for x,y in floor.keys()])-2,max([x for x,y in floor.keys()])+4)
    yr = range(min([y for x,y in floor.keys()])-2,max([y for x,y in floor.keys()])+4)

    for y in yr:
        for x in xr:
            current_tile = floor.get((x,y),0)
            adjacent = [] + [t for t in product((x-1,x+1),(y-1,y+1))] + [(x-2,y),(x+2,y)]
            black_tiles = len([t for t in adjacent if floor.get(t,0) == 1])
            
            if ((current_tile == 1 and black_tiles in (1,2))              #  stays black
            or  (current_tile == 0 and black_tiles == 2)):                #  flips white to black
                next_state[(x,y)] = 1
                
    return next_state
                

def cycle_floor(floor,cycles):
    
    for _ in range(cycles):
        floor = cycle(floor)
        
    return sum(floor.values())
    
           
def main(filepath,cycles=100):
    
     paths = read_file(filepath)
     floor, pt1 = starting_configuration(paths)
     pt2 = cycle_floor(floor,cycles)
    
     return pt1, pt2
         
print(main('24.txt'))
