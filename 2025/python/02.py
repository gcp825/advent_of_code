def parse_input(filepath):

    ranges = [tuple(map(int,x)) for x in [y.split('-') for y in open(filepath).read().split(',')]]

    return [range(x[0], x[1]+1) for x in ranges], len(str(max(x[1] for x in ranges)))


def get_matches(ranges, divisors):

    matches = []
    for num, length in [(str(n), len(str(n))) for num_range in ranges for n in num_range]:
        for divisor in divisors[length]:
            if num == num[:divisor] * (length // divisor):
                matches += [int(num)]
                break
    return matches


def main(filepath):

    ranges, max_length = parse_input(filepath)

    all_divisors = {n : [d for d in range(1,n) if n%d == 0][::-1] for n in range(1,max_length+1)}
    divisors = [{k : [n for n in v if n*2 == k] for k,v in all_divisors.items()}, all_divisors]

    return tuple(sum(get_matches(ranges,d)) for d in divisors)


print(main('02.txt'))