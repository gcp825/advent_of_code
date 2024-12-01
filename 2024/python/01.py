def main(filepath):

    one, two = tuple(map(sorted, zip(*[map(int, line.split()) for line in open(filepath).read().split('\n')])))

    return sum([abs(b-a) for a,b in zip(one, two)]), sum([a*two.count(a) for a in one])

print(main('01.txt'))