def main(filepath):

    one, two = tuple(map(sorted, zip(*[map(int, line.split()) for line in open(filepath).read().split('\n')])))

    pt1 = sum([abs(b-a) for a,b in zip(one, two)])
    pt2 = sum([a*two.count(a) for a in one])

    return pt1, pt2

print(main('01.txt'))