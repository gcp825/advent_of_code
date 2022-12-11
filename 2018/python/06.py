#  A little slow, but couldn't figure out a quicker way than brute force without some clever heuristic.
#  Part 2 was my first 2018 example of not reading the question properly - I calculated something completely different at first!

from collections import Counter

def manhattan(a,b): return sum([abs(a[0]-b[0]),abs(a[1]-b[1])])

def main(filepath,safe_distance=10000):

    grid, total_distances = (dict(), [])

    input  = [(int(y),int(x)) for x,y in [x.split(', ') for x in open(filepath,'r').read().split('\n')]]
    bounds = (max(input)[0] + min(input)[0], max([(x,y) for y,x in input])[0] + min([(x,y) for y,x in input])[0])
    coords = [(chr(i+34),c) for i,c in enumerate(input)]

    for y in range(0,bounds[0]+1):
        for x in range(0,bounds[1]+1):
            distances = [manhattan((y,x),c) for _,c in coords]
            total_distances += [(sum(distances))]
            ordered = sorted(distances)
            if ordered[0] < ordered[1]:
                idx = distances.index(ordered[0])
                grid[(y,x)] = coords[idx][0]

    infinite_ids = set([id for c,id in grid.items() if c[0] in (0,bounds[0]) or c[1] in (0,bounds[1])])
    largest_finite_area = Counter([id for id in grid.values() if id not in infinite_ids]).most_common(1)[0][1]

    safest_area = len([d for d in total_distances if d < safe_distance])

    return largest_finite_area, safest_area


print(main('06.txt'))
