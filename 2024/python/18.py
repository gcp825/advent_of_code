from heapq import heappop, heappush

def manhattan(a,b): return sum([abs(a[0]-b[0]),abs(a[1]-b[1])])


def get_moves(y, x, wall):

    return [c for c in [(y-1,x), (y,x+1), (y+1,x), (y,x-1)] if c not in wall]


def a_star(bytes, origin=(0,0), target=(70,70)):

    wall = set([(y,x) for y in (origin[0]-1, target[0]+1) for x in range(origin[1]-1, target[1]+2)] +
               [(y,x) for x in (origin[1]-1, target[1]+1) for y in range(origin[0]-1, target[0]+2)] + bytes)

    distance = manhattan(origin,target)
    queue = [(distance + 0, distance, 0, origin)]
    seen = {origin:0}

    while queue:
        _, _, steps, location = heappop(queue)
        if location == target: break
        else:
            steps += 1
            for new_location in get_moves(*location, wall):
                if steps < seen.get(new_location, float("inf")):
                    seen[new_location] = steps
                    distance = manhattan(new_location, target)
                    heappush(queue,(distance + steps, distance, steps, new_location))

    return steps if location == target else None


def binary_search(bytes):

    lo, hi = 0, len(bytes)

    while hi-lo > 1:
        mid = (lo+hi)//2
        achievable = a_star(bytes[:mid+1])
        lo, hi = (mid,hi) if achievable else (lo,mid)

    return bytes[hi] if a_star(bytes[:lo+1]) else bytes[lo]


def main(filepath):

    bytes = [tuple(map(int,x.split(','))) for x in open(filepath).read().split('\n')]

    return a_star(bytes[:1024]), binary_search(bytes)


print(main('18.txt'))
