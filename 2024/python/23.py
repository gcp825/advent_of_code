from collections import defaultdict

def parse_input(filepath):

    links = defaultdict(set)

    for a,b in [tuple(x.split('-')) for x in open(filepath).read().split('\n')]:
        links[a].add(b)
        links[b].add(a)

    return links


def groups_of_three(links):

    groups = []
    for a in links:
        for b in [b for b in links[a] if a < b]:
            for c in [c for c in links[b] if b < c and c in links[a]]:
                groups += [(a,b,c)]
    return groups


def maximum_clique(groups, links):

    queue = [set(g) for g in groups]
    cliques = []

    while queue:
        a = queue.pop(0)
        for b in queue:
            for computer in a:
                if computer not in b:
                    match = sum(1 for x,y,z in [b] if computer in links[x] and computer in links[y] and computer in links[z])
                    if not match: break
            if match:
                a.update(b)
                queue.remove(b)
        cliques.append(a)

    return ','.join(sorted(max(cliques,key=len)))


def main(filepath):

    links = parse_input(filepath)
    groups = groups_of_three(links)
    password = maximum_clique(groups,links)

    return sum(1 for grp in groups if 't' in [x[0] for x in grp]), password


print(timer(main,'23.txt'))