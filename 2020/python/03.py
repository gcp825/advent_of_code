def tree_count(terrain,across,down):

    tree_ct = 0
    x,y = 0,0
    a,b = len(terrain[0]) - 1, len(terrain) - 1
    
    while y < b:

        y = y + down
        x = x + across           
        if x > a: x = x-a-1   # wrap around to other side of the terrain
        
        if terrain[y][x] == '#': tree_ct += 1
            
    return tree_ct

def multiply_trees(terrain,routes):

    prod = 1    
    for x in routes: prod = prod * tree_count(grid,x[0],x[1])
    
    return prod
        
grid = ['..##.......',
        '#...#...#..',
        '.#....#..#.',
        '..#.#...#.#',
        '.#...##..#.',
        '..#.##.....',
        '.#.#.#....#',
        '.#........#',
        '#.##...#...',
        '#...##....#',
        '.#..#...#.#']

print(multiply_trees(grid,[(3,1)]))                              # part 1
print(multiply_trees(grid,[(1,1),(3,1),(5,1),(7,1),(1,2)]))      # part 2
