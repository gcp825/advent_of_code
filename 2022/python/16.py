#  Really happy with the interpretation of the puzzle and the implementation of Part 1.
#  Part 2 is clunky and slow though - whilst the approach I'm using was the quickest way to get Star 2, it's pretty rubbish as a
#  permanent solution (unless I can come up with a heuristic to prune bad journeys that don't hit the high value valves early).
#  Likely need to refactor the Part 1 solution to cater for two related journeys running in parallel.

def parse_input(f):

    file = lambda f: open(f).read().replace(';',',').split('\n')
    keep = lambda x: x if x.isnumeric() or x.isupper() else ',' if x in (';','=',',') else ''

    return list(sorted([(v[0],int(v[1]),v[2:]) for v in [w.split(',') for w in [''.join([keep(x) for x in y]) for y in [list(z[6:]) for z in file(f)]]]]))


def build_routes(data,startpoint):

    start_moves   = filter_out_useless_valves(data,startpoint)
    useful_routes = filter_out_useless_valves(data)

    return dict(start_moves + useful_routes)


def filter_out_useless_valves(data,startpoint=None):

    steps  = dict([(a,b) for a,_,b in data])
    nodes  = [a for a,b,_ in data if b > 0]
    routes = []

    terminals = [(start,end) for i,start in enumerate(nodes) for end in nodes[i+1:]] if startpoint is None else [(startpoint,end) for end in nodes]

    for start,end in terminals:

        queue = [[start]]

        while queue:

            trail = queue.pop(0)
            moves = [x for x in steps[trail[-1]] if x not in trail]

            if end in moves: break
            else:
                queue += [trail+[move] for move in moves]

        routes += [((start,end),len(trail)+1)]

    return routes + ([(k[::-1],v) for k,v in routes] if startpoint is None else [])


def build_journeys(routes,startpoint,time_limit):

    journeys = []
    valves   = set([x[0] for x in routes.keys() if x[0] != startpoint])
    queue    = [(list(moves),time) for moves, time in routes.items() if moves[0] == startpoint]

    while queue:

        trail, total_time = queue.pop(0)

        moves = [(trail+[m],total_time+t) for m,t in [(x,routes[(trail[-1],x)]) for x in valves if x not in trail] if total_time+t <= time_limit]

        if moves:         
            queue += moves
        else:
            journeys += [trail]

    return journeys


def score(journeys,routes,valve_pressure,time_limit):

    max_pressure = 0

    for journey in journeys:

        pressure = 0
        minutes  = time_limit

        for i in range(len(journey)-1):

            minutes -= routes[tuple(journey[i:i+2])]
            pressure += (valve_pressure[journey[i+1]] * minutes)

        max_pressure = max(pressure,max_pressure)

    return max_pressure


def pair_and_score_journeys(journeys,routes,valve_pressure,time_limit):

    valves = len(valve_pressure)

    pair_lengths = [(a+b+1,a+1,b+1) for i in range(valves//2,valves+1) for a in range(i) for b in range(i) if a+b == i and a >= b and a-b <= 3][::-1]

    best_score = 0
    consecutive_drops = 0

    while pair_lengths:

        this_score = 0

        target_valves,a,b = pair_lengths.pop(0)

        x,y = [j for j in journeys if len(j) == a], [j for j in journeys if len(j) == b]

        paired_journeys = [(j1,j2) for j1 in x for j2 in y if len(list(set(j1+j2))) == target_valves]

        for x,y in paired_journeys:

            pressure = score([x],routes,valve_pressure,time_limit) + score([y],routes,valve_pressure,time_limit)
            this_score = max(pressure,this_score)

        if best_score > 0:
            if this_score >= best_score:
                consecutive_drops = 0
            else:
                consecutive_drops += 1

        if consecutive_drops == 2: break

        best_score = max(this_score,best_score)

    return best_score


def main(filepath,startpoint='AA'):

    data           = parse_input(filepath)
    valve_pressure = dict([(a,b) for a,b,_ in data if b > 0])
    routes         = build_routes(data,startpoint)
    journeys       = build_journeys(routes,startpoint,30)   
    max_pressure   = score(journeys,routes,valve_pressure,30)

    journeys       = build_journeys(routes,startpoint,26)
    max_pressure2  = pair_and_score_journeys(journeys,routes,valve_pressure,26)

    return max_pressure, max_pressure2

    
print(main('16.txt'))