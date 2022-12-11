#  Tuned this to a point where the speed is roughly comparable to the typical python recursive DFS solution on the reddit solutions megathread.
#  Runs a little slower than most, though it's not that noticeable (~ 33% slower) and faster than some. Thats not bad for a non-recursive BFS
#  that is far more understandable. I'll take this over any of those solutions (except the impressive but utterly unreadble set based recursive
#  generator solution that runs 4 times quicker than mine!)

from itertools import chain, groupby

def build_bridges(comp_by_port):

    length = 1;  strongest, strongest_longest = (0,0)
    queue = [[x] for x in comp_by_port[0]]

    while len(queue) > 0:

        current = queue.pop(0);  p = current[-1][1]
        next_up = [c for c in comp_by_port[p] if c not in current and c[::-1] not in current]
        if (p,p) in next_up:                                                                                    #  perf. tune #1 - components with identical ports
            next_up = [(p,p)]                                                                                   #  taken first to avoid duplicate bridges with these
                                                                                                                #  components in different places
        if len(next_up) == 0:
            strongest = max(strongest, sum(chain(*current)))
            if len(current) > length:
                length = len(current);  strongest_longest = 0
            strongest_longest = max(strongest_longest, sum(chain(*current)))
        else:
            for component in next_up:
                queue += [current+[component]]

    return strongest, strongest_longest

def main(filepath):

    components   = [tuple(map(int,x)) for x in [x.split('/') for x in open(filepath,'r').read().split('\n')]]
    orientations = set(components+[(y,x) for x,y in components])
    comp_by_port = dict([(k,list(v)) for k,v in groupby(sorted(orientations), lambda x: x[0])])                #  perf. tune #2 - this dict of components by port
#   port_to_port = dict([(k,list(chain(*v))[1::2]) for k,v in groupby(sorted(orientations), lambda x: x[0])])  #  <-- redundant but kept as a nice groupby example

    return build_bridges(comp_by_port)

print(main('24.txt'))
