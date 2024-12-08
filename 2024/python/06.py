#  Tuned this down to ~9 seconds on my weak old laptop. For something doing this amount of work every choice
#  e.g. object types, whether to use ifs or dictionary/set lookups, whether to use a comprehension etc makes a
#  noticeable difference to the runtime. Only starting the route mapping for Part 2 immediately before the
#  obstruction shaved about 8 seconds off the run time.

def parse_grid(filepath):

    grid = [((y,x),val) for y,row in enumerate(open(filepath).read().split('\n')) for x,val in enumerate(row)]
    obstacles = {k for k,v in grid if v == '#'}
    start = [(k,v) for k,v in grid if v in '<>^v'][0]

    return obstacles, start, max(grid)[0]


def map_route(obstacles, current_location, facing, bounds, part_1=False):

    visit, route = ([],[]) if part_1 else ([],set())
    turn = {'^':'>', '>':'v', 'v':'<', '<':'^'}

    while (0 <= current_location[0] <= bounds[0]) and (0 <= current_location[1] <= bounds[1]):

        if (current_location, facing) in route:
            return 1
        else:
            if part_1:
                visit.append(sum(route.count(x) for x in [(current_location,f) for f in '<>^v'])+1)
                route.append((current_location, facing))
            else:
                route.add((current_location, facing))

        y = current_location[0] + (1 if facing == 'v' else -1 if facing == '^' else 0)
        x = current_location[1] + (1 if facing == '>' else -1 if facing == '<' else 0)

        if (y,x) in obstacles:
            facing = turn[facing]
        else:
            current_location = (y,x)

    return (route, visit) if part_1 else 0


def main(filepath):

    obstacles, start, bounds = parse_grid(filepath)
    route, visit = map_route(obstacles, *start, bounds, True)

    obstructions = [(o,s) for o,s,v in zip([x[0] for x in route][1:], route, visit[1:]) if v == 1]
    loops = sum(map_route(obstacles|{obstruction}, *start, bounds) for obstruction, start in obstructions)

    return len({x[0] for x in route}), loops


print(main('06.txt'))