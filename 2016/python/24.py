#  Another BFS... but at least this one was a challenge. Got my stars using a solution that was another retread of the OOP BFS search I'd used for 3 or 4
#  of the 2016 puzzles... but the performance fell off a cliff with the size of this maze compared to the previous puzzles, so I was waiting for a while! 
#  Subsequently had a look at the reddit megathread for some inspiration, picked apart a couple of other solutions and ultimately rewrote this using a
#  basic recursion approach, which is soooo much quicker it's insane. 

from itertools import permutations
from copy import deepcopy

def read_file(filepath):
    
    locations = []
    maze = [list(x) for x in open(filepath,'r').read().split('\n')]
    
    for row, r in enumerate(maze):
        for col, location in enumerate(r):
            if location.isnumeric():
                locations += [(int(location),(row,col))]
 
    return maze, [x for x,_ in sorted(locations)], [y for _,y in sorted(locations)]


def get_distances(maze,locations):
    
    distances = {} 
    for origin in range(len(locations)-1):
        for destination in range(origin+1,len(locations)):
            distances[(origin,destination)] = move(deepcopy(maze), locations[origin], locations[destination])            
            
    return distances


def move(maze,origins,destination,steps=0):
    
    found = False;  move_queue = set();  steps += 1
    
    if type(origins) == tuple: origins = [origins] 
    
    for coordinates in origins:
        
        if not found:
            
            y,x = coordinates
            maze[y][x] = 'x'    #  mark this location as visited

            for y,x in [(y-1,x),(y,x+1),(y+1,x),(y,x-1)]:
            
                if (y,x) == destination:  found = True;  break
            
                if maze[y][x] == '.':
                    move_queue.update([(y,x)])
                    
    if found:
        return steps
    else:
        return move(maze,list(move_queue),destination,steps)  #  recursively execute next moves if destination not found


def shortest_path(paths,distances):

    journeys = []
    for path in paths:
        distance = 0
        for leg in [tuple(sorted(path[i:i+2])) for i in range(len(path)-1)]: 
            distance += distances[leg]
        journeys += [(distance,'>'.join(list(map(str,path))))]
        
    return min(journeys)
        

def main(filepath):
    
    maze, destinations, locations = read_file(filepath)
    paths = [[0] + list(p) for p in permutations(destinations[1:])]    
    distances = get_distances(maze,locations)
    
    pt1 = shortest_path(paths,distances)    
    paths = [path + [0] for path in paths]
    pt2 = shortest_path(paths,distances)

    return pt1, pt2

print(main('24.txt'))
