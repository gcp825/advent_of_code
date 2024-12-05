# There's always one puzzle each year where I use list comprehensions for everything (even when I shouldn't) just for practice...

def rotate_45(grid):

    row_starts = [(y,0) for y in range(len(grid))] + [(len(grid)-1,x) for x in range(1,len(grid[0]))]

    return [''.join([grid[y][x] for y,x in zip(range(r,-1,-1),range(c,len(grid[0])))]) for r,c in row_starts]


def rotate_90(grid,iterations=1):

    for i in range(iterations):
        grid = [] + [''.join([row[i] for row in grid][::-1]) for i in range(len(grid[0]))]

    return grid


def regular_search(grids, search_term='XMAS'):

    return sum(line.count(search_term) for grid in grids for line in grid)


def xmas_search(grids):

    return sum(1 for grid in grids for y,line in enumerate(grid[1:-1]) for x,char in enumerate(line[1:-1])
                  if char == 'A' and grid[y][x:x+3:2] + grid[y+2][x:x+3:2] == 'MSMS')


def main(f):

    grids = list(sum([(g, rotate_45(g)) for g in [rotate_90(open(f).read().split('\n'), i) for i in range(4)]],()))

    return regular_search(grids), xmas_search(grids[::2])


print(main('04.txt'))