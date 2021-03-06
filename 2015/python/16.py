from collections import namedtuple

def read_file(filepath,Sue):
    
    with open(filepath,'r') as f:
        
        sues = []
        for x in f.read().replace('Sue ','').split('\n'):
            facts = [f.split(': ') for f in x[x.find(':')+2:].split(', ')]
            f = {}
            for fact in facts: f[fact[0]] = int(fact[1])
                
            sues += [Sue(int(x[0:x.find(':')]), f.get('akitas',-1), f.get('cars',-1), f.get('cats',-1), f.get('children',-1),
                         f.get('goldfish',-1), f.get('perfumes',-1), f.get('pomeranians',-1), f.get('samoyeds',-1), f.get('trees',-1), f.get('vizslas',-1))]

    return sues

def match_sues(target,sues,mode):

    matches = []
    for sue in sues:
        if ((sue.akitas == target.akitas or sue.akitas < 0)
        and (sue.cars == target.cars or sue.cars < 0)
        and ((mode == 1 and (sue.cats == target.cats or sue.cats < 0)) or (mode == 2 and (sue.cats > target.cats or sue.cats < 0)))
        and (sue.children == target.children or sue.children < 0)
        and ((mode == 1 and (sue.goldfish == target.goldfish or sue.goldfish < 0)) or (mode == 2 and (sue.goldfish < target.goldfish or sue.goldfish < 0)))
        and (sue.perfumes == target.perfumes or sue.perfumes < 0)
        and ((mode == 1 and (sue.pomeranians == target.pomeranians or sue.pomeranians < 0)) or (mode == 2 and (sue.pomeranians < target.pomeranians or sue.pomeranians < 0)))
        and (sue.samoyeds == target.samoyeds or sue.samoyeds < 0)
        and ((mode == 1 and (sue.trees == target.trees or sue.trees < 0)) or (mode == 2 and (sue.trees > target.trees or sue.trees < 0)))
        and (sue.vizslas == target.vizslas or sue.vizslas < 0)):
            break
    
    return sue.nbr

def main(filepath,facts):
    
    Sue = namedtuple('Sue','nbr akitas cars cats children goldfish perfumes pomeranians samoyeds trees vizslas')
    target = Sue(0,*facts)
    sues   = read_file(filepath,Sue)
    sue1   = match_sues(target,sues,1)
    sue2   = match_sues(target,sues,2)

    return sue1, sue2

print(main('16.txt',(0,2,7,3,5,1,3,2,3,0)))
