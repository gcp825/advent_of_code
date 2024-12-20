#  Slow. But I'll tune it some other time.
#  Also... threw away all of my original Part 1 after falling for the "it's just another 2d grid search" con!

def get_distances(filepath):

    grid = dict(((y,x),col) for y,row in enumerate(open(filepath).read().split('\n')) for x,col in enumerate(row))

    route = [()] + [loc for loc,val in grid.items() if val == 'E']

    for _ in range(sum(1 for v in grid.values() if v != '#')):
        y,x = route[-1]
        route += [c for c in [(y-1,x), (y,x+1), (y+1,x), (y,x-1)] if grid.get(c,'#') != '#' and c != route[-2]][:1]

    return [(c,i) for i,c in enumerate(route[1:])]


def manhattan(a,b): return sum((abs(a[0]-b[0]),abs(a[1]-b[1])))


def count_cheats(distances, time_limit, saving=100, cheats=0):

    distance = saving - time_limit

    for a, time_from_a in distances:
        for b, time_from_b in distances:
            if time_from_a - time_from_b >= distance:
                shortcut = manhattan(a,b)
                if shortcut <= time_limit:
                    if (time_from_a - time_from_b - shortcut) >= saving:
                        cheats += 1
    return cheats


def main(filepath):

    distances = get_distances(filepath)

    return tuple(count_cheats(distances,n) for n in (2,20))


print(main('20.txt'))