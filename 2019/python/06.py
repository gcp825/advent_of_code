def main(filepath):

    relationships = dict([tuple(x.split(')'))[::-1] for x in open(filepath,'r').read().split('\n')])
    
    queue = ['COM'];  orbits, depth = (0,1)
    you= [];  san = [];  a = 'YOU';  b = 'SAN'

    while len(queue) > 0:
        children = []
        for parent in queue:
            children += [c for c,p in relationships.items() if p == parent]
        orbits += len(children) * depth
        queue = children
        depth += 1

    while a != 'COM':  a = relationships[a];  you += [a]
    while b != 'COM':  b = relationships[b];  san += [b]
    common_ancestor = you[min(i for i,x in enumerate(you) if x in san)]
    xfers = you.index(common_ancestor) + san.index(common_ancestor)

    return orbits, xfers

print(main('06.txt'))
