from intcode import IntcodeComputer    # see intcode.py in this repo

def paint(f,start_colour):

    left = {'N':'W','E':'N','S':'E','W':'S'};  right = dict([(v,k) for k,v in left.items()])

    panels = {};  y,x = (0,0);  panels[(y,x)] = start_colour;  facing = 'N'
    colour, turn = (start_colour,0)

    comp = IntcodeComputer(load=f)

    while True:
        colour = comp.run(panels.get((y,x),0))
        if colour is None: break
        else: 
            panels[(y,x)] = colour
            turn = comp.run()
            if turn is None: break
            else:
                facing = left[facing] if turn == 0 else right[facing]
                y,x = (y-1,x) if facing == 'N' else (y,x+1) if facing == 'E' else (y+1,x) if facing == 'S' else (y,x-1)

    return panels

def render(panels):

    reverse = [(x,y) for y,x in panels.keys()]
    grid = [];  row = ''
    for y in range(min(panels)[0],max(panels)[0]+1):
        for x in range(min(reverse)[0],max(reverse)[0]+1):
            row += '#' if panels.get((y,x),0) == 1 else ' '
        grid += [row]
        row = ''
    return grid

def main(f):

    pt1 = paint(f,0)
    pt2 = render(paint(f,1))

    print('Part 1:',len(pt1.keys()),'\nPart2:\n')
    for row in pt2: print(row)
    return '\n' 

print(main('11.txt'))
