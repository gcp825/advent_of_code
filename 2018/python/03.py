from collections import Counter

def main(filepath):
    
    claims = [tuple(map(int,x.translate(x.maketrans('@:x',',,,',' #')).split(','))) for x in open(filepath,'r').read().split('\n')]
    counts = Counter([(a,b) for _,x,y,width,height in claims for a in range(x,x+width) for b in range(y,y+height)])

    for claim_nbr,x,y,width,height in claims:

        sq_inches  = [(a,b) for a in range(x,x+width) for b in range(y,y+height)]
        occurences = sum([counts[x] for x in sq_inches])

        if len(sq_inches) == occurences: break

    return len([k for k,v in counts.items() if v >= 2]), claim_nbr    
    
print(main('03.txt'))