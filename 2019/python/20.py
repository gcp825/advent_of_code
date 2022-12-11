#  Works out portal to portal distances, then calculates shortest total journey distance for all permutations, pruning suboptimal permutations
#  as soon as possible. Same approach for Part 2, except with additional analysis of route path to limit to just those permutations that end back
#  on level zero and slight logic amendment to allow for repeated portals.

from copy import deepcopy

def setup_maze(f):

    maze  = [x for x in open(f,'r').read().split('\n')]  
    width, length = max([len(x) for x in maze]), len(maze)
    rotated = [''.join([row[i] for row in [x[::-1] for x in maze]]) for i in range(width)]
    
    portals = get_portals(maze,(1,width-1)) + get_portals(rotated,(1,length-1),True)

    maze = [list(x.replace(' ','#').replace('.', ' ')) for x in maze]
    for y,x in [coords for portals,coords in portals]: maze[y][x] = '?'

    return maze, dict(portals)


def get_portals(maze,outer,rotated=False):

    portals = []
    for y,x,case in [(y,x,str.upper if x in outer else str.lower) for y in range(len(maze)) for x in range(outer[0],outer[1]+1)]:
        if maze[y][x-1:x+1].isalpha():
            if x != outer[0] and maze[y][x-2:x-1] == '.':  portals += [(case(maze[y][x-1:x+1]),(y,x-2))]
            if x != outer[1] and maze[y][x+1:x+2] == '.':  portals += [(case(maze[y][x-1:x+1]),(y,x+1))] 
    return [(p,(c[1],len(maze)-c[0]-1)) for p,c in portals] if rotated else portals 


def get_distances(maze,portals):

    subroutes = {};  distances = {};  reverse_portals = dict([(v,k) for k,v in portals.items()])
    for origin, coords in sorted(portals.items()):
        destinations = set()
        paths = recursive_bfs(deepcopy(maze),reverse_portals,[(*coords,0)],[])
        for dest, steps in paths:
            destinations.add(dest)
            distances[origin+dest] = steps
        partner = origin.lower() if origin.isupper() else origin.upper()
        if partner in portals: 
            destinations.add(partner)
            distances[origin+partner] = 1
        subroutes[origin] = list(destinations)

    return subroutes, distances


def recursive_bfs(maze,portals,routes,found):

    next_routes = []
    for yy,xx,steps in routes:

        maze[yy][xx] = '.'                                                        
        for y,x in [(yy-1,xx),(yy,xx+1),(yy+1,xx),(yy,xx-1)]:

            if   maze[y][x] == ' ':  next_routes += [(y,x,steps+1)]                                   
            elif maze[y][x] == '?':  found += [(portals[(y,x)],steps+1)]

    return found if len(next_routes) == 0 else recursive_bfs(maze,portals,next_routes,found)
  

def shortest_journey(subroutes,distances,start,end,recursive=False):

    routes = [(0,[start])];  shortest_steps = 2**31-1;  best_route = []
    max_levels = len([x for x in subroutes.keys() if x.islower()]) if recursive else 1

    while len(routes) > 0:
        next_routes = []

        for steps, route in routes:

            next_steps = get_next_steps(route,subroutes,recursive)

            for portal in next_steps:
                incremented_steps = steps + distances[route[-1]+portal]

                if incremented_steps < shortest_steps:
                    new_route = [] + route + [portal]
                    level = get_level(new_route,end) if recursive else 0

                    if 0 <= level <= max_levels:
                        if portal == end:                            
                            if level == 0:  shortest_steps, best_route = incremented_steps, new_route
                        else:
                            next_routes += [(incremented_steps, new_route)]

        routes = next_routes

    return (shortest_steps, '>'.join(best_route)) 
      

def get_next_steps(route,subroutes,recursive):

    last = route[-1]
    if recursive:
        if len(route) >= 2 and route[-2].upper() != last.upper():  return [portal for portal in subroutes[last] if portal.upper() == last.upper()]
        else:                                                      return [portal for portal in subroutes[last] if portal.upper() != last.upper()]
    else:                                                          return [portal for portal in subroutes[last] if portal not in route]


def get_level(route,end):

    level = 0;  prev = route[0]
    for portal in route[1:]:
        level += 0 if portal.upper() == prev else 0 if portal == end else 1 if portal.islower() else -1
        prev = portal.upper()
        if level < 0: break
    return level 


def main(f):

    maze, portals = setup_maze(f)
    subroutes, distances = get_distances(maze,portals)
    shortest_pt1 = shortest_journey(subroutes,distances,'AA','ZZ')
    shortest_pt2 = shortest_journey(subroutes,distances,'AA','ZZ',True)

    return shortest_pt1[0], shortest_pt2[0]

print(main('20.txt'))
