from functools import reduce

def parse_input(path):

    pt1 = list(zip(*[tuple([int(n) for n in x[11:].strip().split(' ') if n]) for x in open(path).read().split('\n')]))
    pt2 = [tuple([int(x[11:].strip().replace(' ','')) for x in open(path).read().split('\n')])]

    return pt1, pt2


def calc_winning_perms(duration, record):

    perms = duration + 1

    for hold_time in range(perms):
        distance = hold_time * (duration - hold_time) 
        if distance > record: break

    return perms - (2 * hold_time)


def product_of_wins(races):

    return reduce(lambda x,y: x*y, [calc_winning_perms(d,r) for d,r in races])


def main(filepath):

    part_1, part_2 = parse_input(filepath)

    return product_of_wins(part_1), product_of_wins(part_2)

print(main('06.txt'))