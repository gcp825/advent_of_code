def rotate(platform,n):

    for _ in range(n):
        platform = [] + [''.join([row[i] for row in platform][::-1]) for i in range(len(platform[0]))]

    return platform


def slide(row):

    while '.O' in row:
        row = row.replace('.O','O.')

    return row


def tilt(platform,d):

    rotations = dict(zip('wsen',(0,1,2,3)))
    platform = [slide(row) for row in rotate(platform,rotations[d])]

    return rotate(platform,-rotations[d]%4)


def load(platform):

    return sum([row.count('O') * load for row,load in zip(platform,range(len(platform),0,-1))])


def cycle(platform, target_cycle=10**9):

    interval, current_cycle, sequences = (0,1,{})
    loads = [load(platform)]

    # Store load values & count repeating instances of groups of 5 consecutive load values.
    # When a group has repeated twice or more, break if the interval between the last two repeats is identical.

    while not interval:

        for d in 'nwse': platform = tilt(platform,d)

        loads += [load(platform)]
        repeats = sequences.get(tuple(loads[-5:]),[]) + [current_cycle]

        if len(repeats) >= 3 and repeats[-1]-repeats[-2] == repeats[-2]-repeats[-3]:
            interval = repeats[-1]-repeats[-2]
        else:
            sequences[tuple(loads[-5:])] = repeats
            current_cycle += 1

    # Use the determined interval to calculate the offset between the current load value
    # and the value that will correspond to the target cycle

    number_of_intervals = (target_cycle - current_cycle) // interval
    offset = target_cycle - current_cycle - (interval * number_of_intervals)
    
    # Using the offset, return the target value from the stored load values

    return loads[current_cycle - interval + offset]


def main(filepath):

    platform = open(filepath).read().split('\n')

    return load(tilt(platform,'n')), cycle(platform)


print(main('14.txt'))