#  Just Part 1... will attempt to write a generic solution to Part 2 when I have more time between Xmas & New Year.

def parse_input(filepath):

    grid, instr = [(x.split('\n'),y) for x,y in [tuple([z for z in open(filepath).read().split('\n\n')])]][0]

    grid = dict([((y,x),val) for y,row in enumerate(grid) for x,val in enumerate(row) if val in ('.','#')])

    instr = [x if x in 'LR' else int(x) for x in instr.replace('L',',L,').replace('R',',R,').split(',')]

    return grid, instr


def follow_instruction(grid,location,facing,move):

    cardinals, ordinals = {'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}, {'NE':(-1,1),'SE':(1,1),'SW':(1,-1),'NW':(-1,-1)}
    rotate = {'RN':'E','RE':'S','RS':'W','RW':'N','LN':'W','LE':'N','LS':'E','LW':'S'}

    if type(move) is not int:

        facing = rotate[move+facing]

    else:

        for _ in range(move):

            y,x = tuple(map(sum,zip(location,{**cardinals,**ordinals}[facing])))
            terrain = grid.get((y,x),'x')

            if terrain == 'x':
                coords = (min([k for k in grid.keys() if k[0] == y]) if facing == 'E' else
                          max([k for k in grid.keys() if k[0] == y]) if facing == 'W' else
                          min([k for k in grid.keys() if k[1] == x]) if facing == 'S' else
                          max([k for k in grid.keys() if k[1] == x]))
                terrain = grid[coords]
                if terrain == '.':
                    y,x = coords

            if terrain == '.':
                location = (y,x)

            if terrain == '#':
                break


    return location, facing


def navigate(grid,instr):

    location = min([k for k,v in grid.items() if v == '.'])
    facing   = 'E'

    for move in instr:
        location, facing = follow_instruction(grid,location,facing,move)
    
    return location, facing


def main(filepath):

    grid, instr       = parse_input(filepath)
    location, facing  = navigate(grid,instr)
    password          = ((location[0]+1)*1000) + ((location[1]+1)*4) + {'E':0,'S':1,'W':2,'N':3}[facing]
    
    return password

print(main('22.txt'))