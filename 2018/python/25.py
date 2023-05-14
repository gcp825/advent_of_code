def manhattan(a,b): return sum([abs(a[n]-b[n]) for n in range(4)])

def main(filepath):

    coords = list(sorted([tuple(map(int,x.split(','))) for x in open(filepath).read().split('\n')]))
    paired = [(a,b) for i,a in enumerate(coords) for j,b in enumerate(coords) if i < j and manhattan(a,b) <= 3]

    constellations = [set([c]) for c in coords if c not in set([x[0] for x in paired]+[x[1] for x in paired])]

    while paired:
        constellation = set(paired.pop(0))
        indices = [i for i,(a,b) in enumerate(paired) if a in constellation or b in constellation][::-1]
        if indices:
            for i in indices: 
                constellation.update(paired.pop(i))
            paired = [tuple(constellation)] + paired
        else:
            constellations += [constellation]

    return len(constellations)
            

print(main('25.txt'))