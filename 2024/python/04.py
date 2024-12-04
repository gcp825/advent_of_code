# Much cleaner implementation than what I first wrote this morning; need to stop doing this whilst still asleep!

def rotate_45(grid):

    row_starts = [(y,0) for y in range(len(grid))] + [(len(grid)-1,x) for x in range(1,len(grid[0]))]

    return [''.join([grid[y][x] for y,x in zip(range(r,-1,-1),range(c,len(grid[0])))]) for r,c in row_starts]


def rotate_90(grid):

    return [''.join([row[i] for row in grid][::-1]) for i in range(len(grid[0]))]


def regular_search(grid, search_term='XMAS'):

    return sum(line.count(search_term) for line in grid)


def xmas_search(grid):

    return sum(1 for y,line in enumerate(grid[1:-1]) for x,char in enumerate(line[1:-1])
               if char == 'A' and grid[y][x:x+3:2] + grid[y+2][x:x+3:2] == 'MSMS')


def main(filepath):

    grid = open(filepath).read().split('\n')
    pt1, pt2 = (0,0)

    for _ in range(4):
        pt1 += regular_search(grid) + regular_search(rotate_45(grid))
        pt2 += xmas_search(grid)
        grid = rotate_90(grid)

    return pt1, pt2


print(main('04.txt'))