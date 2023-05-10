from heapq import heapify, heappush, heappop

def survey_cave(target,depth):

    cave = dict()
    southeast_bound = int(max(*target)*1.5)+1

    for y in range(southeast_bound):
       for x in range(southeast_bound):
           cave[(y,x)] = survey_region(y,x,target,depth,cave)

    return cave


def survey_region(y,x,target,depth,cave):

    geo_idx = 0 if (y,x) in [(0,0),target] else x*16807 if y == 0 else y*48271 if x == 0 else cave[(y-1,x)][1] * cave[(y,x-1)][1]

    erosion_level = (geo_idx + depth) % 20183

    region_type = erosion_level % 3

    return region_type, erosion_level, geo_idx


def dijkstra(cave,target):
    
    start = (0,(1,0,0))
    visited = dict([start[::-1]])
    queue = [start]; heapify(queue)

    while queue:
        journey_time, current_state = heappop(queue)
        if current_state[1:] == target: 
            return journey_time
        else:
            for minutes, state in get_moves(journey_time,*current_state,cave,target):
                if minutes < visited.get(state,minutes+1):
                    visited[state] = minutes
                    heappush(queue,(minutes,state))


def get_moves(minutes,tool,y,x,cave,target):

    moves = []

    for coords in [(y-1,x),(y,x+1),(y+1,x),(y,x-1)]:
        region_type = cave.get(coords,(-1,))[0]
        if region_type >= 0:
            if region_type != tool:
                if coords == target and tool == 2:
                    moves += [(minutes+8, (1, *coords))]                   
                else:
                    moves += [(minutes+1, (tool, *coords))]
            else:
                moves += [(minutes+8, (t, *coords)) for t in [(tool-1)%3, (tool+1)%3]]

    return moves

   
def main(target,depth):
    
    cave = survey_cave(target,depth)
    risk_level = sum([v[0] for k,v in cave.items() if k <= target and k[1] <= target[1]])
    journey_time = dijkstra(cave,target)

    return risk_level, journey_time
    
print(main((739,9),10914))
