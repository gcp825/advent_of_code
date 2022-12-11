# This is much tidier and coherent than my barely woken up first effort this morning.
# Nothing fancy... as usual, avoided recursion.

from functools import reduce

def autocomplete(line,map={'(':1,'[':2,'{':3,'<':4}): 
    
    return reduce(lambda x,y: (x*5)+y, [map[z] for z in line], 0)

def main(filepath):

    input = [x for x in open(filepath,'r').read().split('\n')] 
    pairs = ['()','[]','{}','<>']
    right = [x[1:] for x in pairs]
    scorer = dict(zip(right,[3,57,1197,25137]))
    scores = [[],[]]

    for line in input:

        i, invalid, length = (0,0,len(line)-1)

        while i < length:

            if   i == len(line)-1:      break
            elif line[i:i+2] in pairs:  line = line[:i] + line[i+2:];  i = max(0,i-1)
            elif line[i] in right:      invalid = scorer[line[i]]
            elif line[i+1] in right:    invalid = scorer[line[i+1]]
            else:                       i += 1

            if invalid > 0: break

        scores[min(1,invalid)] += [autocomplete(line[::-1]) if invalid == 0 else invalid]

    return sum(scores[1]), sorted(scores[0])[len(scores[0])//2]

print(main('10.txt'))