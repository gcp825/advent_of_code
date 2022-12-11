def main(filepath):

    score = lambda x: ord(x)-96 if x.islower() else ord(x)-38

    groups = [tuple(x[i:i+3:]) for x in [open(filepath).read().split('\n')] for i in range(0,len(x),3)]

    misplaced = [list(set(a).intersection(b))[0] for group in groups for bag in group for a,b in [(bag[:len(bag)//2],bag[len(bag)//2:])]]
    badges    = [list(set(a).intersection(b).intersection(c))[0] for group in groups for a,b,c in [group]]

    return sum([score(x) for x in misplaced]), sum([score(x) for x in badges])

print(main('03.txt'))