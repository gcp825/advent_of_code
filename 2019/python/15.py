from intcode import IntcodeComputer    # see intcode.py in this repo
from copy import deepcopy

def explore(droid):

    routes = [(deepcopy(droid),0,0)];  maze={(0,0):'.'};  steps, target = (0,0);  running = True

    while running:
        steps, routes, maze, target, running = recursive_bfs(steps,routes,maze,target)

    start = [k for k,v in maze.items() if v == 'O'][0]
    routes = [start];  minutes = 0;  running = True

    while running:
        minutes, routes, maze, running = another_recursive_bfs(minutes, routes, maze)

    return target, minutes


def recursive_bfs(steps,routes,maze,target):

    next_routes = [];  reply = None

    for droid,yy,xx in routes:
        for inp,y,x in [(1,yy-1,xx),(4,yy,xx+1),(2,yy+1,xx),(3,yy,xx-1)]:
            if maze.get((y,x),'?') == '?':
                reply = droid.run(inp)
                if reply == 0:
                    maze[(y,x)] = '#'
                if reply == 1:
                    maze[(y,x)] = '.'
                    next_routes += [(deepcopy(droid),y,x)]
                    droid.reset()
                if reply == 2:
                    maze[(y,x)] = 'O'
                    target = steps+1
    steps += 1

    if len(next_routes) == 0: return steps, next_routes, maze, target, False
    elif steps%500 == 0:      return steps, next_routes, maze, target, True
    else:                     return recursive_bfs(steps,next_routes,maze,target)


def another_recursive_bfs(minutes,routes,maze):

    next_routes = []

    for yy,xx in routes:
        neighbours = [(y,x) for y,x in [(yy-1,xx),(yy,xx+1),(yy+1,xx),(yy,xx-1)] if maze.get((y,x),'?') == '.']
        for y,x in neighbours:
            maze[(y,x)] = 'O'
            next_routes += [(y,x)]

    if len(next_routes) > 0: minutes += 1

    if len(next_routes) == 0:  return minutes, next_routes, maze, False
    elif minutes%500 == 0:     return minutes, next_routes, maze, True
    else:                      return another_recursive_bfs(minutes,next_routes,maze)


def main(f):

    droid = IntcodeComputer(load=f)
    steps, minutes = explore(droid)

    return steps, minutes

print(main('15.txt'))   #  254, 268
