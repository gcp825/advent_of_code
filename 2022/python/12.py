def setup_search(filepath,start,end):

    map = dict([((y,x),height) for y,row in enumerate(open(filepath).read().split('\n')) for x,height in enumerate(row)])

    S = [k for k,v in map.items() if v == 'S'][0]
    E = [k for k,v in map.items() if v == 'E'][0]

    queue   = [k for k,v in map.items() if v == start] + ([S] if start == 'a' else [E] if start == 'z' else [])
    targets = [k for k,v in map.items() if v == end]   + ([S] if end == 'a'   else [E] if end == 'z'   else [])

    map[S], map[E] = ('a','z')

    compare = '<' if (start == 'S' or end == 'E') else '>' if (start == 'E' or end == 'S') else '<' if start <= end else '>'

    return map, queue, targets, compare


def adjacent_coords(coords):

    return [tuple(map(sum,zip(coords,{'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}[d]))) for d in 'NESW']


def valid_moves(map,location,visited,compare):

    return [c for c in adjacent_coords(location) 
               if c in map and c not in visited and ((compare == '<' and (ord(map[c]) - ord(map[location])) <= 1)
                                                 or  (compare == '>' and (ord(map[location]) - ord(map[c])) <= 1))]

            
def route_search(filepath,start,end):

    map, queue, targets, compare = setup_search(filepath,start,end)

    visited = set(queue)
    steps = 0

    if len(list(set(queue+targets))) == len(queue+targets): 

        while queue:

            steps += 1; new_queue = []

            for location in queue:

                moves = valid_moves(map,location,visited,compare)

                targets_found = [c for c in moves if c in targets]

                if targets_found or steps == len(map): return steps

                visited.update(moves)
                new_queue += moves

            queue = [] + new_queue

    return steps


def main(filepath):

    return route_search(filepath,'S','E'), route_search(filepath,'E','a')

    
print(main('12.txt'))