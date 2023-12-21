#  Part 2 solved by examining the location totals for 500 steps, the difference between totals for consecutive 
#  steps, the differences between those differences and then the differences between those differences to 
#  establish that there was a repeating cycle. Having established the cycle interval, I then repeated the above 
#  for totals seperated by the interval to establish how to increase the totals with each interval. Then I just
#  had to work out what number of steps to start incrementing from in order to return the target steps value.

def count_steps(grid,target):

    locations = set([(y,x) for y,row in enumerate(grid) for x,col in enumerate(row) if col == 'S'])
    gy, gx = len(grid), len(grid[0])
    location_counts = [1]

    while len(location_counts)-1 < target:

        new_locations = set()
        for y,x in locations:
            adjacent = [(y-1,x),(y,x+1),(y+1,x),(y,x-1)]
            viable = [(ay,ax) for ay,ax in adjacent if (ay,ax) not in locations and grid[ay%gy][ax%gx] != '#']
            new_locations.update(viable)

        locations = new_locations
        location_counts += [len(list(locations))]

    return location_counts


def count_many_steps(grid,target):

    steps      = (target % len(grid)) + (2 * len(grid))
    counts     = count_steps(grid,steps)

    cycles     = [counts[-1-(len(grid)*n)] for n in (0,1,2)]
    increments = [a-b for a,b in zip(cycles[:2],cycles[1:])]

    total      = counts[-1]
    increment  = increments[0]
    difference = increments[0] - increments[1]

    while steps != target:
        total += (increment + difference)
        increment += difference
        steps += len(grid)

    return total


def main(filepath):

    grid = open(filepath).read().split('\n')

    part_1 = count_steps(grid,64)[-1]
    part_2 = count_many_steps(grid,26501365)

    return part_1, part_2


print(main('21.txt'))