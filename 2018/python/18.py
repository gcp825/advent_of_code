def setup_grid(filepath):
    
    grid = [((y,x),val) for y,row in enumerate(open(filepath).read().split('\n')) for x,val in enumerate(row)]

    acres = set([k for k,v in grid if v == '.'])
    trees = set([k for k,v in grid if v == '|'])
    yards = set([k for k,v in grid if v == '#'])

    return acres, trees, yards


def count(s,y,x): 
    
    return len(list(s.intersection([(y-1,x-1),(y-1,x),(y-1,x+1),(y,x-1),(y,x+1),(y+1,x-1),(y+1,x),(y+1,x+1)])))


def cycle(acres,trees,yards,minutes):

    results, m = (dict(), 0)

    while m < minutes:

        new_acres = set([c for c in yards if count(trees,*c) == 0 or count(yards,*c) == 0])
        new_trees = set([c for c in acres if count(trees,*c) >= 3])
        new_yards = set([c for c in trees if count(yards,*c) >= 3])

        acres = new_acres.union([c for c in acres if c not in new_trees])  
        trees = new_trees.union([c for c in trees if c not in new_yards])
        yards = new_yards.union([c for c in yards if c not in new_acres])

        m, results = fast_forward(m,minutes,results,trees,yards)

        m += 1

    return len(list(trees)) * len(list(yards))


def fast_forward(m,minutes,results,trees,yards):

    if m > 500:
        result = len(list(trees)) * len(list(yards))
        if result in results:
            m = minutes - ((minutes-m) % (m-results[result]))
            results = dict()
        else:
            results[result] = m

    return m, results    
    
     
def main(filepath):
    
    pt1 = cycle(*setup_grid(filepath),10)
    pt2 = cycle(*setup_grid(filepath),1000000000)
    
    return pt1, pt2
    
print(main('18.txt'))