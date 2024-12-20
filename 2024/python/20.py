#  Threw away all of my original Part 1 after falling for the "it's just another 2d grid search" con!
#  Not superfast, but much quicker than many of other python solutions on the megathread. Probably still
#  missing one more trick somewhere?

def get_route(filepath):

    grid = dict(((y,x),col) for y,row in enumerate(open(filepath).read().split('\n')) for x,col in enumerate(row))

    route = [()] + [loc for loc,val in grid.items() if val == 'S']

    for _ in range(sum(1 for v in grid.values() if v != '#')):
        y,x = route[-1]
        route += [c for c in [(y-1,x), (y,x+1), (y+1,x), (y,x-1)] if grid.get(c,'#') != '#' and c != route[-2]][:1]

    return route[1:]


def count_cheats(route, part_1=0, part_2=0):

    for i,(ay,ax) in enumerate(route):
        for j,(by,bx) in enumerate(route[i+100:]):
            shortcut = abs(ay-by) + abs(ax-bx)
            if shortcut <= 20:
                if j >= shortcut:
                    part_2 += 1
                    if shortcut == 2:
                        part_1 += 1

    return part_1, part_2


def main(filepath):

    return count_cheats(get_route(filepath))


print(main('20.txt'))