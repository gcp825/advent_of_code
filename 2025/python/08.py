from functools import reduce

def parse_input(filepath):

    return [tuple(map(int,x.split(','))) for x in open(filepath).read().split('\n')]


def euclidean(a,b):

    return sum([abs(b[0]-a[0])**2, abs(b[1]-a[1])**2, abs(b[2]-a[2])**2])


def calculate_distances(boxes):

    return [(euclidean(a,b),a,b) for i,a in enumerate(boxes) for j,b in enumerate(boxes) if i < j]


def join_boxes(circuits,a,b):

    one = circuits.pop([i for i,x in enumerate(circuits) if a in x][0])
    two = set() if b in one else circuits.pop([i for i,y in enumerate(circuits) if b in y][0])

    return circuits + [one|two]


def solve(boxes):

    circuits, largest = [{x} for x in boxes], [1]
    distances = [(a,b) for _,a,b in sorted(calculate_distances(boxes))]

    while len(circuits) > 1:
        box_a, box_b = distances.pop(0)
        circuits = join_boxes(circuits, box_a, box_b)
        largest += [reduce(lambda x,y: x*y, list(sorted([len(x) for x in circuits]))[-3:])]

    return largest[1000], box_a[0] * box_b[0]


def main(filepath):

    return solve(parse_input(filepath))


print(main('08.txt'))