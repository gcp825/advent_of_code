def parse_input(f):

    data = [tuple(map(int,x.split('-'))) for x in open(f).read().split('\n') if x.isdigit() or '-' in x]

    return [x for x in data if len(x) == 2], [x[0] for x in data if len(x) == 1]


def compare_ranges(lo,hi,queue):

    return (lo, max(hi,queue[0][1]), queue[1:]) if lo <= queue[0][0] <= hi else (lo, hi, queue[1:] + queue[:1])


def consolidate_ranges(ranges):

    queue, consolidated = [] + list(sorted(ranges)), []

    while queue:
        lo, hi = queue.pop(0)
        for _ in range(len(queue)):
            lo, hi, queue = compare_ranges(lo,hi,queue)
        consolidated += [(lo,hi)]

    return consolidated


def main(filepath):

    raw_ranges, ids = parse_input(filepath)
    fresh = consolidate_ranges(raw_ranges)

    return sum(1 for i in ids for a,b in fresh if a <= i <= b), sum(b-a+1 for a,b in fresh)


print(main('05.txt'))