from collections import defaultdict

def blink(stones,cycles):

    for _ in range(cycles):

        current = stones.items()
        stones = defaultdict(int)

        for stone, count in current:

            if stone == '0':
                stones['1'] += count

            elif len(stone)%2 == 0:
                stones[stone[:len(stone)//2]] += count
                stones[str(int(stone[len(stone)//2:]))] += count

            else:
                stones[str(int(stone)*2024)] += count

    return sum(stones.values())


def main(filepath):

    stones = defaultdict(int)
    for stone in [x for x in open(filepath).read().split()]:
        stones[stone] += 1

    return tuple(blink(stones,n) for n in (25,75))


print(main('11.txt'))