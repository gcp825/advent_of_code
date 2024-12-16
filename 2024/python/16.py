from heapq import heapify, heappush, heappop

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


def dijkstra(wall, origin, target, target_cost=0):

    lowest_total_cost, best_locations = float('inf'), set()

    seen = {(*origin, 1) : 0}
    queue = [(0, *origin, 1, [origin])];  heapify(queue)

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