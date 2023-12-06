# That was tough for Day 5... but: Sampling + Brute Force = Good Enough

def parse_input(filepath):

    input = [x.split('\n') for x in open(filepath).read().split('\n\n')]
    seeds = parse_numbers(input[0][0].split(':')[-1])
    maps = [[parse_numbers(n) for n in m] for m in [x[1:] for x in input[1:]]]

    return seeds, list(zip(seeds[::2],seeds[1::2])), maps


def parse_numbers(raw_numbers):

    return tuple([int(n) for n in raw_numbers.strip().split(' ')])


def calculate_sample_stride(total, sample_size):

    ct = sum([v for _,v in total]) if type(total) is list else total

    return 1 if ct <= sample_size else int(ct/sample_size)


def find_location(seeds, maps):

    min_location = 99**99

    for seed in seeds:
        sequence = [seed]
        for mapping in maps:
            sequence += [get_destination(sequence[-1], mapping)]
        min_location = min(min_location, sequence[-1])

    return min_location


def get_destination(src, mapping):

    matches = [src+(d-s) for d,s,l in mapping if s <= src <= (s+l-1)]

    return matches[0] if matches else src


def sample_seeds(seed_ranges, maps, sample_size):

    samples = []
    stride = calculate_sample_stride(seed_ranges, sample_size)

    for start,values in seed_ranges:
        samples += list(range(start, start + values, stride)) + [start + values - 1]

    print(f"Sampling {len(samples)} seed values to establish initial upper search boundary")

    return find_location(samples, maps)


def sample_locations(upper_bound, seed_ranges, maps, sample_size):

    stride = calculate_sample_stride(upper_bound, sample_size)
    samples = list(range(0, upper_bound + 1, stride))

    print(f"Sampling {len(samples)} location values to establish final search boundaries")

    for location in samples:
        if valid_seed(location, seed_ranges, maps): break

    lower_bound = max(0,location - 10**6)  # Set lower bound at 1 million below the first valid sample location

    return lower_bound, location


def valid_seed(location, seed_ranges, maps):

    sequence = [location]
    for mapping in maps:
        sequence += [get_source(sequence[-1], mapping)]
        
    valid = [1 for start, values in seed_ranges if start <= sequence[-1] <= (start + values - 1)]

    return True if valid else False


def get_source(dest, mapping):

    matches = [dest+(s-d) for d,s,l in mapping if d <= dest <= (d+l-1)]

    return matches[0] if matches else dest


def find_location_between_bounds(lower_bound, upper_bound, seed_ranges, maps):

    print(f"Checking locations {lower_bound} to {upper_bound} for the first location corresponding to an input seed")

    for location in range(lower_bound, upper_bound + 1):
        if valid_seed(location, seed_ranges, maps): break

    return location


def main(filepath, approx_sample_size=100000):

    seeds, seed_ranges, maps = parse_input(filepath)

    part_1 = find_location(seeds, maps)

    upper_bound = sample_seeds(seed_ranges, maps, approx_sample_size)
    bounds = sample_locations(upper_bound, seed_ranges, maps[::-1], approx_sample_size)

    part_2 = find_location_between_bounds(*bounds, seed_ranges, maps[::-1])

    return part_1, part_2


print(main('05.txt'))