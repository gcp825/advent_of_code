#  Brute force, but non-typical brute force! No need to record every visited location step by step... just bulk update a set of visited locations
#  with every possibility covered by each instruction. That makes the whole thing very quick... so much so that the easiest approach to Part 2 given
#  that I'm not visiting every location, is to just run the whole process again, passing in the intersections from Part 1 and calculating steps
#  to each of those only when they first appear in the list of bulk locations for each wire. Originally had this as two separate processes
#  with a lot of repetition, but since refactored to a single trace_wires function.

def get_visited_locations(coords,move,distance):

    adjust = 1 if move in ('DR') else -1   
    x,y = (coords[0] + (distance*adjust), coords[1]) if move in ('LR') else (coords[0], coords[1] + (distance*adjust))
    lo, hi = (min(coords[0],x), max(coords[0],x)+1)  if move in ('LR') else (min(coords[1],y), max(coords[1],y)+1)

    return (x,y), [(n,y) for n in range(lo,hi)] if move in ('LR') else [(x,n) for n in range(lo,hi)]

def count_steps(wire,move,coords,steps,visited,store):

    idx = {'L':0,'R':0,'U':1,'D':1}
    for loc in visited:
        current_steps, last_update = store.get(loc,(0,-1))
        if wire > last_update:
            i = idx[move]
            store[loc] = (current_steps + steps + (max(coords[i],loc[i]) - min(coords[i],loc[i])), wire)
    return store

def trace_wires(wires,intersects=set()):

    store = {};  mode = len(intersects)
    
    for wire, moves in enumerate(wires):
        coords = (0,0);  visited = set();  steps = 0
        for move, distance in moves:
            next_coords, locations = get_visited_locations(coords,move,distance)
            if mode == 0:
                visited.update(locations)
            else:
                visited = intersects.intersection(locations)   
                store = count_steps(wire,move,coords,steps,visited,store)
                steps += distance
            coords = next_coords
        visited.discard((0,0))
        if mode == 0: store[wire] = visited

    return store

def main(f):

    wires = []
    for moves in [x.split(',') for x in open(f,'r').read().split('\n')]:
        wires += [[(x[0],int(x[1:])) for x in moves]]

    paths = trace_wires(wires)
    intersects = paths[0].intersection(paths[1])
    steps = trace_wires(wires,intersects)

    return min(abs(x)+abs(y) for x,y in intersects), min(v for v in steps.values())[0]

print(main('03.txt'))
