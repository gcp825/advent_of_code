import re

def render(positions):

    coords = list(sorted(positions.values()))
    y,yy   = (coords[0][0], coords[-1][0])
    x,xx   = (min(c[::-1] for c in coords)[0], max(c[::-1] for c in coords)[0])

    if yy-y > 10: return False

    else:

        print('\n')

        for row in range(y,yy+1):
            line = ''
            for col in range(x,xx+1):
                line += '#' if (row,col) in coords else ' '
            print(line)

        print('\n')           

    return True


def main(filepath):

    stars     = [tuple(map(int,y.split(','))) for y in [re.sub('[^1234567890,-]','',x[:-1].replace('>',',')) for x in open(filepath,'r').read().split('\n')]]
    velocity  = dict([(i,(x[3],x[2])) for i,x in enumerate(stars)])
    positions = dict([(i,(x[1],x[0])) for i,x in enumerate(stars)])
    seconds   = 0

    while True:
        
        seconds += 1
        positions = dict([(i,(x[0]+velocity[i][0],x[1]+velocity[i][1])) for i,x in positions.items()])
        printed = render(positions)
        if printed: break

    return str(seconds) + ' seconds'

print(main('10.txt'))