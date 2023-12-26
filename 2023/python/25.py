from heapq import heapify, heappush, heappop
from itertools import combinations
from random import shuffle

def parse_input(f):

    input = [(x,y.split(' ')) for x,y in [z.split(': ') for z in open(f).read().split('\n')]]
    links = list(sorted([tuple(sorted((frm,to))) for frm, array in input for to in array]))

    adjacencies = {}
    for a,b in links:
        adjacencies[a] = adjacencies.get(a,[]) + [b]
        adjacencies[b] = adjacencies.get(b,[]) + [a]

    return adjacencies, links


def dijkstra(start,finish,adjacencies):
    
    visited = {start:0}
    queue = [(0,[start])];  heapify(queue)

    while queue:
        steps, trail = heappop(queue)
        current = trail[-1]
        if current == finish: break
        else:
            steps += 1
            for node in adjacencies[current]:
                if steps < visited.get(node,steps+1):
                    visited[node] = steps
                    heappush(queue,(steps,[] + trail + [node]))

    return trail


def rank_edges(paths):

    ranks = {}
    for path in paths:
        updates = [(k,ranks.get(k,0)+1) for k in [tuple(sorted((a,b))) for a,b in zip(path[:-1],path[1:])]]
        ranks.update(updates)

    return [edge[1] for edge in sorted([(v,k) for k,v in ranks.items()])][::-1]


def try_cut(remove,original_edges):

    edges  = list(sorted(list(set(original_edges).difference(remove))))
    groups = [];  g = 0

    while edges:

        if len(groups) == g:
            groups += [[*edges.pop(0)]]

        if g >= 2: break
        else:
            new_edges = []
            i = len(edges)-1

            while i >= 0:
                a,b = edges[i]
                if a in groups[g] and b not in groups[g]:  groups[g] += [b]
                if b in groups[g] and a not in groups[g]:  groups[g] += [a]
                if a in groups[g] and b in groups[g]:      new_edges  = [edges.pop(i)]
                i -= 1

            if not new_edges: g += 1

    return groups


def sample_cuts(adjacencies,edges):

    nodes = list(adjacencies.keys())
    sample_size = max(200,len(nodes)//10)
    high_ranking_combos = combinations(range(5),3)

    while True:

        shortest_paths = []

        if len(nodes) > 30:
            for _ in range(sample_size):
                shuffle(nodes)
                shortest_paths += [dijkstra(nodes[0],nodes[-1],adjacencies)]
        else:
            shortest_paths += [dijkstra(a,b,adjacencies) for i,a in enumerate(nodes[:-1]) for b in nodes[i+1:]]

        ranked_edges = rank_edges(shortest_paths)
        likely_combos = [(ranked_edges[a],ranked_edges[b],ranked_edges[c]) for a,b,c in high_ranking_combos]
   
        for combo in likely_combos:
            groups = try_cut(combo,edges)
            if len(groups) == 2: break

        if len(groups) == 2: break

    return len(groups[0]) * len(groups[1])


def main(filepath):

    adjacencies, edges = parse_input(filepath)
    result = sample_cuts(adjacencies,edges)

    return result

print(main('25.txt'))
