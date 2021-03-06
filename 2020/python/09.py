# quick and possibly dirty approach, but doesn't feel like any more obvious improvements really worth making

from itertools import combinations

def read_file(filepath):

    with open(filepath,'r') as i:
        nbrs = i.read().split('\n')

    return [int(i) for i in nbrs]


def find_invalid_nbr(nbrs, preamble_length):
        
    for i, nbr in enumerate(nbrs):
        
        if i > preamble_length - 1:
            
            stash = nbrs[(i - preamble_length): i]
            valid = [sum(pair) for pair in combinations(stash,2)]   #  likely a way of avoiding recalculating everything here... but not worth the effort!
            
            if nbr not in valid: return nbr
            
    return None
                

def find_contiguous_nbrs(nbrs, invalid_nbr):
 
    stash = []; x = 1
 
    for _, nbr in enumerate(nbrs):
        
        stash = [nbr] + stash + [nbrs[x]]
        
        while sum(stash) < invalid_nbr:
            x += 1
            stash += [nbrs[x]]
               
        if sum(stash) > invalid_nbr:     #  retain most of the contiguous number stash for the next pass: remove first item as we're
            stash = stash[2:-1]          #  moving on to the next input val + 2nd & last items as they'll be re-added at the top of the loop       
            
        if sum(stash) == invalid_nbr:
            return min(stash) + max(stash)

    return None
        
        
def main(preamble_length, filepath):
    
    nbrs = read_file(filepath)
    i = find_invalid_nbr(nbrs, preamble_length)
    s = find_contiguous_nbrs(nbrs,i)
    
    return i,s
    
print(main(25,'xmas.txt'))
