def main(filepath):

    xform = str.maketrans(';',',','Glued man')
    input = [x[x.find(':')+1:]for x in open(filepath).read().translate(xform).replace('gr','g').split('\n')]
    cubes = [list(dict(sorted([(y[-1],int(y[:-1])) for y in x.split(',')])).values()) for x in input]

    return (sum([i+1 for i,(b,g,r) in enumerate(cubes) if b <= 14 and g <= 13 and r <= 12]),
            sum([b*g*r for (b,g,r) in cubes]))

print(main('02.txt'))