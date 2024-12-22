#  I'm sure there's a much quicker way to do this - there's likely a repeating pattern in there somewhere.
#  But not in the mood for analysing that given that I need to write Day 21 for the third time, so slightly
#  slow brute force is good enough for me!

from collections import defaultdict
from operator import floordiv, mod, mul, xor

def parse_input(filepath):

    return [int(x) for x in open(filepath).read().split('\n')]


def generate_number(number):

    for op, value in zip((mul, floordiv, mul), (64, 32, 2048)):
        number = mod(xor(number, op(number, value)), 16777216)

    return number


def main(filepath, part_1=0):

    initial_numbers = parse_input(filepath)
    total_bananas = defaultdict(int)

    for number in initial_numbers:

        numbers, diffs, bananas = [number], [], {}

        for i in range(2000):
            numbers += [generate_number(numbers[-1])]
            diffs += [numbers[-1] % 10 - numbers[-2] % 10]
            if i >= 3:
                if tuple(diffs[-4:]) not in bananas:
                    bananas[tuple(diffs[-4:])] = numbers[-1] % 10

        part_1 += numbers[-1]

        for sequence, count in bananas.items():
            total_bananas[sequence] += count

    return part_1, max(total_bananas.values())


print(main('22.txt'))