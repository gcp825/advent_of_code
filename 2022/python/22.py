#  Spent ages trying to think about how to implement a generic solution to Part 2 rather than just code a bespoke solution for the input
#  because doing the latter just seemed tedious. In the end, decided to code the bespoke solution as a step towards something generic 
#  and found it surprisingly straightforward - once I'd made the obligatory cardboard cube to aid with matching the faces/edges - and
#  actually not that tedious!


def parse_input(filepath):

    grid, instr = [(x.split('\n'),y) for x,y in [tuple([z for z in open(filepath).read().split('\n\n')])]][0]

    grid = dict([((y,x),val) for y,row in enumerate(grid) for x,val in enumerate(row) if val in ('.','#')])

    instr = [x if x in 'LR' else int(x) for x in instr.replace('L',',L,').replace('R',',R,').split(',')]

    a = [[((y,x),v) for (y,x),v in grid.items() if y == n and 50 <= x < 100] for n in range(50)]
    b = [[((y,x),v) for (y,x),v in grid.items() if y == n and 100 <= x < 150] for n in range(50)]
    c = [[((y,x),v) for (y,x),v in grid.items() if y == n and 50 <= x < 100] for n in range(50,100)]
    d = [[((y,x),v) for (y,x),v in grid.items() if y == n and 50 <= x < 100] for n in range(100,150)]
    e = [[((y,x),v) for (y,x),v in grid.items() if y == n and 0 <= x < 50] for n in range(100,150)]
    f = [[((y,x),v) for (y,x),v in grid.items() if y == n and 0 <= x < 50] for n in range(150,200)]

    return grid, instr, (a,b,c,d,e,f)


def get_edges(x):

    edges = [[c[0] for c in x[0]], [r[-1][0] for r in x], [c[0] for c in x[-1]], [r[0][0] for r in x]]

    return edges + [x[::-1] for x in edges]


def build_portals(faces):

    edges = dict([(k,get_edges(f)) for i,f in enumerate(faces) for j,k in enumerate('abcdef') if i == j])

    portals = ( 

        [((x,'N'),(y,'E')) for x,y in zip(edges['a'][0],edges['f'][3])] +
        [((x,'W'),(y,'E')) for x,y in zip(edges['a'][7],edges['e'][3])] +
        [((x,'N'),(y,'N')) for x,y in zip(edges['b'][0],edges['f'][2])] +
        [((x,'E'),(y,'W')) for x,y in zip(edges['b'][1],edges['d'][5])] +
        [((x,'S'),(y,'W')) for x,y in zip(edges['b'][2],edges['c'][1])] +
        [((x,'E'),(y,'N')) for x,y in zip(edges['c'][1],edges['b'][2])] +
        [((x,'W'),(y,'S')) for x,y in zip(edges['c'][3],edges['e'][0])] +
        [((x,'E'),(y,'W')) for x,y in zip(edges['d'][1],edges['b'][5])] +
        [((x,'S'),(y,'W')) for x,y in zip(edges['d'][2],edges['f'][1])] +
        [((x,'N'),(y,'E')) for x,y in zip(edges['e'][0],edges['c'][3])] +
        [((x,'W'),(y,'E')) for x,y in zip(edges['e'][7],edges['a'][3])] +
        [((x,'E'),(y,'N')) for x,y in zip(edges['f'][1],edges['d'][2])] +
        [((x,'S'),(y,'S')) for x,y in zip(edges['f'][2],edges['b'][0])] +
        [((x,'W'),(y,'S')) for x,y in zip(edges['f'][3],edges['a'][0])]
    
    )

    return dict(portals)


def follow_instruction(grid,location,facing,move,portals):

    compass = {'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1),'NE':(-1,1),'SE':(1,1),'SW':(1,-1),'NW':(-1,-1)}
    rotate  = {'RN':'E','RE':'S','RS':'W','RW':'N','LN':'W','LE':'N','LS':'E','LW':'S'}

    if type(move) is not int:

        facing = rotate[move+facing]

    else:

        for _ in range(move):

            if (location,facing) in portals:

                coords, orientation = portals[(location,facing)]

                if grid[coords] == '#': break
                else:
                    location, facing = coords, orientation

            else:

                y,x = tuple(map(sum,zip(location,compass[facing])))

                terrain = grid.get((y,x),None)

                if terrain is None:

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


def navigate(grid,instr,portals):

    location = min([k for k,v in grid.items() if v == '.'])
    facing   = 'E'

    for move in instr:
        location, facing = follow_instruction(grid,location,facing,move,portals)
    
    return location, facing


def main(filepath,use_portals=False):

    grid, instr, faces = parse_input(filepath)
    portals            = build_portals(faces) if use_portals else dict()
    location, facing   = navigate(grid,instr,portals) 
    password           = ((location[0]+1)*1000) + ((location[1]+1)*4) + {'E':0,'S':1,'W':2,'N':3}[facing]
    
    return password


print((main('22.txt'),main('22.txt',True)))