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


def shrink_grid(path,slopes):

    nodes = determine_nodes(path,slopes,False)
    edges = determine_edges(nodes,path,slopes,False)
    crossings = determine_edge_overlaps(edges)
    links = link_nodes(edges)

    return edges, crossings, links


def determine_nodes(path,slopes,avoid_uphill):

    nodes = [coords for coords in path if len([c for c in moves(*coords,slopes,avoid_uphill) if c in path or c in slopes]) > 2]

    return [min(path), max(path)] + nodes


def determine_edges(nodes,path,slopes,avoid_uphill):

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


def determine_edge_overlaps(edges):

    overlaps = {}
    for i,(termini, path) in enumerate(edges):
        for t,p in edges[i+1:]:
            matches = set(path[1:-1]).intersection(p[1:-1])
            if matches:
                overlaps[termini] = overlaps.get(termini,[]) + [t]
                overlaps[t] = overlaps.get(t,[]) + [termini]

    return overlaps


def link_nodes(edges):

    links = {}
    for (a,b), _ in sorted(edges):
        links[a] = links.get(a,[]) + [b]

    return links


def calculate_longest_bfs(path, slopes):

    start = min(path);  finish = max(path);  longest = 0

    queue = [(0, start, set())]

    while queue:

        steps, current, visited = queue.pop(0)

        if current == finish:
            longest = max(len(list(visited)),longest)
        else:
            steps += 1
            options = [c for c in moves(*current,slopes,True) if c in path and c not in visited]
            for coords in options:
                queue += [(steps, coords, visited.union([coords]))]

    return longest


def calculate_longest_dfs(path,slopes):

    edges, crossings, links = shrink_grid(path,slopes)
    steps = dict([(termini,len(visited)-1) for termini, visited in edges])

    start = min(path);  target = max(path);  longest = 0
    
    stack = [(start, set([start]), set())]

    while stack:

        previous, visited, traversed = stack.pop(-1)

        for node in [x for x in links[previous] if x not in visited]:
            
            if node == target:
                traversed.add((previous,node))
                longest = max(sum([steps[edge] for edge in traversed]), longest)
            else:
                if node not in visited:
                    overlaps = [edge for edge in crossings[(previous,node)] if edge in traversed]
                    if not overlaps:
                        stack += [(node, visited.union([node]), traversed.union([(previous,node)]))]

    return longest

 
def main(filepath):

    path, slopes = parse_input(filepath)

    return calculate_longest_bfs(path,slopes), calculate_longest_dfs(path,slopes)


print(main('23.txt'))