#  This is slow at ~9 seconds on my laptop... but other than trying to fast forward rather than move
#  step-by-step or cache intermediate states with their energised counts, not sure what else I can do.
#  My original move determination process looked much slicker and neater than it does now... but this
#  implementation is notably quicker and more explicit.

def move(tile,y,x,dir):

    if tile == '/': 
        return [{'e':(y-1,x,'n'), 'n':(y,x+1,'e'), 'w':(y+1,x,'s'), 's':(y,x-1,'w')}[dir]]

    elif tile == '!': 
        return [{'w':(y-1,x,'n'), 's':(y,x+1,'e'), 'e':(y+1,x,'s'), 'n':(y,x-1,'w')}[dir]]

    elif tile == '-' and dir in 'ns': 
        return [(y,x-1,'w'),(y,x+1,'e')]

    elif tile == '|' and dir in 'ew':
        return [(y-1,x,'n'),(y+1,x,'s')]

    else:
        return [{'n':(y-1,x,'n'), 'e':(y,x+1,'e'), 's':(y+1,x,'s'), 'w':(y,x-1,'w')}[dir]]

    
def energised(grid,origin):

    yy, xx = len(grid)-1, len(grid[0])-1
    seen_states = set()
    queue = [origin]

    while queue:
        y,x,d = queue.pop(0)
        seen_states.add((y,x,d))
        queue += [m for m in move(grid[y][x],y,x,d) if 0 <= m[0] <= yy and 0 <= m[1] <= xx and m not in seen_states]

    return len(list(set([(y,x) for y,x,_ in seen_states])))


def most_energised(grid):

    origins = ([(y,x,d) for y,d in zip((0,len(grid)-1),'sn') for x in range(len(grid[0]))] +
               [(y,x,d) for x,d in zip((0,len(grid[0])-1),'ew') for y in range(len(grid))])

    return max([energised(grid,origin) for origin in origins])


def main(filepath):

    grid = open(filepath).read().replace('\\','!').split('\n')

    return energised(grid,(0,0,'e')), most_energised(grid)


print(main('16.txt'))