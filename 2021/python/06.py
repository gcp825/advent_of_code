# Well, this is infinitely better than the trash I wrote this morning, and spent forever over (trying to determine some magical mathematical formula).
# Refactored to use neat file parsing trick and make deque operations clearer.

from collections import deque

def spawn(fishes, cycles):

    for _ in range(cycles):
        fishes.rotate(-1)            # shift all one position left, [0] moves to the end [8) - representing new spawn
        fishes[6] += fishes[8]       # add [8] to [6] to add recent parents back into the rotation
    return sum(fishes)

def main(filepath):

    fishes = deque([*map(open(filepath,'r').read().count,'012345678')])

    return spawn(fishes,80), spawn(fishes,256-80)

print(main('06.txt'))