from itertools import combinations

def read_file(filepath):
    
    return sorted([int(x) for x in open(filepath,'r').read().split('\n')])

def main(filepath,volume):

    combos = []
    containers = read_file(filepath)
    for n in range(1,len(containers)+1):
        combos += [x for x in combinations(containers,n) if sum(x) == volume]
        
    return len(combos), len([x for x in combos if len(x) == min([len(x) for x in combos])])

print(main('17.txt',150))
