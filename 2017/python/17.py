#  So, I could use maths... but deque just makes this too easy (albeit slow) to brute force.

from collections import deque

def main(rotations,inserts,after):

    buffer = deque([0]);  rotations = -(rotations+1)

    for n in range(inserts):
        buffer.rotate(rotations)
        buffer.extendleft([n+1])
 
    return buffer[(buffer.index(after)+1)%inserts]

print(main(345,2017,2017))
print(main(345,5*10**7,0))
