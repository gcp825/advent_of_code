# Similar to a bunch of previous puzzles, but rather than reuse any old code, I wrote this from scratch with a conscious attempt to write any grid updates as
# list comprehensions, rather than explicitly looping over and incrementing items one by one. This has kept the code pretty tight and there's really nothing
# to refactor. The smaller worked example was sooo useful for spotting the need to increment by the NUMBER of adjacent flashing octopodes in each sub-step.

from itertools import product
from collections import Counter

def count_flashers(grid,part,cycles=99*99):

    adjacent = list(product((0,1,-1),repeat=2))[1:]
    flasher_ct, octopodes = (0,len(grid))

    for step in range(1,cycles+1):

        grid = [(k,v+1) for k,v in grid]
        flashers = set()

        while True:

            new_flashers = [k for k,v in grid if v > 9 and k not in flashers]

            if len(new_flashers) > 0:

                increases = Counter([tuple(map(sum,zip(a,b))) for a,b in product(new_flashers,adjacent)])
                grid = [(k,v+increases.get(k,0)) for k,v in grid]
                flashers.update(new_flashers)

            else:
                grid = [(k,0 if v>9 else v) for k,v in grid]
                flasher_ct += len(flashers)
                break

        if part == 2 and len(flashers) == octopodes: break

    return flasher_ct, step
        
def main(filepath):

    grid = [((y,x),int(v)) for y, row in enumerate(open(filepath,'r').read().split('\n')) for x,v in enumerate(row)]

    return count_flashers(grid,1,100)[0], count_flashers(grid,2)[1]
    
print(main('11.txt'))
