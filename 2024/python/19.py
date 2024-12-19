from collections import defaultdict

def parse_input(f):

    return [(t.rstrip('\n').split(', '), p.split('\n')) for t,p in [tuple(open(f).read().split('\n\n'))]][0]


def solve(towels, patterns):

    viable_patterns, variations = set(), 0
    stripes = {len(towel) for towel in towels}

    for pattern in patterns:

        queue = [(pattern,1)]
        valid_towels = [t for t in towels if t in pattern]

        while queue:

            states = defaultdict(int)

            while queue:
                state, ct = queue.pop(0)
                new_states = [state[:-n] for n in stripes if n < len(state) and state[-n:] in valid_towels]
                for state in new_states:
                    states[state] += ct

            new_variations = sum(ct for state, ct in states.items() if state in valid_towels)

            if new_variations:
                viable_patterns.add(pattern)
                variations += new_variations

            queue = list(states.items())

    return len(viable_patterns), variations


def main(filepath):

    towels, patterns = parse_input(filepath)

    return solve(towels, patterns)


print(main('19.txt'))
