# This is slow (2 minutes total). I suspect I'm probably missing a trick by maintaining a trail of the last 3/10 moves
# and using these as part of the key in my visited dictionary... with the result that the queue is being bloated with
# unnecessary routes to investigate. But it's also worth noting that in amending the code to cope with both parts,
# Part 1 is now twice as slow as it was without the changes to enable Part 2!

from heapq import heapify, heappush, heappop

def regular_rules(cy,cx,trail,my,mx):

    moves = [(cy-1,cx,0,1), (cy,cx+1,1,1), (cy+1,cx,2,1), (cy,cx-1,3,1)]

    return [((y,x),d,s) for y,x,d,s in moves if 0 <= y <= my and 0 <= x <= mx
                                             and (len(trail) < 3 or len(list(set(trail+[d]))) > 1)
                                             and (len(trail) == 0 or d != (trail[-1]+2)%4)]


def ultra_rules(cy,cx,trail,my,mx):

    initial_moves  = [(cy-4,cx,0,4), (cy,cx+4,1,4), (cy+4,cx,2,4), (cy,cx-4,3,4)]
    standard_moves = [(cy-1,cx,0,1), (cy,cx+1,1,1), (cy+1,cx,2,1), (cy,cx-1,3,1)]

    if len(trail) == 0:
        return [((y,x),d,s) for y,x,d,s in initial_moves if 0 <= y <= my and 0 <= x <= mx]
    
    elif len(trail) == 10 and len(list(set(trail))) == 1:
        return [((y,x),d,s) for y,x,d,s in initial_moves if 0 <= y <= my and 0 <= x <= mx
                                                         and d != trail[-1] and d != (trail[-1]+2)%4]
    else:
        return ([((y,x),d,s) for y,x,d,s in standard_moves if 0 <= y <= my and 0 <= x <= mx and d == trail[-1]] +
                [((y,x),d,s) for y,x,d,s in initial_moves  if 0 <= y <= my and 0 <= x <= mx 
                                                           and d != trail[-1] and d != (trail[-1]+2)%4])


def heat_loss(city,cy,cx,direction,steps):

    ay = cy if direction in (1,3) else cy-steps+1 if direction == 2 else cy+steps-1
    ax = cx if direction in (0,2) else cx-steps+1 if direction == 1 else cx+steps-1

    return sum([city[(y,x)] for y in range(min(ay,cy),max(ay,cy)+1) for x in range(min(ax,cx),max(ax,cx)+1)])
               

def dijkstra(city,get_moves,ultra=False):

    start, target = (0,0), max(city.keys())
    visited = {};  queue = [(0,*start,[])];  heapify(queue)

    while queue:

        loss, y, x, trail = heappop(queue)

        if (y,x) == target: break
        else:
            for coords, direction, steps in get_moves(y,x,trail,*target):

                if not visited and steps == 4: ultra = True

                new_loss  = loss + heat_loss(city,*coords,direction,steps)
                new_trail = [] + trail[steps-10 if ultra else -2:] + [direction]*steps

                if new_loss < visited.get((coords,*new_trail),99**99):
                    visited[(coords,*new_trail)] = new_loss
                    heappush(queue, (new_loss, *coords, new_trail))

    return loss

   
def main(f):
    
    city = dict([((y,x),int(col)) for y,row in enumerate(open(f).read().split('\n')) for x,col in enumerate(row)])

    return dijkstra(city,regular_rules), dijkstra(city,ultra_rules)

    
print(main('17.txt'))