#  Runs for ~13 mins to produce the answer for both parts.
#  The optimisation / pruning is relatively simple and minimal - mainly because my answers were too low the more cavalier I was with
#  pruning the queue, so I had to scale that back and increase the run time to get the correct answer.
#  Likely need to come up with an intelligent method of pruning based on removing states that can no longer return a better geode score 
#  than the current best state.

def parse_input(f):

    retain = lambda x: tuple(''.join([y if y.isnumeric() or y in ('.',',') else '' for y in x]).split('.'))
    intify = lambda x: tuple([list(map(int,y.split(','))) if ',' in y else [int(y)] for y in x])
    format = lambda x: [[a[0],b+[0,0],c+[0,0],d+[0],e[:1]+[0]+e[1:]] for a,b,c,d,e in [x]][0]

    return [format(x) for x in [intify(y) for y in [retain(z) for z in open(f).read().replace(':','.').replace('and',',').replace('an.','an').split('\n')]]]


def choose_actions(robots,substances,costs):

    makeable = lambda x: min([substances[i] // costs[x][i] for i in range(3) if costs[x][i] > 0])

    queue_updates = []

    if makeable(3):
        
        updated_robots      =  [r+1 if i == 3 else r for i,r in enumerate(robots)]
        updated_substances  =  [substances[i] - costs[3][i] for i in range(3)]+[substances[3]]
        queue_updates       += [(updated_robots,updated_substances)]

    else:

        for idx, affordable in enumerate([makeable(i) for i in range(4)]):

            if affordable:
                updated_robots      =  [r+1 if idx == i else r for i,r in enumerate(robots)]
                updated_substances  =  [substances[i] - costs[idx][i] for i in range(3)]+[substances[3]]    
                queue_updates       += [(updated_robots,updated_substances)]

        queue_updates += [(robots,substances)]

    return queue_updates


def determine_quality(blueprint,minutes):

    costs      = blueprint[1:]
    robots     = [1,0,0,0]
    substances = [0,0,0,0]

    queue = [(robots,substances)]

    for _ in range(minutes):

        new_queue = []

        while queue:

            robots, substances = queue.pop(0)

            new_queue_inc_actions = choose_actions(robots,substances,costs)

            new_queue_inc_collections = [(r,[s[0]+w, s[1]+x, s[2]+y, s[3]+z]) for r,s in new_queue_inc_actions for w,x,y,z in [tuple(robots)]]

            new_queue += new_queue_inc_collections

        new_queue = [(list(x),list(y)) for x,y in list(set([(tuple(x),tuple(y)) for x,y in new_queue]))]

        max_obsidian_robots  = max([x[0][2] for x in new_queue])
        max_geode_robots     = max([x[0][3] for x in new_queue])

        if len(new_queue) > 200000:
            queue = [x for x in new_queue if (max_geode_robots == 0 and x[0][2] == max_obsidian_robots)
                                          or (max_geode_robots > 0 and (x[0][3] == max_geode_robots or x[0][2] == max_obsidian_robots))]
        else:
            queue = new_queue

    return max([substances[3] for _, substances in queue])


def main(filepath,limit=None,minutes=24):

    blueprints = parse_input(filepath)
    limit      = len(blueprints) if limit is None else limit
    geodes     = [determine_quality(b,minutes) for b in blueprints[:limit]]

    return sum([(i+1)*q for i,q in enumerate(geodes)]) if limit == len(blueprints) else geodes[0]*geodes[1]*geodes[2]


print((main('19.txt'),main('19.txt',3,32)))