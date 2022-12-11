#  Possibly my favourite solutions from any puzzle I've done so far. I worked out almost immediately that I didn't have to build the whole spiral - I just 
#  calculated the central column (the "spine") to the required depth, worked out the distance between the input and the nearest point on that outer ring
#  where you've got a straight shot to the centre and then added the number of outer rings to that. Looking at the reddit megathread afterwards I can't see
#  another solution quite like mine... those that haven't built the spiral seem to have used a pattern on the diagonal rather than the vertical.
 
#  For Part 2, given that I hadn't built the spiral and thus had nothing to adapt, I figured I'd be a smartarse and automate the process of just looking up 
#  the answer on OEIS. For me, that's actually more beneficial than writing a typical brute force 'build the spiral' solution - particularly as it gives me a 
#  chance to learn something: I've never used urllib before. Looking at the megathread afterwards, it seems I'm not the only one that cheated... but nobody else 
#  automated their cheating!

from urllib.request import urlopen

def part1(target):

    spine = [1,4,8,15,23];  distance = [0,1,1,2,2];  moves= 0

    if target <= spine[-1]:
        for i in range(len(spine)-1):
            if spine[i] <= target <= spine[i+1]:
                spine = spine[:i+2]
                distance = distance[:i+2]
                break

    while target > spine[-1]:
        spine = spine[-3:] + [(2*spine[-1]) - (2*spine[-3]) + spine[-4]]
        distance = distance[-3:] + [distance[-1]+1 if distance[-1]-distance[-2] == 0 else distance[-1]]

    if distance[-1] == distance[-2]:       
        s = spine[-1];  n = spine[-2];  w = s-((s-n)//2);  nw = n+((s-n)//4);  sw = s-((s-n)//4)
        if  sw <= target <= s:  moves = s-target+distance[-1]
        elif n <= target <= nw: moves = target-n+distance[-2]
        else:                   moves = abs(target-w)+distance[-1]
    else:
        n = spine[-1];  s = spine[-2];  e = s+((n-s)//2);  ne = n-((n-e)//2);  se = s+((n-e)//2)
        if  ne <= target <= n:  moves = n-target+distance[-1]
        elif s <= target <= se: moves = target-s+distance[-2]
        else:                   moves = abs(target-e)+distance[-1]

    return moves

def part2(target):

    data = urlopen('https://oeis.org/A141481/b141481.txt')
    answer = min(int(x[1]) for x in [line.decode('utf-8').strip('\n').split(' ') for line in data] if x[0].isnumeric() and x[1].isnumeric() and int(x[1]) > target)

    return answer

def main(target):

    return part1(target), part2(target)


print(main(312051))
