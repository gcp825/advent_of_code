# Pretty standard non-recursive BFS. Not much else to add other than I made a meal of it, because it was far too early and I wasn't thinking straight yet.

from functools import reduce

def main(filepath):
    
    heightmap = dict([((x,y),z) for y,row in enumerate([list(map(int,list(x))) for x in open(filepath,'r').read().split('\n')]) for x,z in enumerate(row)])   
    map_size  = tuple(map(sum,zip(max(heightmap),(1,1))))       
    compass   = {'n':(0,-1),'s':(0,1),'e':(1,0),'w':(-1,0)}
    basins    = []

    adjacent_height = lambda x,y: heightmap.get(tuple(map(sum,zip(x,compass[y]))),9)
    adjacent_coords = lambda x,y: [tuple(map(sum,zip((x,y),compass[d]))) for d in 'nesw']

    lows = [((x,y),heightmap[(x,y)]) for y in range(map_size[1]) for x in range(map_size[0]) 
                if len([z for z in [adjacent_height((x,y),d) for d in 'nesw'] if z <= heightmap[(x,y)]]) == 0]

    for coords, _ in lows:

        queue = [coords]; basin = set([coords])

        while len(queue) > 0:
           
            a,b = queue.pop(0)
            height = heightmap.get((a,b),9)

            for x,y in adjacent_coords(a,b):

                if (x,y) not in basin and height <= heightmap.get((x,y),9) < 9:
                    queue += [(x,y)]
                    basin.add((x,y))

        basins += [len(basin)]   

    return sum([y+1 for x,y in lows]), reduce(lambda x,y: x*y, sorted(basins)[-3:])
    
print(main('09.txt'))