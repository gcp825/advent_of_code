#  A bit slow for Part 2 (~25 seconds on my laptop) but not egregiously bad given that my AoC metric for
#  'Is it fast enough?' is 'does it complete in the time it takes for me to make a cup of tea?'.
#  It's already set based, so not much more tuning I can do. Might try rewriting the coordinate update
#  to remove the dictionary lookup perhaps? But unless I'm missing a trick can't see how to bring this
#  down significantly.

def parse_grid(filepath):

    grid = [((y,x),val) for y,row in enumerate(open(filepath).read().split('\n')) for x,val in enumerate(row)]
    obstacles = {k for k,v in grid if v == '#'}
    start = [(k,v) for k,v in grid if v in '<>^v'][0]

    return {x[0] for x in grid}, start, obstacles


def map_route(locations, start, obstacles, insert_obstacle=()):

    compass, turn = {'^':(-1,0),'v':(1,0),'<':(0,-1),'>':(0,1)}, {'^':'>', '>':'v', 'v':'<', '<':'^'}

    obstacles = set([insert_obstacle] + [x for x in obstacles]) if insert_obstacle else {x for x in obstacles}
    route = set()
    location, facing = start

    while location in locations:

        if (location, facing) in route:
            break
        else:
            route.add((location, facing))

        y,x = (location[0] + compass[facing][0], location[1] + compass[facing][1])

        if (y,x) in obstacles:
            facing = turn[facing]
        else:
            location = (y,x)

    return [] if (location, facing) in route else list({x[0] for x in route})


def count_loops(locations, start, obstacles, visited):

    loops = 0
    for i, location in enumerate(visited):
        exit_route = map_route(locations, start, obstacles, location)
        if not exit_route:
            loops += 1

    return loops


def main(filepath):

    locations, start, obstacles = parse_grid(filepath)
    visited = map_route(locations, start, obstacles)
    loops = count_loops(locations, start, obstacles, visited)

    return len(visited), loops

print(main('06.txt'))