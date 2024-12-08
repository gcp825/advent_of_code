def parse_input(filepath):

    grid = [((y,x),val) for y,row in enumerate(open(filepath).read().split('\n')) for x,val in enumerate(row)]

    return {x for x in grid if x[1] != '.'}, max(grid)[0]


def count_antinodes(antennas, bounds, repeat):

    radius = range(max(bounds)+1) if repeat else range(1,2)

    pairs = [(*a,*b) for a,t1 in antennas for b,t2 in antennas if t1 == t2 and a < b]
    antinodes = [(p[i] + n*(p[i]-p[i-2]), p[i+1] + n*(p[i+1]-p[i-1])) for p in pairs for i in (0,2) for n in radius]

    return len({(y,x) for y,x in antinodes if 0 <= y <= bounds[0] and 0 <= x <= bounds[1]})


def main(filepath):

    grid = parse_input(filepath)

    return tuple(count_antinodes(*grid, repeat) for repeat in (False, True))


print(main('08.txt'))