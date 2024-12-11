#  Some minor refactoring to use better names, only do one pass, and perform the number split mathematically,
#  thus removing the need for any string manipulation.

from collections import defaultdict
from math import floor, log10

def blink(stones,cycles):

    results = []

    for cycle in range(1, max(cycles)+1):

        new_stones = defaultdict(int)

        for stone_number, quantity in stones.items():

            if stone_number == 0:
                new_stones[1] += quantity
            else:
                digits = floor(log10(stone_number))+1
                if digits % 2 == 0:
                    new_stones[stone_number // 10**(digits//2)] += quantity
                    new_stones[stone_number % 10**(digits//2)]  += quantity
                else:
                    new_stones[stone_number * 2024] += quantity

        stones = new_stones
        if cycle in cycles:
            results += [sum(stones.values())]

    return tuple(results)


def main(filepath):

    stones = defaultdict(int)
    for stone_number in [int(x) for x in open(filepath).read().split()]:
        stones[stone_number] += 1

    return blink(stones,(25,75))


print(main('11.txt'))