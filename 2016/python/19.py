#  Part 1 just some basic maths. Part 2 was a nice excuse to finally use a deque... I've been waiting for an AoC opportunity since the 2020 crab cups
#  puzzle where some of the reddit solutions introduced me to the concept (I used a dict as a linked list for that one). Generally I'd try and avoid 
#  anything that actively encourages mutation... but the deque is created for exactly this kind of thing, and the mutation is part of the reason for the
#  associated speed benefit. Anyway it worked well but interestingly, I was able to visualise the puzzle much better in terms of some sort of 
#  round-robin sniper crossfire scenario than I was elves taking presents... not sure what that says about me?!

from collections import deque, namedtuple

def part1(total_elves):

    Elves = namedtuple('Elves','first last remaining interval')
    elves = Elves(1 if total_elves%2 == 0 else 3, total_elves-(1-(total_elves%2)), total_elves//2, 2)

    while elves.remaining > 2:
        elves = Elves(elves.first + (elves.interval*2) if elves.remaining%2 != 0 else elves.first,
                      elves.last  - (elves.interval*2) if elves.remaining%2 == 0 else elves.last,
                      elves.remaining//2,
                      elves.interval*2)

    return elves.first

def part2(participants):

    snipers = deque(range(1,(participants//2)+1))
    targets = deque(range((participants//2)+1,participants+1))

    while targets:

        targets.popleft()                              #  kill the current target  
        if targets:                                    #  if targets remain...
            targets.append(snipers.popleft())          #    rotate kill zone by 1 so current sniper is now the target furthest away         
            if len(snipers)+1 < len(targets):          #    snipers & targets should always be aligned (same number of each, else 1 more target if odd total)...
                snipers.append(targets.popleft())      #    ... so counterbalance by adding the nearest target to the sniper group if necessary                 

    return snipers[0]                                  #  only survivor

def main(elves):

    return part1(elves), part2(elves)

print(main(3004953))
