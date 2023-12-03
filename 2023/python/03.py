#  The code for these grid coordinate puzzles always ends up looking horrible. Too many different x and y variables 
#  and you can't call them anything else because they are literally references to x and y axes.

def extract_parts_and_gears(grid):

    parts = [];  gears = dict();  max_y = len(grid)-1;  max_x = len(grid[0])-1;  bounds = (max_y, max_x)

    for y in range(max_y+1):

        x = 0
        while x <= max_x:

            if not grid[y][x].isnumeric(): x += 1
            else:
                x1 = x
                while x <= max_x and grid[y][x].isnumeric(): x += 1

                adjacent_symbols = get_symbols(grid,y,x1,x-1,bounds)

                if adjacent_symbols:
                    new_part = int(grid[y][x1:x])
                    parts += [new_part]
                    for coords in [c for s,c in adjacent_symbols if s == '*']:
                        gears[coords] = gears.get(coords,[]) + [new_part]

    return parts, gears


def adjacent_coords(y,x1,x2):

    return [(yy,xx) for yy in range(y-1,y+2) for xx in range(x1-1,x2+2) if (yy,xx) not in [(y,x) for x in range(x1,x2+1)]]


def get_symbols(grid,y,x1,x2,bounds):

    coords = [(yy,xx) for yy,xx in adjacent_coords(y,x1,x2) if 0 <= yy <= bounds[0] and 0 <= xx <= bounds[1]]
    
    return [(s,c) for s,c in [(grid[yy][xx], (yy,xx)) for yy,xx in coords] if s != '.' and not s.isnumeric()]


def main(filepath):

    grid = [x for x in open(filepath).read().split('\n')]
    parts, gears = extract_parts_and_gears(grid)

    return sum(parts), sum([p[0]*p[1] for p in gears.values() if len(p) == 2])

print(main('03.txt'))