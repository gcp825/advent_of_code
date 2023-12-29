# Not speedy, but good enough.

def parse_input(filepath):

    locations = [((y,x),col) for y,row in enumerate(open(filepath).read().split('\n')) for x,col in enumerate(row)]
    path   = set([c for c,x in locations if x != '#'])
    slopes = tuple([(c,x) for c,x in locations if x in '^v<>'])

    return path, slopes


def moves(y,x,slopes):

    slopes = dict(list(slopes))
    possible = [((y-1,x),'^'), ((y,x+1),'>'), ((y+1,x),'v'), ((y,x-1),'<')]

    return [(c, False if c not in slopes or d == slopes[c] else True, 
                False if c not in slopes or d != slopes[c] else True) for c,d in possible]


def shrink_grid(path,slopes):

    nodes = determine_nodes(path,slopes)
    edges, uphill = collapse_edges(*determine_edges(nodes,path,slopes))
    links = link_nodes(edges)
    distances = dict([(termini, len(visited)-1) for termini, visited in edges])

    return links, distances, uphill


def determine_nodes(path,slopes):

    nodes = [coords for coords in path if len([c for c,_,_ in moves(*coords,slopes) if c in path or c in slopes]) > 2]

    return [min(path), max(path)] + nodes


def determine_edges(nodes,path,slopes):

    edges = [];  hills = {};  unmapped = [] + nodes

    while unmapped:

        start = unmapped.pop(0)
        queue = [([start],(False,False))]

        while queue:

            visited, hill = queue.pop(0)
            current = visited[-1]

            if current in nodes and current != start:
                edges += [((start,current), visited)]
                hills[(start,current)] = hill
            else:
                next_moves = [c for c in moves(*current,slopes) if c[0] in path and c[0] not in visited]
                for coords, uphill, downhill in next_moves:
                    queue += [([] + visited + [coords], (max(uphill,hill[0]), max(downhill,hill[1])))]

    return edges, hills


def collapse_edges(edges,hills):

    updated_edges = [];  collapse = [];  consecutive = 1;  i = 1

    while i <= len(edges):
        if ((i < len(edges) and edges[i][0][0] == edges[i-1][0][0])
        or (i == len(edges) and edges[i-1][0][0] == edges[i-2][0][0])
        or consecutive > 1):
            consecutive = 1 if i == len(edges) or edges[i][0][0] != edges[i-1][0][0] else consecutive + 1
            updated_edges += [edges[i-1]]
        else:
            consecutive = 1
            if i > 0:  collapse += [edges[i-1]]
        i += 1

    edges = [] + updated_edges

    for (a,b), trail in collapse:
        updated_edges = [];  u1,d1 = hills[(a,b)]
        for (c,d), path in edges:
            u2,d2 = hills[(c,d)]
            if b == c:
                if a != d:
                    updated_edges += [((a,d),trail[:-1]+path)]
                    hills[(a,d)] = (max(u1,u2), max(d1,d2))
            elif b == d:
                if c != a:
                    updated_edges += [((c,a),path+trail[:-1][::-1])]
                    hills[(c,a)] = (max(d1,u2), max(u1,d2))
            else:
                updated_edges += [((c,d),path)]
        edges = [] + updated_edges

    return edges, dict([(k,v[0]) for k,v in hills.items()])


def link_nodes(edges):

    links = {}
    for (a,b), _ in sorted(edges):
        links[a] = links.get(a,[]) + [b]

    return links


def calculate_longest_path(links, distances, uphill):

    start = min(links);  target = max(links);  longest_downhill, longest = (0,0)
    stack = [(start, set([start]), 0, False)]

    while stack:

        previous, visited, steps, up_hill = stack.pop(-1)

        for node in [n for n in links[previous] if n not in visited]: 
            edge = (previous,node)
            distance = steps + distances[edge]
            if node == target:
                longest_downhill = max(0 if up_hill else distance, longest_downhill)
                longest = max(distance, longest)
            else:
                stack += [(node, visited.union([node]), distance, max(up_hill, uphill[edge]))]

    return longest_downhill, longest

 
def main(filepath):

    grid = shrink_grid(*parse_input(filepath))
    longest_downhill, longest = calculate_longest_path(*grid)

    return longest_downhill, longest


print(main('23.txt'))
