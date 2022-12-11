#  I was certain Part 1 could be solved by maths alone and I got some of the way there, recognising how the arc decreases in the forward
#  direction, and that the distance from origin to target could be measured in triangular numbers. Noticed the same was also true for the max 
#  vertical_velocity and the highest y position on the example... but couldn't quite put it all together, so just used the maths to limit my
#  brute force probes to optimal forward velocities only, calculating the apogee based upon the max vertical velocity that resulted in a hit.
#
#  This gave me the correct answer for Part 1, and it was only then, already having the answer, that I noticed the relationship between the max 
#  vertical velocity resulting in a hit and the minimum y coordinate (as I'd printed out all hit velocities to the terminal). This allowed me to
#  calculate Part 1 with maths only... though by luck more than judgement seeing as I still haven't quite figured out why!
#
#  And Part 2... well that's just the sort of unoptimised brute force I'm used to writing for Part 1.

def hit(xx,yy,target):

    x,y = (0,0);  hit = False

    while y >= target[2]:

        x,y   = (x+xx,y+yy)
        xx,yy = (0 if xx == 0 else xx-(xx//abs(xx)),yy-1)

        if target[0] <= x <= target[1] and target[2] <= y <= target[3]:
            hit = True
            break

    return hit


def probe(target):

    return [(x,y) for x,y in [(x,y) for x in range(target[1]+1) for y in range(target[2],abs(target[2]))] if hit(x,y,target)]


def main(filepath):

    target = tuple([int(x) for x in open(filepath,'r').read()[15:].replace('..',',').replace(' y=','').split(',')])

    return (abs(target[2])-1)*(abs(target[2]))//2, len(probe(target))

print(main('17.txt'))