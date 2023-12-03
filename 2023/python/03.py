#  The code for these grid coordinate puzzles always ends up looking horrible. Too many different x and y variables 
#  and you can't call them anything else because they are literally references to x and y axes.

def get_parts_and_gears(grid):

    parts = [];  possible_gears = dict();  max_y = len(grid)-1;  max_x = len(grid[0])-1

    for y in range(max_y+1):

        x = 0
        while x <= max_x:

            if not grid[y][x].isdigit(): x += 1
            else:
                x, coords = get_number_coords(grid,y,x,max_x)
                adjacent_symbols = get_symbols(grid,*coords,max_y,max_x)

                if adjacent_symbols:
                    parts += [int(grid[coords[0]][coords[1]:coords[2]+1])]
                    for coords in [c for s,c in adjacent_symbols if s == '*']:
                        possible_gears[coords] = possible_gears.get(coords,[]) + parts[-1:]

    return parts, [p for p in possible_gears.values() if len(p) == 2]


def get_number_coords(grid,y,x1,max_x):

    x2 = x1
    while x2 <= max_x and grid[y][x2].isdigit(): x2 += 1

    return x2, (y,x1,x2-1)
    

def adjacent_coords(y,x1,x2):

    return [(yy,xx) for yy in range(y-1,y+2) for xx in range(x1-1,x2+2) if (yy,xx) not in [(y,x) for x in range(x1,x2+1)]]


def get_symbols(grid,y,x1,x2,max_y,max_x):

    coords = [(yy,xx) for yy,xx in adjacent_coords(y,x1,x2) if 0 <= yy <= max_y and 0 <= xx <= max_x]
    
    return [(s,c) for s,c in [(grid[yy][xx], (yy,xx)) for yy,xx in coords] if s != '.' and not s.isdigit()]


def main(filepath):

    grid = open(filepath).read().split('\n')
    parts, gears = get_parts_and_gears(grid)

    return sum(parts), sum([g[0]*g[1] for g in gears])

print(main('03.txt'))