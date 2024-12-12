#  Can't imagine that my determination of sides is the quickest or slickest way of doing that. But it works!

def map_all_regions(garden, max_y, max_x):

    regions = {}
    queue = [(y,x) for y in range(max_y+1) for x in range(max_x+1)]

    while queue:

        y,x = queue.pop(0)
        region = map_region(garden, y, x, max_y, max_x)

        queue = [coords for coords in queue if coords not in region]
        regions[(y,x)] = list(sorted(list(region)))

    return regions


def map_region(garden, y, x, max_y, max_x):

    visited, plant_type = set(), garden[(y,x)]
    queue = [(y,x)]

    while queue:

        y,x = queue.pop(0)
        visited.add((y,x))

        adjacent = get_adjacent(y, x, max_y, max_x)
        queue += [(y,x) for y,x in adjacent if (y,x) not in queue and (y,x) not in visited and garden[(y,x)] == plant_type]

    return visited


def get_adjacent(y, x, max_y, max_x, min_y=0, min_x=0):

    return [(ay,ax) for ay,ax in [(y-1,x),(y,x+1),(y+1,x),(y,x-1)] if min_y <= ay <= max_y and min_x <= ax <= max_x]


def map_perimeter(region, max_y, max_x):

    perimeter = 0
    for y,x in region:
        adjacent = get_adjacent(y, x, max_y+1, max_x+1, -1, -1)
        perimeter += sum(1 for plot in adjacent if plot not in region)

    return perimeter


def map_sides(region, garden, max_y):

    sides = 0
    plant_type = garden[region[0]]

    for cycle in range(2):

        coords = [(x, max_y-y) for y,x in region] if cycle else [] + region
        grid = dict(((x, max_y-y),v) for (y,x),v in garden.items()) if cycle else {**garden}

        for i in (-1,1):
            for row in [sorted([(y,x) for y,x in coords if y == row]) for row in range(min(coords)[0], max(coords)[0]+1)]:
                edges = [x for y,x in row if grid.get((y+i,x),'') != plant_type]
                sides += sum(1 for b,a in zip(edges[1:], edges) if b-a > 1) + (1 if edges else 0)

    return sides


def main(filepath):

    garden = dict(((y,x),col) for y,row in enumerate(open(filepath).read().split('\n')) for x,col in enumerate(row))
    bounds = max(garden.keys())
    regions = map_all_regions(garden, *bounds)

    cost_1 = sum(map_perimeter(r,*bounds) * len(r) for r in regions.values())
    cost_2 = sum(map_sides(r, garden, bounds[0]) * len(r) for r in regions.values())

    return cost_1, cost_2


print(main('12.txt'))