# Not speedy, but good enough. Haven't attempted to refactor Part 1 to utilise the Part 2 solution.

def parse_input(filepath):

    locations = [((y,x),col) for y,row in enumerate(open(filepath).read().split('\n')) for x,col in enumerate(row)]
    path   = set([c for c,x in locations if x != '#'])
    slopes = tuple([(c,x) for c,x in locations if x in '^v<>'])

    return path, slopes


def moves(y,x,slopes,avoid_uphill):

    slopes = dict(list(slopes))
    possible = [((y-1,x),'^'), ((y,x+1),'>'), ((y+1,x),'v'), ((y,x-1),'<')] 

    return [c for c,d in possible if c not in slopes or not avoid_uphill or d == slopes[c]]


def shrink_grid(path,slopes,avoid_uphill):

    nodes = determine_nodes(path,slopes,avoid_uphill)
    edges = collapse_edges(determine_edges(nodes,path,slopes,avoid_uphill))
    links = link_nodes(edges)

    return edges, links


def determine_nodes(path,slopes,avoid_uphill):

    nodes = [coords for coords in path if len([c for c in moves(*coords,slopes,avoid_uphill) if c in path or c in slopes]) > 2]

    return [min(path), max(path)] + nodes


def determine_edges(nodes, path, slopes, avoid_uphill):

    edges = [];  unmapped = [] + nodes

    while unmapped:

        start = unmapped.pop(0)
        queue = [[start]]

        while queue:

            visited = queue.pop(0)
            current = visited[-1]

            if current in nodes and current != start:
                edges += [((start,current), visited)]
            else:
                next_moves = [c for c in moves(*current,slopes,avoid_uphill) if c in path and c not in visited]
                for coords in next_moves:
                    queue += [[] + visited + [coords]]

    return edges


def collapse_edges(edges):

    retained_edges = [];  updated_edges = [];  collapse = [];  consecutive = 1;  i = 1

    while i <= len(edges):
        if ((i < len(edges) and edges[i][0][0] == edges[i-1][0][0])
        or (i == len(edges) and edges[i-1][0][0] == edges[i-2][0][0])
        or consecutive > 1):
            consecutive = 1 if i == len(edges) or edges[i][0][0] != edges[i-1][0][0] else consecutive + 1
            retained_edges += [edges[i-1]]
        else:
            consecutive = 1
            if i > 0:  collapse += [edges[i-1]]
        i += 1

    for (a,b), trail in collapse:
        updated_edges = []
        for (c,d), path in retained_edges:
            if b == c:
                if a != d:
                    updated_edges += [((a,d),trail[:-1]+path)]
            elif b == d:
                if c != a:
                    updated_edges += [((c,a),path+trail[:-1][::-1])]
            else:
                updated_edges += [((c,d),path)]
        retained_edges = updated_edges

    return retained_edges


def link_nodes(edges):

    links = {}
    for (a,b), _ in sorted(edges):
        links[a] = links.get(a,[]) + [b]

    return links


def calculate_longest_bfs(path, slopes):

    start = min(path);  finish = max(path);  longest = 0

    queue = [(start, set(), 0)]

    while queue:

        current, visited, steps = queue.pop(0)

        if current == finish:
            longest = max(len(list(visited)),longest)
        else:
            steps += 1
            options = [c for c in moves(*current,slopes,True) if c in path and c not in visited]
            for coords in options:
                queue += [(coords, visited.union([coords]), steps)]

    return longest


def calculate_longest_dfs(path, slopes, avoid_uphill):

    edges, links = shrink_grid(path, slopes, avoid_uphill)
    distances = dict([(termini, len(visited)-1) for termini, visited in edges])

    start = min(path);  target = max(path);  longest = 0
    
    stack = [(start, set([start]), 0)]

    while stack:

        previous, visited, steps = stack.pop(-1)

        for node in [x for x in links[previous] if x not in visited]:
            
            if node == target:
                longest = max(steps + distances[(previous,node)], longest)
            else:
                stack += [(node, visited.union([node]), steps + distances[(previous,node)])]

    return longest

 
def main(filepath):

    path, slopes = parse_input(filepath)

    return calculate_longest_bfs(path,slopes), calculate_longest_dfs(path,slopes,False)


print(main('23.txt'))