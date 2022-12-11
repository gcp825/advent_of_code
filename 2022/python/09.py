def manhattan(a,b): return sum([abs(a[0]-b[0]),abs(a[1]-b[1])])  

def main(filepath,nbr_of_knots):

    moves = ''.join([x*int(y) for x,y in [x.split(' ') for x in open(filepath).read().translate({85:78,82:69,68:83,76:87}).split('\n')]])

    knots = [(0,0)] * nbr_of_knots
    visited = set()
    cardinals, ordinals = {'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}, {'NE':(-1,1),'SE':(1,1),'SW':(1,-1),'NW':(-1,-1)}

    move_knot = lambda knot,direction: tuple(map(sum,zip(knot,{**cardinals,**ordinals}[direction])))


    for direction in moves:

        knots[0] = move_knot(knots[0],direction)

        for this in range(1,nbr_of_knots):

            prev = this-1
            knot_distance = manhattan(knots[prev],knots[this])

            if knot_distance == 2:
                if knots[prev][0] == knots[this][0] or knots[prev][1] == knots[this][1]:
                    knots[this] = [move for move in [move_knot(knots[this],d) for d in cardinals] if manhattan(knots[prev],move) == 1][0]

            elif knot_distance in (3,4):
                knots[this] = [move for move in [move_knot(knots[this],d) for d in ordinals] if manhattan(knots[prev],move) == knot_distance-2][0]

        visited.add(knots[-1])

    return len(list(visited))

print((main('09.txt',2),main('09.txt',10)))