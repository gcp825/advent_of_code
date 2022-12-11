#  Non-recursive DFS this time. Part 2 takes just under a second; a recursive DFS might halve that, but < 1 second is good enough - so no recursion for me!
#  Creating a new independent version of tracker with the set.union method, rather than using deepcopy saved ~4.5 seconds of runtime from the initial version.

from itertools import groupby

def parse_file(f):

    input  = [tuple(x.split('-')) for x in open(f,'r').read().split('\n')]+[tuple(x.split('-')[::-1]) for x in open(f,'r').read().split('\n')]
    groups = [(k,[v for _, v in list(g) if v != 'start']) for k,g in groupby(sorted(input), lambda x: x[0])]

    return dict([(k,v) for k,v in groups if k != 'end'])

def route_ct_dfs(start,paths,pt):

    route_ct = 0;  queue = [(cave,0,set()) for cave in start]

    while len(queue) > 0:

        move, revisits_used, tracker = queue.pop(-1)

        if move == 'end':
            route_ct += 1
        else:     
            revisits_used += 0 if revisits_used == (pt-1) or move.isupper() or move not in tracker else 1

            queue += [(cave, revisits_used, tracker.union([move]) if move.islower() else tracker.union([]) )                 
                      for cave in paths[move] if cave not in tracker or (cave in tracker and revisits_used < (pt - 1))]

    return route_ct

def main(filepath):

    paths = parse_file(filepath)
    start = paths.pop('start')

    return route_ct_dfs(start,paths,1), route_ct_dfs(start,paths,2)
    
print(main('12.txt'))