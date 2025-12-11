from functools import cache, reduce
from operator import mul

def parse_input(filepath):

    return tuple((x[0],tuple(x[1:])) for x in [line.split() for line in open(filepath).read().replace(':','').split('\n')])

@cache
def count_paths(graph,node,target):

    return 1 if node == target else sum(count_paths(graph,n,target) for n in dict(graph).get(node,[]))


def main(filepath):

    graph = parse_input(filepath)
    nodes = (('you','out'), ('svr','dac','fft','out'), ('svr','fft','dac','out'))

    you_to_out = count_paths(graph,*nodes[0])
    svr_to_out = sum(reduce(mul,(count_paths(graph,a,b) for a,b in zip(n[:-1],n[1:]))) for n in nodes[1:])

    return you_to_out, svr_to_out


print(main('11.txt'))
