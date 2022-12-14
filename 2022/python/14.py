#  This is a bit tidier than my original code. Still need to come up with a slicker way of parsing the input and creating the grid.
#  Also need to look at implementing each vertical drop as a single move rather than a step by step iteration.

def setup_grid(filepath):

    rocks = [[tuple(map(int,x.split(',')))[::-1] for x in y] for y in [z.split(' -> ') for z in open(filepath).read().split('\n')]]
    grid  = {(0,500):'.'}

    for rock in rocks:

        for i in range(len(rock)-1):
            
            y,x = rock[i];  yy,xx = rock[i+1]

            grid[(y,x)] = '#'

            while (y,x) != (yy,xx):

                y -= (y-yy)//(abs(y-yy) or 1)
                x -= (x-xx)//(abs(x-xx) or 1)

                grid[(y,x)] = '#'

    return grid


def main(filepath,part2=False):

    grid = setup_grid(filepath)

    abyss = max(grid)[0]+1;  floor = abyss+1;  y = abyss-1;  origin = [k for k,v in grid.items() if v == '.'][0]; 

    while (not part2 and y < abyss) or (part2 and grid[origin] == '.'):

        y,x = origin

        while True:

            move = [coords for coords in [(y+1,x),(y+1,x-1),(y+1,x+1)] if grid.get(coords,'.') == '.' and (y+1) < floor][:1]

            if move: y,x = move[0]
            else:
                grid[(y,x)] = 'o' if part2 or y < abyss else '.'
                break

    return sum([1 for v in grid.values() if v == 'o'])

    
print((main('14.txt'),main('14.txt',True)))