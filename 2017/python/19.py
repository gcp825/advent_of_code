def move(x,y,d): return (x,y-1) if d == 'N' else (x+1,y) if d == 'E' else (x,y+1) if d == 'S' else (x-1,y)

def main(filepath):

    layout = []    
    for y, row in enumerate(open(filepath,'r').read().split('\n')):
        for x,value in enumerate(row):
            if value != ' ': layout += [((x,y),value)]
    layout = dict(layout)

    coords = min(layout);  direction = 'S';  here = layout[coords];  letters = '';  steps = 0

    while here != '':

        steps += 1
        prev, coords = coords, move(*coords,direction)
        
        here = layout.get(coords,'')
        if here == '+':    
            direction = max(x[0] for x in [(x[0],layout.get(x[1],' ')) for x in [(x,move(*coords,x)) for x in 'NESW' if x != direction] if x[1] != prev] if x[1] != ' ')
        if here.isalpha(): 
            letters += here 

    return letters, steps

print(main('19.txt'))
