#  Went for the easy option on part 2 by just including the entire trail so far within the item on the priority
#  queue - allowing me to easily dump it into the set of best locations at the end. It would be more efficient to
#  keep a record of all of the cheapest point-to-point moves and reverse engineer the best locations from that, but
#  this is fast enough for my liking, so sticking with keeping it simple.

from heapq import heappush, heappop

def parse_input(filepath):

    grid = [((y,x),col) for y,row in enumerate(open(filepath).read().split('\n')) for x,col in enumerate(row)]
    wall = {loc for loc,val in grid if val == '#'}
    origin = [loc for loc,val in grid if val == 'S'][0]
    target = [loc for loc,val in grid if val == 'E'][0]

    return wall, origin, target


def get_moves(y, x, d, wall):

    adjacent = [(y-1,x,0), (y,x+1,1), (y+1,x,2), (y,x-1,3)]
    valid_moves = [c for c in adjacent][:(d-2)%4] + [c for c in adjacent][((d-2)%4)+1:]
    moves = [(ny if nd == d else y, nx if nd == d else x, nd) for ny, nx, nd in valid_moves if (ny,nx) not in wall]

    return moves


def dijkstra(wall, origin, target):

    seen = {(*origin, 1) : 0}
    queue = [(0, *origin, 1, [origin])]
    lowest_total_cost = float('inf')

    while queue:

        cost, y, x, facing, trail = heappop(queue)

        if (y,x) == target:

            if cost < lowest_total_cost:
                lowest_total_cost = cost
                best_locations = set(trail)

            elif cost == lowest_total_cost:
                best_locations.update(trail)

        else:
            for ny, nx, direction in get_moves(y, x, facing, wall):

                new_cost = cost + 1 if direction == facing else cost + 1000

                if cost <= lowest_total_cost:
                    lowest_cost_at_this_location = seen.get((ny, nx, direction), float('inf'))

                    if new_cost <= lowest_cost_at_this_location:
                        seen[(ny, nx, direction)] = new_cost
                        heappush(queue, (new_cost, ny, nx, direction, trail + [(ny,nx)]))

    return lowest_total_cost, len(best_locations)


def main(filepath):

    return dijkstra(*parse_input(filepath))


print(main('16.txt'))