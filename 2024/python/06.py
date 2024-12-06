#  Tuned this down to ~16 seconds on my weak old laptop. For something doing this amount of work every choice
#  e.g. object types, whether to use ifs or dictionary/set lookups, whether to use a comprehension etc makes a
#  noticeable difference to the runtime.

def parse_grid(filepath):

    grid = [((y,x),val) for y,row in enumerate(open(filepath).read().split('\n')) for x,val in enumerate(row)]
    obstacles = {k for k,v in grid if v == '#'}
    start = [(k,v) for k,v in grid if v in '<>^v'][0]

    return obstacles, start, max(grid)[0]


def map_route(obstacles, current_location, facing, bounds, part_1=False):

    route = set()
    turn = {'^':'>', '>':'v', 'v':'<', '<':'^'}

    while (0 <= current_location[0] <= bounds[0]) and (0 <= current_location[1] <= bounds[1]):

        if (current_location, facing) in route:
            return 1
        else:
            route.add((current_location, facing))

        y = current_location[0] + (1 if facing == 'v' else -1 if facing == '^' else 0)
        x = current_location[1] + (1 if facing == '>' else -1 if facing == '<' else 0)

        if (y,x) in obstacles:
            facing = turn[facing]
        else:
            current_location = (y,x)

    return {x[0] for x in route} if part_1 else 0


def main(filepath):

    obstacles, start, bounds = parse_grid(filepath)
    visited = map_route(obstacles, *start, bounds, True)
    loops = sum(map_route(obstacles|{location}, *start, bounds) for location in visited)

    return len(visited), loops

print(main('06.txt'))