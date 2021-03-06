def setup_grid(filepath,stuck_corners=False):
    
    f = open(filepath,'r').read().split('\n')
    if stuck_corners:
        f[0] = '#'+f[0][1:-1]+'#'
        f[len(f)-1] = '#'+f[len(f)-1][1:-1]+'#'

    return f

def cycle_lights(grid,cycles,stuck_corners=False,render=False):

    for r in range(cycles):
        transposed_grid = [];  new_grid = [] 
        for x in range(len(grid[0])):
            start = max(0,x-1);  end = x+2;  new_col = ''
            for y in range(len(grid)):
                
                a = b if y > 0 else ''
                b = c if y > 0 else grid[y][start:end]
                c = grid[y+1][start:end] if y <= len(grid)-2 else ''
                
                ct = str(a+b+c).count('#') - str(grid[y][x]).count('#')
                new_status = '#' if grid[y][x] == '.' and ct == 3 else '.' if grid[y][x] == '#' and ct not in (2,3) else grid[y][x]
                
                if stuck_corners and len(a+b+c) == 4:
                    new_col += '#'
                else:
                    new_col += new_status
                
            transposed_grid += [new_col]
        for i in range(len(transposed_grid)): new_grid += [''.join([row[i] for row in transposed_grid])]
        grid = new_grid
        
    if render: render_grid(grid)
        
    return ''.join(grid).count('#')

def render_grid(grid):
 
    for row in grid: print(row.replace('.','-'))
    print('')
    return None
        
def main(filepath,cycles=100):
    
    pt1 = cycle_lights(setup_grid(filepath),cycles)
    pt2 = cycle_lights(setup_grid(filepath,True),cycles,True)
    
    return pt1, pt2
    
print(main('18.txt'))
