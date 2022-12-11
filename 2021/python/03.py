# Refactored to genericize as much as possible, clean up the tie break logic & use a much cleaner transpose approach (thanks for that one Darren!)

from collections import Counter

def transpose(nbrs): return list(zip(*nbrs))

def get_rate(nbrs,i): return int(''.join([Counter(list(n)).most_common()[i][0] for n in transpose(nbrs)]),2)

def get_rating(nbrs,minmax):

    i, j = (0, minmax(-1,0))

    while len(nbrs) > 1:
        digits, cts = zip(*Counter(list(transpose(nbrs)[i])).most_common())
        filter_value = digits[j] if cts[0] != cts[-1] else minmax(digits)
        nbrs = [x for x in nbrs if x[i] == filter_value]
        i += 1

    return int(nbrs[0],2)   

def main(filepath):

    nbrs = [x for x in open(filepath,'r').read().split('\n')]

    return get_rate(nbrs,0) * get_rate(nbrs,-1),  get_rating(nbrs,max) * get_rating(nbrs,min)

print(main('03.txt'))