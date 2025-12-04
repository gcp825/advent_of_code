def parse_input(f):

    return {(y,x) for y,row in enumerate(open(f).read().split('\n')) for x,loc in enumerate(row) if loc == '@'}


def calculate_neighbours(locations):

    return {(y,x):[(y+a,x+b) for a in (-1,0,1) for b in (-1,0,1) if (y,x) != (y+a,x+b)] for y,x in locations}


def main(filepath):

    removed = []
    locations = parse_input(filepath)
    neighbours = calculate_neighbours(locations)

    while not removed or removed[-1]:
        removable = [loc for loc in locations if sum(1 for n in neighbours[loc] if n in locations) < 4]
        locations.difference_update(removable)
        removed += [len(removable)]

    return removed[0], sum(removed)


print(main('04.txt'))