#  So this is v2. I said I'd come back to it eventually, and I did... and it's much faster than the lazy v1, and also much uglier than the beautiful v1! 
#  It's now doing the minimum number of seat proximity checks possible (at least without caching/reusing the results of prior checks where relevant - 
#  which would be hideous to try and implement)

def setup_floorplan(filepath):
    
    with open(filepath,'r') as i:
        f = i.read().replace('L','#').split('\n')
    
    return f


def render_floorplan(floorplan):
 
    for r in floorplan: print(r.replace('.','-'))
    print('')
   
    return None

 
def move(floorplan,proximity,rules):

    update = [];  changes = 0
    
    for row_nbr, row in enumerate(floorplan):
        new_row = ''
        for seat, status in enumerate(list(row)):
            if status == '.':
                new_row += status
            else:
                new_status = determine_status(floorplan,row_nbr,seat,status,proximity,rules)
                new_row += new_status
                if status != new_status: changes += 1
 
        update += [new_row]
        
    return update, changes

 
def determine_status(floorplan,row,seat,status,proximity,rules):

    n = ne = e = se = s = sw = w = nw = '.'
    x = len(floorplan[0]);  y = len(floorplan)
    proximity = proximity if proximity > 0 else max(x,y)
    ct = 0
    
    if row > 0 and ((status == 'L' and ct == 0) or (status == '#' and ct < rules and ct + 8 >= rules)):
        for i in range(row-1,-1,-1):
            n = floorplan[i][seat]
            if n != '.' or row-i == proximity: break
        if n == '#': ct+= 1
            
    if row < y-1 and ((status == 'L' and ct == 0) or (status == '#' and ct < rules and ct + 7 >= rules)):
        for i in range(row+1,y,+1):
            s = floorplan[i][seat]
            if s != '.' or i-row == proximity: break
        if s == '#': ct+= 1
            
    if seat > 0 and ((status == 'L' and ct == 0) or (status == '#' and ct < rules and ct + 6 >= rules)):
        for i in range(seat-1,-1,-1):
            w = floorplan[row][i]
            if w != '.' or seat-i == proximity: break
        if w == '#': ct+= 1
            
    if seat < x-1 and ((status == 'L' and ct == 0) or (status == '#' and ct < rules and ct + 5 >= rules)):
        for i in range(seat+1,x,+1):
            e = floorplan[row][i]
            if e != '.' or i-seat == proximity: break
        if e == '#': ct+= 1

    if row > 0 and seat > 0 and ((status == 'L' and ct == 0) or (status == '#' and ct < rules and ct + 4 >= rules)):
        r = row-1;  i = seat-1
        while r >= 0 and i >= 0:
            nw = floorplan[r][i]
            if nw != '.' or row-r == proximity: break
            else: r -= 1;  i -= 1
        if nw == '#': ct+= 1

    if row > 0 and seat < x-1 and ((status == 'L' and ct == 0) or (status == '#' and ct < rules and ct + 3 >= rules)):
        r = row-1;  i = seat+1
        while r >= 0 and i < x:
            ne = floorplan[r][i]
            if ne != '.' or row-r == proximity: break
            else: r -= 1;  i += 1
        if ne == '#': ct+= 1
        
    if row < y-1 and seat > 0 and ((status == 'L' and ct == 0) or (status == '#' and ct < rules and ct + 2 >= rules)):
        r = row+1;  i = seat-1
        while r < y and i >= 0:
            sw = floorplan[r][i]
            if sw != '.' or r-row == proximity: break
            else: r += 1;  i -= 1
        if sw == '#': ct+= 1

    if row < y-1 and seat < x-1 and ((status == 'L' and ct == 0) or (status == '#' and ct < rules and ct + 1 >= rules)):
            r = row+1;  i = seat+1
            while r < y and i < x:
                se = floorplan[r][i]
                if se != '.' or r-row == proximity: break
                else: r += 1;  i += 1
            if se == '#': ct+= 1
                
    return '#' if status == 'L' and ct == 0 else 'L' if status == '#' and ct >= rules else status

        
def calculate_occupancy(floorplan,proximity,rules,stdout=False):

    before = [] + floorplan;  cycles = 1
    
    if stdout: render_floorplan(before)
    
    while True:
        after, changes = move(before,proximity,rules)
        if changes > 0:
            before = [] + after
            cycles += 1
            if stdout: render_floorplan(after)
        else:
            break
        
    if stdout: print('Number of Cycles:',cycles)
        
    return ''.join(after).count('#')

        
def main(filepath,rules,proximity=0,stdout=False):
    
    f = setup_floorplan(filepath)
    seat_ct = calculate_occupancy(f,proximity,rules,stdout)
    
    return seat_ct
    
    
print(main('D:/grid.txt',4,1))  # pt1
print(main('D:/grid.txt',5))    # pt2
