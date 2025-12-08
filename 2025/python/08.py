from functools import reduce
from itertools import combinations
from math import dist


def parse_input(filepath):

    return [tuple(map(int,line.split(','))) for line in open(filepath).read().split('\n')]


def pairs_by_distance(boxes):

    return list(sorted(combinations(boxes,2), key=lambda x: dist(*x)))


def join_boxes(circuits,a,b):

    one, two = tuple([c for c in circuits if box in c][0] for box in (a,b))

    return [c for c in circuits if c not in (one,two)] + [one|two]


def solve(boxes):

    circuits, largest_3_circuits = [{box} for box in boxes], [1]

    for box_a, box_b in pairs_by_distance(boxes):
        circuits = join_boxes(circuits,box_a,box_b)
        largest_3_circuits += [reduce(lambda x,y: x*y, list(sorted([len(x) for x in circuits]))[-3:])]
        if len(circuits) == 1: break

    return largest_3_circuits[1000], box_a[0] * box_b[0]


def main(filepath):

    return solve(parse_input(filepath))


print(main('08.txt'))