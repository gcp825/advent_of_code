def main(filepath,cycles,part2):

    locations = {}
    for y,row in enumerate(open(filepath,'r').read().split('\n')):
        for x,v in enumerate(list(row)):
            locations[(x,y)] = v

    left = {'N':'W','E':'N','S':'E','W':'S'}
    right = {'N':'E','E':'S','S':'W','W':'N'}
    coords = (max(locations)[0]//2,max(locations)[1]//2);  direction = 'N';  infect_ct = 0

    for _ in range(cycles):

        state = locations.get(coords,'.')

        if state == '#':
            direction = right[direction]
            locations[coords] = 'f' if part2 else '.'
        elif state == '.':
            direction = left[direction]
            locations[coords] = 'w' if part2 else '#'
        elif state == 'f':
            direction = left[left[direction]]
            locations[coords] = '.'
        else:
            locations[coords] = '#'

        infect_ct = infect_ct + 1 if (state == '.' and not part2) or (state == 'w' and part2) else infect_ct

        x,y = coords;  coords = (x,y-1) if direction == 'N' else (x,y+1) if direction == 'S' else (x+1,y) if direction == 'E' else (x-1,y)     

    return infect_ct

print(main('22.txt',10000,False))
print(main('22.txt',10000000,True))
