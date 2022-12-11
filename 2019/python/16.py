#  Slow. But who cares? This one is a pretty pointless activity in spotting a pattern in some numbers to get the second star.

from itertools import chain
from collections import deque

def part1(pt1):

    update = []
    for n in range(len(pt1)):
        pattern = list(chain(*[[x]*(n+1) for x in [0,1,0,-1]]))
        pattern = (pattern*((len(pt1)//len(pattern))+2))[1:len(pt1)+1]
        update += [int(str(sum([x*pattern[i] for i,x in enumerate(pt1)]))[-1:])]
    return update

def part2(pt2,last=0):

    for _ in range(len(pt2)):
        last = (pt2.popleft()+last)%10
        pt2.append(last)
    return pt2

def main(f):

    data = open(f,'r').read().strip('\n')
    pt1 = list(map(int,list(data)))
    pt2 = deque(map(int,list((data*10000)[int(data[:7]):][::-1])))

    for _ in range(100):
        pt1 = part1(pt1)
        pt2 = part2(pt2)

    return ''.join(map(str,pt1[:8])), ''.join(map(str,list(pt2)[-8:][::-1]))

print(main('16.txt'))
