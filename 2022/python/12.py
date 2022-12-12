def build_map(filepath):

    return dict([((y,x),terrain) for y,row in enumerate(open(filepath).read().split('\n')) for x,terrain in enumerate(row)])


def adjacent_coords(coords):

    return [tuple(map(sum,zip(coords,{'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}[d]))) for d in 'NESW']

            
def route_search(map,start_coords=False,break_on=9**9):

    queue  = [k for k,v in map.items() if v == 'S']
    target = [k for k,v in map.items() if v == 'E'][0]

    map[queue[0]] = 'a';  map[target] = 'z'

    visited = set();  steps = 0

    if start_coords: queue = [start_coords]

    while queue:

        steps += 1; new_queue = set()

        for location in queue:

            visited.add(location)

            moves = [c for c in adjacent_coords(location) if c in map and c not in visited and (ord(map.get(c,'~')) - ord(map[location])) <= 1]

            if target in moves or steps == break_on: return steps

            new_queue.update(moves)

        queue = list(new_queue)

    return break_on


def main(filepath):

    map = build_map(filepath)
    pt1 = route_search({**map})
    pt2 = pt1

    for start_coords in [k for k,v in map.items() if v == 'a']:

        steps = route_search({**map},start_coords,pt2)
        pt2 = min(steps,pt2)

    return pt1, pt2
    
print(main('12.txt'))