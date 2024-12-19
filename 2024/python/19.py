from collections import defaultdict

def parse_input(f):

    return [(t.rstrip('\n').split(', '), p.split('\n')) for t,p in [tuple(open(f).read().split('\n\n'))]][0]


def solve(towels, patterns):

    stripes = {len(towel) for towel in towels}
    possible_patterns, total_variations = (0,0)

    for pattern in patterns:

        valid_towels = [t for t in towels if t in pattern]
        variations = 0
        queue = [(pattern, 1)]

        while queue:
            states = defaultdict(int)
            while queue:
                state, occurences = queue.pop(0)
                for new_state in [state[:-n] for n in stripes if n < len(state) and state[-n:] in valid_towels]:
                    states[new_state] += occurences
            variations += sum(occurences for state, occurences in states.items() if state in valid_towels)
            queue = list(states.items())

        if variations:
            possible_patterns += 1
            total_variations += variations

    return possible_patterns, total_variations


def main(filepath):

    towels, patterns = parse_input(filepath)

    return solve(towels, patterns)


print(main('19.txt'))
