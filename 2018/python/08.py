#  First recursive one of 2018. Couldn't figure out any way to do this without recursion (I tried!), and then misunderstood Part 2
#  on the first go around. Came back to it later, reread it and found it pretty straightforward... another typical AoC recursion
#  problem where my brain just needs to be in the right place for me to succeed!

def parse_nodes(input,nodes=dict(),node_id=[0]):

    children = input[0];  meta_idx = input[1];  input = input[2:]

    for child in range(1,children+1):
        id = [] + node_id + [child]
        input, nodes = parse_nodes(input,nodes,id)

    metadata = input[:meta_idx]
    metasum  = sum(metadata)
    value    = metasum if children == 0 else sum([v for _,v in [nodes.get(tuple(node_id+[i]),(0,0)) for i in metadata]])

    nodes[tuple(node_id)] = (metasum,value)
    input                 = input[meta_idx:]

    return (input,nodes) if len(input) > 0 else nodes


def main(filepath):

    input = [int(x) for x in open(filepath,'r').read().split(' ')]
    nodes = parse_nodes(input)

    return sum([m for m,_ in nodes.values()]), nodes[(0,)][1]


print(main('08.txt'))