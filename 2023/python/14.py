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


def cycle(platform, cycles=10**9, sample_size=200):

    loads = []

    # Take a small sample of consecutive load values

    for _ in range(sample_size):
        for d in 'nwse':
            platform = tilt(platform,d)
        loads += [load(platform)]

    # Get the minimum load value from the sample + find the max load value that appears after that

    cutoff = loads.index(min(loads))+1
    hi = max(loads[cutoff:])

    # Get the minimum load value that appears after the max load value found above

    cutoff = [n+1 for n,v in enumerate(loads) if v == hi and n > cutoff][0]
    lo = min(loads[cutoff:])

    # Determine the interval between repeat instances of the min load value found above

    low_indices = [n for n,v in enumerate(loads) if v == lo and n > cutoff]
    interval = low_indices[-1] - low_indices[-2]

    # Align current cycle with last known low value

    current_cycle = low_indices[-1] + 1

    # Using the known interval between repeated instances of the low value, determine the cycle immediately before
    # the target cycle that has this load value. From this, calculate the offset of this cycle to the target cycle.

    number_of_intervals = (cycles - current_cycle) // interval
    offset = cycles - current_cycle - (interval * number_of_intervals)
    
    # Using the offset, return the target value from the sample of load values

    return loads[low_indices[-2] + offset]


def main(filepath):

    platform = open(filepath).read().split('\n')

    return load(tilt(platform,'n')), cycle(platform)


print(main('14.txt'))