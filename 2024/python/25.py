
def parse_input(filepath):

    locks_and_keys = [[],[]]

    for item in [item.split('\n') for item in open(filepath).read().split('\n\n')]:

        type, heights = item[0].count('.....'), [0]*5

        for i, line in enumerate(item):
            if (type == 0 and i > 0) or (type == 1 and i < 6):
                heights = [sum(x) for x in zip(heights, [pin.count('#') for pin in line])]

        locks_and_keys[type] += [heights]

    return tuple(locks_and_keys)


def main(filepath):

    locks, keys = parse_input(filepath)

    return sum(1 for match in [max(sum(x) for x in zip(lock,key)) for lock in locks for key in keys] if match <= 5)


print(main('25.txt'))