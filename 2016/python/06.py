from collections import Counter

def main(filepath):
    
    rows = [x for x in open(filepath,'r').read().split('\n')]
    cts  = [Counter(x) for x in [''.join(x) for x in [[row[i] for row in rows] for i in range(0,len(rows[0]))]]]   #  transpose to columns, concat then count characters
    pt1  = ''.join([x.most_common(1)[0][0] for x in cts])
    pt2  = ''.join([v for k,v in [min(x) for x in [[(v,k) for k,v in x.items()] for x in cts]]])

    return pt1, pt2

print(main('06.txt'))
