def main(filepath):

    listing = open(filepath,'r').read().split('\n')

    path, directories, sizes = [], dict(), dict()

    for line in listing:

        if   line == '$ cd /':     path = ['/']
        elif line == '$ cd ..':    path = path[:-1] 
        elif line[:4] == '$ cd':   path += [line[5:]]
        elif line == '$ ls':       pass
        else:
            if line[0:3] == 'dir':        
                item = path + [line[4:]] 
            else:
                item = tuple(line.split(' ')[::-1])

            directories[tuple(path)] = directories.get(tuple(path),[]) + [item]


    for dir in [x[1] for x in list(sorted([(len(path),path) for path in directories.keys()]))[::-1]]:

        sizes[dir] = sum([int(item[1]) if type(item) is tuple else sizes[tuple(item)] for item in directories[dir]])

    required_space = 3*10**7 - (7*10**7 - sizes[('/',)])


    return sum([x for x in sizes.values() if x <= 10**5]), list(sorted([x for x in sizes.values() if x >= required_space]))[0]

print(main('07.txt'))