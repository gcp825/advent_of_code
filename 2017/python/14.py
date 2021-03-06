def knot_hash(data):

    lengths = list(map(ord,list(data))) + [17, 31, 73, 47, 23];  numbers = list(range(256));  i = 0;  skip = 0  

    for _ in range(64):
        for length in lengths:                      
            numbers = numbers[i:] + numbers[:i] 
            numbers = numbers[:length][::-1] + numbers[length:]
            numbers = numbers[i*-1:] + numbers[:i*-1]
            i = (i + length + skip) % len(numbers)
            skip += 1

    return ''.join([('0'+hex(eval('^'.join(list(map(str,numbers[i:i+16])))))[2:])[-2:] for i in range(0,256,16)]) 

def setup_grid(salt,size):

    grid = []
    for n in range(size):
        grid += [list(map(int,list(bin(int(knot_hash(salt+'-'+str(n)),16))[2:].zfill(size))))]
    return grid

def determine_regions(grid,size):
    
    x= 0;  y = 0;  regions = 0
    while y < size:
        while x < size:
            if grid[y][x] == 1:
                grid = explore_region(grid,size,y,x)
                regions += 1
            x += 1
        x = 0;  y += 1

    return regions

def explore_region(grid,size,y,x):    
    
    members = set();  queue = [(y,x)] 

    while len(queue) > 0:
        y,x = queue.pop(0)
        if grid[y][x] == 1:
            members.add((y,x))
            queue += [(b,a) for b,a in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)] if (b,a) not in members and 0 <= a < size and 0 <= b < size]
            grid[y][x] = 0

    return grid

def main(salt,size):

    grid = setup_grid(salt,size)
    used = sum(sum(row) for row in grid)
    regions = determine_regions(grid,size)

    return used, regions

print(main('jxqlasbh',128))
