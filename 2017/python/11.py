def main(filepath):
    
    moves = open(filepath,'r').read().strip('\n').split(',')        
    compass = {'n':(0,-2),'s':(0,2),'nw':(-1,-1),'ne':(1,-1),'sw':(-1,1),'se':(1,1)}
    location = (0,0);  distance = 0;  furthest = 0

    for m in moves:
        location = tuple(map(sum,zip(location,compass[m])))
        distance = abs(location[0]) + ((abs(location[1])-abs(location[0]))//2)
        furthest = max(distance,furthest)

    return distance, furthest
    
print(main('11.txt'))
