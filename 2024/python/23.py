#  AoC fatigue has set in, so the slowest, laziest, untuned brute-force you'll ever see.
#  It's so dumb, it might be the worst solution I've ever written, but quick to write!

from collections import defaultdict

def parse_input(filepath):

    return [tuple(x.split('-')) for x in open(filepath).read().split('\n')]


def map_links(connections):

    links = defaultdict(set)

    for a,b in connections:
        links[a].add(b)
        links[b].add(a)

    return list(sorted(links.items()))


def groups_of_three(links):

    groups = []

    for i, (one, a) in enumerate(links):
        for two, b in links[i+1:]:
            if two in a:
                threes = a.intersection(b)
                for three in threes:
                    if two < three:
                        groups += [(one,two,three)]
    return groups


def most_connected(links, groups):

    queue = groups

    while queue:
        print(f"Items in Groups: {len(queue[0])}, Length of Queue: {len(queue)}")
        new_queue = set()
        while queue:
            group = queue.pop(0)
            for node, links_from in links:
                if node not in group:
                    intersect = links_from.intersection(group)
                    if len(intersect) == len(group):
                        new_group = tuple(sorted((*group, node)))
                        new_queue.add(new_group)

        queue = list(new_queue)

    return ','.join(sorted(group))


def main(filepath):

    connections = parse_input(filepath)
    links = map_links(connections)
    groups = groups_of_three(links)
    password = most_connected(links, [] + groups)

    return sum(1 for grp in groups if 't' in [x[0] for x in grp]), password


print(main('23.txt'))