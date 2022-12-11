from collections import namedtuple

def read_file(filepath):
    
    Reindeer = namedtuple('Reindeer','name speed duration rest')

    return [Reindeer(x[0],int(x[3]),int(x[6]),int(x[13])) for x in [x.split(' ') for x in [x for x in open(filepath,'r').read().split('\n')]]]


def first_past_the_post(reindeer,seconds):
    
    positions = []

    for r in reindeer:
        s = 0;  d = 0;  distance = r.speed * r.duration;  interval = r.duration + r.rest
        
        while s < seconds:
            if s + interval <= seconds:
                d += distance;  s += interval
                
            elif s + r.duration <= seconds:
                d += distance;  s = seconds
                
            else:
                for _ in range(r.duration):
                    d += r.speed;  s += 1
                    if s == seconds: break
        
        positions += [[d,r.name]]
        
    return tuple(sorted(positions)[-1][::-1])


def race(reindeer,seconds):
    
    points = {}    
    for s in range(1,seconds+1):        
        winner = first_past_the_post(reindeer,s)
        points[winner[0]] = points.get(winner[0],0) + 1
        
    return winner, tuple(sorted([(v,k) for k,v in points.items()])[-1][::-1])


def main(filepath,seconds=2503):

    return race(read_file(filepath),seconds)

print(main('14.txt'))
