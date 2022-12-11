#  One step at a time recursive BFS with updating map and heuristic pruning. Part 2 implemented as single robot that can teleport between
#  submazes (to last known location in each) upon retrieving a key. Part 2 pretty much negates the heuristic, so this is a little slow.
#  However, due to the optional states of doors this seemed a more trivial(!) and foolproof approach than calculating the optimal
#  distance between keys and then trying to work out what point-to-point routes are valid based upon open doors. Still have at least one 
#  more tuning idea (tunnel/fast-forward optimisation) yet to implement but this approach will always be slower than point to point.
#  Part 2 requires presentation of submazes in a single file, as seperate mazes atop each other, seperated by a blank line.

from copy import deepcopy
from time import time

def read_maze(f):

    maze  = [list(x.replace('.',' ')) for x in open(f,'r').read().split('\n')]
    keys  = dict([(key,(y,x)) for y,row in enumerate(maze) for x,key in enumerate(row) if key.isalpha() and key.islower()])
    doors = dict([(door,(y,x)) for y,row in enumerate(maze) for x,door in enumerate(row) if door.isalpha() and door.isupper()])
    start = [(y,x) for y,row in enumerate(maze) for x,location in enumerate(row) if location == '@']
    for s in start: 
         maze[s[0]][s[1]] = ' '

    mazes = [];  m = []
    for row in maze:
        if len(row) >  0: m += [row] 
        if len(row) == 0: mazes += [m];  m = []
    mazes += [m]

    subkeys =  [list(sorted([key for y,row in enumerate(m) for x,key in enumerate(row) if key.isalpha() and key.islower()])) for m in mazes]   
    submazes = [(start[i], subkeys[i], keys) for i in range(len(mazes))] 

    return (maze, keys, doors, submazes)


def coordinate_search(master_maze,keys,doors,start,best_known,submazes):

    start_time = time()
    on = False
    steps = 0;  extended_routes = [];  found_keys = '' 

    routes = [(steps,found_keys,start)]

    for n in range(len(keys)):
                                                                                                      
        print_progress(2,n+1,len(keys),len(routes))

        for route in routes:
            maze, targets = configure_maze(master_maze,keys,doors,start,list(route[1]))
            extended_routes += recursive_bfs(maze,targets,[route],[],submazes)

        if n < len(keys)-1:
            routes = discard_routes(extended_routes,submazes,best_known)
            routes, on = discard_heuristically(routes,submazes,on)
            extended_routes = []
            if len(routes) == 0: break
        else:
            routes = extended_routes

    if len(routes) > 0: 
        print_progress(3,start_time,min(routes)[0])
        return routes
    else:
        print_progress(4)
        return [None]


def configure_maze(master_maze,keys,doors,start,found_keys): 

    maze = deepcopy(master_maze)                                                                   
    for y,x in [coords for d,coords in doors.items() if d.lower() in found_keys]:  maze[y][x] = ' '   #  remove unlocked doors
    for y,x in [coords for k,coords in keys.items() if k in found_keys]:           maze[y][x] = ' '   #  remove found keys
    targets = [k for k in keys.keys() if k not in found_keys]

    return maze, targets


def print_progress(msg,*args):

    if msg == 1:  p = 'Starting search in maze ' + str(args[0]) + '...'
    if msg == 2:  p = 'Searching for key ' + str(args[0]) + ' of ' + str(args[1]) + ' in ' + str(args[2]) + ' active permutations...'
    if msg == 3:  p = 'All keys found in ' + str(time()-args[0])[:6] + ' seconds. Shortest path found: ' + str(args[1]) + ' steps.'
    if msg == 4:  p = 'No valid permutations left to investigate. Terminating...'
    print(p)


