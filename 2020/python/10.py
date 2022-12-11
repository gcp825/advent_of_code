# Completely lost my mind on part 2 of this... yet the end result is so simple. Ridiculous.
# Am still convinced there's a solution that's just a pure mathematical equation.

from collections import Counter, defaultdict

def read_file(filepath):

    with open(filepath,'r') as i:
        nbrs = i.read().split('\n')

    return [int(i) for i in nbrs]

def format_input(data):

    d = sorted(data)
    return [0] + d + [d[-1]+3]

def part1(jolts):
    
    diffs = []

    for i, nbr in enumerate(jolts):
        if i > 0:
            diffs.append(nbr - jolts[i-1])

    count = Counter([x for x in diffs])

    return count[1]*count[3]

def part2(jolts):

    ends = defaultdict(int)                      # stores the end number of a sequence and the running
    ends[0] += 1                                 # total of sequences ending with that number

    target = jolts[-2]
    i = 1

    while jolts[i] <= target:
    
        valid_additions = [j for j in jolts[i:i+3] if j <= (jolts[i]+2)]
    
        stash = defaultdict(int)                 # working dict
    
        for n,ct in ends.items():            
            
            if n == valid_additions[-1]:         # for each previous sequence end point that can't be added to in this pass but
                stash[n] += ct                   # could be added to in a future pass, pass the existing totals to the stash
            else:            
                for v in valid_additions:        # for each previous sequence end point that can be extended in this pass,
                    if n < v <= (n + 3):         # assign the previous running total to the new sequence end point(s)
                        stash[v] += ct           
                    
        ends = stash                             # replace the master running totals with the new calculations
        i += 1                               
        
    return ends[target]

def main(filepath):
    
    j = format_input(read_file(filepath))
    a = part1(j)
    b = part2(j)
    
    return a,b


print(main('jolts.txt'))
