#  Fairly impenetrable, but much slicker than the brute force version used to get the stars. Will cope with multiple medians and 
#  non-integer means + crabs that don't begin at 0 on the x axis. Switched out the sum/range calc for part 2 with the triangular 
#  numbers formula (thanks oeis.org) + chucked in a nested list comprehension for good measure.
#  Possibly the most useful worked example in any AoC puzzle I've seen for working out what is happening mathematically.

def cost(crabs,func,average):

    return min([sum([func(x,y) for x in crabs]) for y in average(crabs)])

def main(filepath):

    input = sorted([int(x) for x in open(filepath,'r').read().split(',')])
    crabs = [x-input[0] for x in input] 

    linear     = lambda x,y: abs(x-y)
    triangular = lambda x,y: abs(x-y)*(abs(x-y)+1)//2
    medians    = lambda x:   set([x[(len(x)-y)//2] for y in (0,1)])
    means      = lambda x:   set([(sum(x)//len(x))+y for y in (0,min(1,sum(x)%len(x)))])

    return cost(crabs,linear,medians), cost(crabs,triangular,means)

print(main('07.txt'))