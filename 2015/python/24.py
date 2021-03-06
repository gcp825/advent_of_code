#  This is basically my part 1 solution... which does work for part 2 with my input (I gave it a whirl just to see).
#  However, it may not always work with all Part 2 input... lines 36-39 assume that if another combination with the target weight is found in the
#  remaining presents that the remaining presents excluding that combination can also  be subdivided into groups of the target weight. This will
#  always be the case for groups of three but may not necessarily be true for groups larger than that. However I'm feeling too lazy to refactor
#  this into a perfect solution right now!

from itertools import combinations
from functools import reduce
from operator  import mul

def calculate(presents,groups):
    
    valid = [];  group_weight = sum(presents) // groups

    weight = 0;  rng = 0
    for p in presents:
        weight += p;  rng += 1
        if weight > group_weight: break

    for r in range(rng):

        small_group = [c for c in combinations(presents,r) if sum(c) == group_weight]
        
        for x in small_group:            
            remainder = [p for p in presents if p not in x]

            weight = 0;  hi = 0
            for p in remainder:
                weight += p;  hi += 1
                if weight > group_weight: break
            weight = 0;  lo = 0
            for p in remainder[::-1]:
                weight += p;  lo += 1
                if weight > group_weight: lo -= 1;  break
            
            for i in range(lo,hi):
                if len([c for c in combinations(remainder,i) if sum(c) == group_weight]) > 0:
                    valid += [x]
                    break
                
        if len(valid) > 0: break
        
    return min([(reduce(mul,x),x) for x in valid])[::-1]


def main(groups):
    
    presents = [1,3,5,11,13,17,19,23,29,31,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
    return calculate(presents,groups)

print(main(3))
print(main(4))
