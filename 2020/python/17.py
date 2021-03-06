#  Initially tried adapting my slow Day 11 string maniuplation approach to this one... and then gave up on that when it became obvious it wouldn't scale
#  (plus I just kept tying myself in knots trying to avoid mashing nested lists together).
#  Changed to a dict solution (actually my first thought on Day 11 that I then abandoned) and discovered itertools.product which made this a lot slicker
#  for calculating all of the adjacent cubes. Couldn't be bothered trying to refactor the 3d and 4d cycle functions into a single function.

from itertools import product

def read_file(filepath,mode):
    
    with open(filepath,'r') as f:
        
        cubes = {}
        for z, zv in enumerate([[list(x) for x in [x for x in f.read().split('\n')]]]):
            for y, yv in enumerate(zv):
                for x, xv in enumerate(yv):
                    if xv == '#':
                        if mode == 3: cubes[(z,y,x)] = xv
                        else:         cubes[(z,y,x,0)] = xv
                
    return cubes

def three_d_cycle(cubes):
    
    next_state = {}
    xr = range(min([x for z,y,x in cubes.keys()])-1,max([x for z,y,x in cubes.keys()])+2)   #  expand each axis by 1 at each boundary
    yr = range(min([y for z,y,x in cubes.keys()])-1,max([y for z,y,x in cubes.keys()])+2)   #  (two total) each cycle
    zr = range(min([z for z,y,x in cubes.keys()])-1,max([z for z,y,x in cubes.keys()])+2)

    for z in zr:
        for y in yr:
            for x in xr:
                adjacent = [c for c in product((z-1,z,z+1),(y-1,y,y+1),(x-1,x,x+1)) if c != (z,y,x)]
                active_ct = len([c for c in adjacent if cubes.get(c,'.') == '#'])
                if cubes.get((z,y,x),'.') == '#':
                    if active_ct in (2,3): next_state[(z,y,x)] = '#'
                else:
                    if active_ct == 3: next_state[(z,y,x)] = '#'
        
    return next_state


def four_d_cycle(cubes):
    
    next_state = {}
    wr = range(min([w for z,y,x,w in cubes.keys()])-1,max([w for z,y,x,w in cubes.keys()])+2)   
    xr = range(min([x for z,y,x,w in cubes.keys()])-1,max([x for z,y,x,w in cubes.keys()])+2)   #  expand each axis by 1 at each boundary
    yr = range(min([y for z,y,x,w in cubes.keys()])-1,max([y for z,y,x,w in cubes.keys()])+2)   #  (two total) each cycle
    zr = range(min([z for z,y,x,w in cubes.keys()])-1,max([z for z,y,x,w in cubes.keys()])+2)

    for z in zr:
        for y in yr:
            for x in xr:
                for w in wr:
                    adjacent = [c for c in product((z-1,z,z+1),(y-1,y,y+1),(x-1,x,x+1),(w-1,w,w+1)) if c != (z,y,x,w)]
                    active_ct = len([c for c in adjacent if cubes.get(c,'.') == '#'])
                    if cubes.get((z,y,x,w),'.') == '#':
                        if active_ct in (2,3): next_state[(z,y,x,w)] = '#'
                    else:
                        if active_ct == 3: next_state[(z,y,x,w)] = '#'
        
    return next_state

def boot_process(cubes,cycles):
    
    mode = len(min(cubes.keys()))
    
    for i in range(0,cycles):
        if mode == 3: cubes = three_d_cycle(cubes)
        else:         cubes = four_d_cycle(cubes)
        
    return cubes
    
           
def main(filepath):
    
     pt1 = boot_process(read_file(filepath,3),6)
     pt2 = boot_process(read_file(filepath,4),6)
    
     return len(pt1), len(pt2)
         
print(main('day17.txt'))
