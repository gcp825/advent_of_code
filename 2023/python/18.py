#  I stubbornly avoided completing Part 2 for a few days, insistent I was going to solve it without shoelace and
#  pick - and I still intend to do that. But just haven't had time this week and the lack of the second star was
#  starting to bug me... so here's a shoelace and pick implementation for now!

def parse_instructions(filepath):

    directions = dict(zip('URDL',(0,1,2,3)))

    reformatted  = [tuple(x.split(' ')) for x in open(filepath).read().split('\n')]
    instructions = [(directions[d], int(m), (int(c[-2])+1)%4, int(c[2:-2],16)) for d,m,c in reformatted]

    return [x[:2] for x in instructions], [x[2:] for x in instructions]


def shoelace_and_pick(polygon):
    '''
    Determines the area of a simple polygon where vertices are expressed as integer coordinates.
    The polygon is expressed as a list of (direction, length) tuples expressing the edges.
    Direction values are 0,1,2,3 - corresponding to N,E,S,W (or U,R,D,L)
    '''

    def get_next_vertex(cy,cx,d,m):

        return [(cy-m,cx),(cy,cx+m),(cy+m,cx),(cy,cx-m)][d]


    def positive_shift(coords):

        coords = [(y-adj,x) for y,x in coords for adj in [min([y for y,_ in coords])]]
        coords = [(y,x-adj) for y,x in coords for adj in [min([x for _,x in coords])]]

        return coords


    def determine_vertices(instructions):

        vertices = [(0,0)]

        for direction, metres in instructions:
            vertices += [get_next_vertex(*vertices[-1], direction, metres)]

        return positive_shift(vertices[1:])


    def perimeter(vertices):

        return sum([abs(by-ay) + abs(bx-ax) for (ay,ax),(by,bx) in zip(vertices,vertices[1:] + vertices[:1])])


    def shoelace(vertices):

        return abs(sum([(by*ax)-(ay*bx) for (ay,ax),(by,bx) in zip(vertices,vertices[1:] + vertices[:1])]) // 2)

    
    vertices = determine_vertices(polygon)

    return shoelace(vertices) + perimeter(vertices)//2 + 1


def main(filepath):

    volumes = []
    instructions = parse_instructions(filepath)

    for instr in instructions:
        volumes += [shoelace_and_pick(instr)]

    return tuple(volumes)

    
print(main('18.txt'))
