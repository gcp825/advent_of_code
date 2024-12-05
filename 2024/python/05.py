from collections import Counter

def ordered(update, rules):

    return False if [1 for i,x in enumerate(update[:-1]) if update[i:i+2] not in rules] else True


def order(update, rules):

    counts = Counter(list(update) + [p for p in update for x,y in rules if p == x and y in update])

    return tuple(k for _,k in sorted((v,k) for k,v in counts.items())[::-1])


def main(filepath):

    input = [(r.split('\n'), u.split('\n')) for r,u in [tuple(open(filepath).read().split('\n\n'))]][0]
    rules = set(tuple(map(int,r.split('|'))) for r in input[0])
    updates = [tuple(map(int,u.split(','))) for u in input[1]]

    correct = sum(u[len(u)//2] for u in [u for u in updates if ordered(u,rules)])
    corrected = sum(u[len(u)//2] for u in [order(u,rules) for u in updates if not ordered(u,rules)])

    return correct, corrected

print(main('05.txt'))