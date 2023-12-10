#  This feels like a bit of a mess. Thats probably partly because I chose a list structure rather than a dict - I've
#  had random performance issues using dicts for this type of puzzle before; partly because of all the corresponding
#  coordinates; partly because there are probably slicker ways to expand and flood the grid, and partly due to how I
#  chose to represent the pipes
#
#  Feels like a grid class would really help to tidy this up no end - when I get a chance, I'll refactor this... but
#  right now, this will have to stay as the initial version that got the stars.

def prepare_grid(filepath):

    repl = dict(zip(('|','-','L','J','7','F'), ('ns','we','ne','nw','sw','se')))
    grid = [[repl.get(x,x) for x in list(y)] for y in open(filepath).read().split('\n')]

    rules = (len(grid)-1, len(grid[0])-1, dict(zip('nswe','snew')))
    y,x   = [(y,x) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == 'S'][0]

    start_pipe = ''.join(['nswe'[i] for i,v in enumerate([valid_pipe(grid,rules,y,x,d) for d in 'nswe']) if v])
    grid[y][x] = start_pipe

    return clean_grid(grid,rules), (y,x)


def valid_pipe(grid,rules,y,x,d):

    max_y, max_x, opposite = rules

    dir = grid[y][x][d] if type(d) is int else d
    opp = opposite[dir]
    
    y += 0 if dir in 'ew' else 1 if dir == 's' else -1
    x += 0 if dir in 'ns' else 1 if dir == 'e' else -1

    return True if 0 <= y <= max_y and 0 <= x <= max_x and opp in grid[y][x] else False


def clean_grid(grid,rules):

    indices = [(y,x,d) for y in range(len(grid)) for x in range(len(grid[0])) for d in (0,1)]
    changes = 1

    while changes:
        changes = 0
        for y,x,d in indices:
            if grid[y][x] != '.':
                if not valid_pipe(grid,rules,y,x,d):
                    changes += 1
                    grid[y][x] = '.'
    return grid


def move(y,x,d):

    return {'n':(y-1,x),'e':(y,x+1),'s':(y+1,x),'w':(y,x-1)}[d]


def get_distances(grid,y,x):

    r0,r1 = [move(y,x,grid[y][x][i]) for i in (0,1)]
    routes = [(y,x,*r0),(y,x,*r1)]

    distances = dict([((y,x),0), (r0,1), (r1,1)])
    visited, steps = (0,1)

    while len(distances) > visited:
        visited = len(distances)
        steps += 1
        for i, (py, px, cy, cx) in enumerate(routes):
            y,x = [(y,x) for y,x in [move(cy,cx,d) for d in grid[cy][cx]] if (y,x) != (py,px)][0]
            distances[(y,x)] = min(steps,distances.get((y,x),99**99))
            routes[i] = (cy,cx,y,x)

    return max(distances.values())


def expand(grid):

    new_grid = []

    for row in grid:

        new_row = []
        for col in row:
            new_row += [col, 'we' if col in ('se','ne','we') else '.']
        new_grid += [new_row]

        new_row = []
        for col in row:
            new_row += ['ns' if col in ('se','sw','ns') else '.', '.']
        new_grid += [new_row]

    return new_grid


def flood(grid):

    grid = [] + grid
    queue = [(y,x) for y, row in enumerate(grid) for x, col in enumerate(row) if col == '.'][:1]
    visited = set()

    while queue:
        y,x = queue.pop(0)

        grid[y][x] = 'X'
        visited.add((y,x))

        adjacent = [(y-1,x),(y,x+1),(y+1,x),(y,x-1)]
        queue += [(y,x) for y,x in adjacent if (y,x) not in queue and (y,x) not in visited and grid[y][x] == '.']

    return grid


def get_inside_locations(grid):

    expanded_grid = flood(expand(grid))

    was_empty = [(y,x) for y,row in enumerate(grid) for x,col in enumerate(row) if col == '.']
    still_empty = [(y,x) for y,x in was_empty if expanded_grid[y*2][x*2] == '.']

    return len(still_empty)


def main(filepath):

    grid, start = prepare_grid(filepath)
    pt1 = get_distances(grid,*start)
    pt2 = get_inside_locations(grid)

    return pt1, pt2


print(main('10.txt'))