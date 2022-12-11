#  Dijkstra using cumulative risk to prioritise routes. Actually pretty trivial to implement in the end thanks to heapq: it's my basic BFS 
#  with the queue heapified. The expansion of the grid in part 2 was actually the most problematic part (shouldn't have been - just me being 
#  an idiot). Added a manhattan heuristic to turn this into A*, but this actually slowed the search down slightly, so removed it!

from heapq import heapify, heappush, heappop

def build_grid(filepath,gridsize=1):

    riskmap = [((x,y),z) for y,row in enumerate([list(map(int,list(x))) for x in open(filepath,'r').read().split('\n')]) for x,z in enumerate(row)]
    width, height = tuple(map(sum,zip(max([x for x,_ in riskmap]),(1,1))))

    riskmap += [((c[0]+(width*i),c[1]), v+i if v+i <=9 else v+i-9)  for c,v in riskmap for i in range(1,gridsize)]
    riskmap += [((c[0],c[1]+(height*i)), v+i if v+i <=9 else v+i-9) for c,v in riskmap for i in range(1,gridsize)]

    return dict(riskmap)

def dijkstra(riskmap,start,end):
    
    max_risk = sum(riskmap.values());  ranked_nodes = dict([(k,max_risk) for k in riskmap.keys()])

    compass = {'n':(0,-1),'s':(0,1),'e':(1,0),'w':(-1,0)}
    adjacent_coords = lambda x,y: [tuple(map(sum,zip((x,y),compass[d]))) for d in ['e','s','n','w']]

    queue = [(0,0,0)];  heapify(queue)

    while len(queue) > 0:

        cumulative_risk, a, b = heappop(queue)

        if cumulative_risk >= ranked_nodes[end]: break

        else:

            if cumulative_risk <= ranked_nodes.get((a,b),max_risk):
        
                for new_risk,x,y in [(v+cumulative_risk,x,y) for v,x,y in [(riskmap.get((x,y),0),x,y) for x,y in adjacent_coords(a,b)] if v > 0]:

                    if new_risk < ranked_nodes[(x,y)]:
                        ranked_nodes[(x,y)] = new_risk
    
                        if (x,y) != end:
                            heappush(queue,(new_risk,x,y))

    return ranked_nodes[end]

def main(f):

    riskmap = build_grid(f,1)
    pt1 = dijkstra(riskmap,(0,0),max(riskmap.keys()))

    riskmap = build_grid(f,5)
    pt2 = dijkstra(riskmap,(0,0),max(riskmap.keys()))

    return pt1, pt2
    
print(main('15.txt'))