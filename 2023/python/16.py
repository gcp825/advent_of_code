#  Original version was horrifically slow due to using lists rather than sets.
#  It's still slow at 12 seconds... might be the way I'm calculating the next moves - which doesn't
#  use many lines of code but has got to the stage where it feels convoluted and might not be efficient.
#  Perhaps some more tuning later...

def setup_rules():

    compass = {'n':(-1,0),'s':(1,0),'e':(0,1),'w':(0,-1)}
    actions = './!|-'
    directions = ['nesw','enws','wsen',('n','ns','s','ns'),('ew','e','ew','w')]

    return dict([(a, dict(zip('nesw',d))) for a,d in zip(actions,directions)]), compass
           
       
def move(grid,next_directions,adjust,y,x,direction):

    return [(y+ay,x+ax,d) for d in tuple(next_directions[grid[y][x]][direction]) for ay,ax in [adjust[d]]]


def energised(grid,rules,origin):

    max_y, max_x = len(grid)-1, len(grid[0])-1
    seen_states = set()
    queue = [origin]

    while queue:
        state = queue.pop(0)
        seen_states.add(state)
        queue += [(y,x,d) for y,x,d in move(grid,*rules,*state) if  0 <= y <= max_y 
                                                                and 0 <= x <= max_x and (y,x,d) not in seen_states]

    return len(list(set([(y,x) for y,x,_ in seen_states])))


def most_energised(grid,rules):

    origins = ([(y,x,d) for y,d in zip((0,len(grid)-1),'sn') for x in range(len(grid[0]))] +
               [(y,x,d) for x,d in zip((0,len(grid[0])-1),'ew') for y in range(len(grid))])

    return max([energised(grid,rules,origin) for origin in origins])


def main(filepath):

    grid = open(filepath).read().replace('\\','!').split('\n')
    rules = setup_rules()

    return energised(grid,rules,(0,0,'e')), most_energised(grid,rules)


print(main('16.txt'))