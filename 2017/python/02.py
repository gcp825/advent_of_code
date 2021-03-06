def main(filepath):

    inp = [list(sorted(map(int,x)))[::-1] for x in [x.split('\t') for x in open(filepath,'r').read().split('\n')]]

    pt1 = sum([x[0]-x[-1] for x in inp])
    pt2 = 0
    for row in inp:
        for i, x in enumerate(row[:-1]):
            for y in row[i+1:]:
                if x%y==0:
                    pt2 += x//y
    return pt1, pt2

print(main('02.txt'))
