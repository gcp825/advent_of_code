import re

def parse_input(filepath):

    data = [chunk.split('\n') for chunk in open(filepath).read().split('\n\n')]

    return [''.join(p[1:]) for p in data[:-1]], [tuple(map(int,re.findall('\d+',line))) for line in data[-1]]


def does_it_fit(presents, regions, func):

    return {r for r in regions if r[0]*r[1] >= sum(func(p) * n for p,n in zip(presents, r[2:]))}


def main(filepath):

    presents, regions = parse_input(filepath)

    definitely_fit = does_it_fit(presents, regions, len)
    theoretically_fit = does_it_fit(presents, regions, lambda x: x.count('#'))

    if len(theoretically_fit - definitely_fit) > 0:
        return "I guess I'll need to write the code implied by the puzzle description then..."

    return len(definitely_fit)


print(main('12.txt'))