def recursive_bfs(maze,targets,routes,completed_routes,submazes):

    next_routes = []

    for steps, found_keys, coordinates in routes:

        y,x = coordinates
        next_moves = [(y-1,x),(y,x+1),(y+1,x),(y,x-1)]
        maze[y][x] = '.'                                                          #  Lay breadcrumb to show this location already visited

        for y,x in next_moves:

            if maze[y][x] == ' ':                                  
                next_routes += [(steps+1,found_keys,(y,x))]                       #  Any non available location (wall, door, already visited)
                                                                                  #  pruned implicitly by this if/elif
            elif maze[y][x] in targets:
                complete_route = (steps+1, found_keys + maze[y][x], (y,x))
                if len(submazes) <= 1:
                    completed_routes += [complete_route]
                else:
                    completed_routes += multimaze_routes(complete_route,submazes)

    if len(next_routes) == 0:                                                     #  No more routes to follow: return completed routes (i.e. key found) only...
        return completed_routes
    else:         
        return recursive_bfs(maze,targets,next_routes,completed_routes,submazes)  #  Else recurse again if more routes to follow...


def multimaze_routes(route,submazes):

    all_routes = [];  all_keys = submazes[0][2]
    steps, found_keys, _ = route  

    if len(found_keys) == len(all_keys):
        all_routes = [route]                                                      #  All keys found - no multimaze route expansion needed
    else:
        for start, sub_keys, _ in submazes:
            found = [key for key in list(found_keys[::-1]) if key in sub_keys]    #  Ascertain keys already found in the submaze under consideration
            if len(found) < len(sub_keys):                                        #  If still keys to retrieve in that submaze, add a teleport route starting
                if len(found) == 0:                                               #  at the last location visited in that submaze (or the entrance otherwise)
                    all_routes += [(steps,found_keys,start)]
                else:
                    all_routes += [(steps,found_keys,all_keys[found[0]])]

    return all_routes    


def discard_routes(routes,submazes,best_known):

    ranked_routes = [];  seen_states = set()
    for route in sorted(routes):
        steps, found_keys, coords = route
        if best_known > 0 and steps >= best_known:                                #  Discard routes known to be suboptimal against a known solution
            break
        else:
            fk = ''.join(sorted(found_keys)) + '-'
            state_id = fk + str(coords) + get_state(found_keys,submazes)          #  Keep only the shortest of each routes to have collected the same keys and ended up
            if state_id not in seen_states:                                       #  at the same location e.g abcdef and acbedf have achieved the same output but in a
                seen_states.add(state_id)                                         #  different order and potentially different number of steps... routes with more steps
                ranked_routes += [route]                                          #  by definition can not be the optimal route

    return ranked_routes


def get_state(found_keys,submazes):

    state = ''
    if len(submazes) <= 1: return state
    for start, sub_keys, all_keys in submazes:
        found = [key for key in list(found_keys[::-1]) if key in sub_keys]   
        state += str(all_keys[found[0]]) if len(found) > 0 else str(start) 
    return '-' + state.replace(' ','')


def discard_heuristically(routes,submazes,on=False,threshold=100):

    if len(routes) == 0:  return routes, on
    else:

        limit = threshold * max(1,(len(submazes)**2))                       #  Once routes to explore >= 100 (single maze) or calculated limit (> 1 maze)
        if limit > 0 and len(routes) > limit:  on = True                    #  switch on heuristic route pruning 

        lo, cutoff = routes[0][0], routes[-1][0]
        if on and len(routes) > (limit//3)*2:                               #  Once heuristics on, only apply if no. of routes > 2/3rds of the threshold used to switch on       
            cutoff = min(lo + ((cutoff-lo)//2),lo*2)                        #  Cutoff for pruning is the lower of the median route length and double the minimum route length

        return [r for r in routes if r[0] <= cutoff], on


def main(f):
    
    maze, keys, doors, submazes = read_maze(f)
    best_routes = [];  best_known = 0

    for i in range(len(submazes)):
        print_progress(1,i+1)
        start  = submazes[i][0]
        best_routes += coordinate_search(maze,keys,doors,start,best_known,submazes)
        best_routes = list(sorted([x for x in best_routes if x is not None]))
        best_known = best_routes[0][0] if len(best_routes) > 0 else 0
        if best_known > 0: break

    return best_known

print(main('18.txt'))
print(main('18pt2.txt'))
