from collections import Counter
from difflib import get_close_matches

def main(filepath):
    
    boxes   = [x for x in open(filepath,'r').read().split('\n')]
    counter = lambda x,y: [k for k,v in Counter(x).items() if v == y]
    counts  = list(map(sum,zip(*[(min(len(counter(b,2)),1),min(len(counter(b,3)),1)) for b in boxes])))

    for i,box in enumerate(boxes):
        match = get_close_matches(box,boxes[i+1:],1,(len(box)-1)/len(box))
        if len(match) > 0: break

    pt2 = ''.join([box[i] for i in range(len(box)) if box[i] == match[0][i]])
    
    return counts[0]*counts[1], pt2
    
print(main('02.txt'))