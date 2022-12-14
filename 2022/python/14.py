#  Hastily combined both parts into a single piece of code, but it feels a bit messy - needs a tidy up for code clarity
#  There may also be a performance tweak I can make to instantly drop a grain of sand as far as it can go vertically in one hit
#  rather than evaluating each step individually - this may or may not be worthwhile depending on the actual layout of the grid.

def setup_grid(filepath):

    rocks = [[tuple(map(int,x.split(',')))[::-1] for x in y] for y in [z.split(' -> ') for z in open(filepath).read().split('\n')]]
    grid  = {(0,500):'+'}

    for rock in rocks:

        for i in range(len(rock)-1):
            
            y,x = rock[i];  yy,xx = rock[i+1]

            grid[(y,x)] = '#'

            while (y,x) != (yy,xx):

                y -= (y-yy)//(abs(y-yy) or 1)
                x -= (x-xx)//(abs(x-xx) or 1)

                grid[(y,x)] = '#'

    return grid, max(grid)[0]+1


def main(filepath,part1=True):

    grid, abyss = setup_grid(filepath)

    origin = (0,500)
    
    while ((part1 and max(grid.keys())[0] < abyss)
       or (not part1 and [location for location in [(1,499),(1,500),(1,501)] if grid.get(location,'.') == '.'])):

        y,x = origin

        while True:

            move = [location for location in [(y+1,x),(y+1,x-1),(y+1,x+1)] if grid.get(location,'.') == '.'][:1]

            if move and y < abyss:
                y,x = move[0]
            else:
                grid[(y,x)] = 'o'
                break

    sand = sum([1 for v in grid.values() if v == 'o'])

    return sand-1 if part1 else sand+1

    
print((main('14.txt'),main('14.txt',False)))