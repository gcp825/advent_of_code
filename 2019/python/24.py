from itertools import chain

def setup_grid(f):  return [list(x.replace('.','0').replace('#','1')) for x in open(f,'r').read().split('\n')]

def get_config(grid):  return int(''.join([x for x in [''.join(x) for x in grid]]),2)

def cycle_grid(grid,above=[],below=[]):
  
    new_grid = []
    for y,row in enumerate(grid):

        new_row = []
        for x,loc in enumerate(row):

            adjacent = [(b,a) for b,a in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)] if 0 <= a < len(row) and 0 <= b < len(grid)]
            bug_ct = len([z for z in [grid[b][a] for b,a in adjacent] if z == '1'])

            if loc != '?' and len(above)+len(below) > 0:
                bug_ct += get_recursive_bug_ct(y,x,grid,above,below)

            if   loc == '1' and bug_ct != 1:     new_row += ['0']
            elif loc == '0' and bug_ct in (1,2): new_row += ['1']
            else:                                new_row += [loc]

        new_grid += [new_row]

    return new_grid

def get_recursive_bug_ct(y,x,grid,above,below): 
    
    adjacent = []

    if len(above) > 0:

        a,b = (len(above[0])//2,len(above)//2)
        top, bottom, left, right = (0,len(above)-1,0,len(above[0])-1)  

        if y == top:    adjacent += [above[b-1][a]]
        if y == bottom: adjacent += [above[b+1][a]]
        if x == left:   adjacent += [above[b][a-1]]
        if x == right:  adjacent += [above[b][a+1]]

    if len(below) > 0:

        a,b = (len(grid[0])-1,len(grid)-1)
        top, bottom = (grid[y-1][x] if y > 0 else '0', grid[y+1][x] if y < b else '0')
        left, right = (grid[y][x-1] if x > 0 else '0', grid[y][x+1] if x < a else '0')

        if '?' == top:    adjacent += below[b]  
        if '?' == bottom: adjacent += below[0]
        if '?' == left:   adjacent += [row[a] for row in below]
        if '?' == right:  adjacent += [row[0] for row in below]

    return len([z for z in adjacent if z == '1'])

def part1(grid):
    
    seen = set();  seen.add(get_config(grid))

    while True:   
        grid = cycle_grid(grid)    
        configuration = get_config(grid)

        if configuration in seen: break
        else: 
            seen.add(configuration)

    return sum([(2**i)*int(x) for i,x in enumerate(list(bin(configuration)[2:].zfill(len(grid)*len(grid[0]))))])

def part2(grid):

    y,x,n = len(grid)//2, len(grid[0])//2, len(grid[0]) 
    base_level = [list('0'*n) for _ in range(n)];  base_level[y][x] = '?';  grid[y][x] = '?'
    levels = [base_level,grid,base_level]

    for _ in range(200):   
        new_levels = [];  above = []
        for i,level in enumerate(levels):
            below = levels[i+1] if i < len(levels)-1 else []
            new_levels += [cycle_grid(level,above,below)]
            above = level
        levels = [base_level] + new_levels + [base_level]

    return ''.join([''.join(list(chain(*grid))) for grid in levels]).count('1')

def main(f):
    
    grid = setup_grid(f)
    
    return part1(grid), part2(grid)
    
print(main('24.txt'))
