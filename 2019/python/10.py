from math import atan2, degrees, hypot

def get_angle(pt1, pt2):  

    angle = degrees(atan2(pt2[0]-pt1[0],pt2[1]-pt1[1]))
    return angle+90 if angle >= -90 else angle+450

def get_distance(pt1, pt2):  return hypot(pt2[1]-pt1[1],pt2[0]-pt1[0])

def main(f):

    asteroids = set()
    for y,row in enumerate([list(x) for x in open(f,'r').read().split('\n')]):
        for x,z in enumerate(row):
            if z == '#':
                asteroids.add((y,x))

    ct = 0
    for origin in asteroids:
        angles = set()
        for target in asteroids:
            if origin != target:
                angles.add(get_angle(origin,target))
        visible_asteroids = len(list(angles))
        if visible_asteroids > ct:
            ct = visible_asteroids
            station = origin
            radar = dict([(target,get_angle(origin,target)) for target in asteroids if target != origin])

    vapourised = 0;  orientation = -1
    while vapourised < 200:
        targets = [v for v in radar.values() if v > orientation]
        if len(targets) == 0:
            orientation = -1
        else:
            orientation = min(targets)
            target = [x[1] for x in sorted([(get_distance(station,asteroid),asteroid) for asteroid, angle in radar.items() if angle == orientation])][0]
            radar.pop(target)
            vapourised += 1

    return ct, (target[1]*100)+target[0]

print(main('10.txt'))
