# This is some ugly code. And my approach to Part 1 really didn't help for Part 2 at all!

def rotate(grid, degrees):

    def _rotate_45(grid):

        new_grid = []

        for start in range(len(grid)):
            new_row, y = ('', start)
            for x in range(start+1):
                new_row += grid[y][x]
                y -= 1
            new_grid += [new_row]

        for start in range(1,len(grid[0])):
            new_row, y = ('', len(grid)-1)
            for x in range(start, len(grid[0])):
                new_row += grid[y][x]
                y -= 1
            new_grid += [new_row]

        return new_grid

    def _rotate_90(grid):

        return [] + [''.join([row[i] for row in grid][::-1]) for i in range(len(grid[0]))]


    if degrees % 45 != 0:
        raise ValueError("Degrees must be divisible by 45")
    else:
        new_grid = [] + grid
        for _ in range(degrees//90):
            new_grid = _rotate_90(new_grid)
        if degrees % 90 != 0:
            new_grid = _rotate_45(new_grid)

    return new_grid


def search(grid,search_term):

    count = 0
    for degrees in range(0,360,45):
        search_grid = rotate(grid,degrees)
        for line in search_grid:
            count += line.count(search_term)

    return count


def x_mas_search(grid):

    count = 0
    for degrees in range(0,360,90):
        search_grid = rotate(grid,degrees)
        for y,line in enumerate(search_grid[1:-1]):
            for x,char in enumerate(line[1:-1]):
                if char == 'A':
                    above = search_grid[y][x:x+3:2]
                    below = search_grid[y+2][x:x+3:2]
                    if above == 'MS' and below == 'MS':
                        count += 1
    return count


def main(filepath):

    grid = open(filepath).read().split('\n')

    return search(grid,'XMAS'), x_mas_search(grid)

print(main('04.txt'))