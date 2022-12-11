#  What I wanted to write first time around! Dijkstra BFS using 2 level priority queue i) Total Energy and ii) Number of Moves 
#  This ensures we end up with the cheapest solution and the fewest moves possible for that cost. Key performance considerations...
#
#  i)  Simple, lightweight immutable game state (a 19 or 27 digit string of numbers) - no need for queueing weighty classes or any deep copying.
#      (The class + deepcopy combo killed the performance of my first attempt).
#  ii) Previously seen game states kept (with their associated energy cost) to enable abandonment of suboptimal solutions
#  ii) Each evaluation of valid moves considers only complete moves between origin and destination rather than individual steps on that journey
#      - basically a fast-forward approach that avoids evaluating irrelevant interim game states
#  iv) If one or more amphipods can be moved to their destination room, one of those is chosen to move and that is considered the only valid move
#      for that turn. This shortcuts a bunch of move evaluation, and avoids queueing multiple different states for future evaluation when we know 
#      those will ultimately end up producing the same state with the same cost later on. Thus, multiple moves are only added to the queue when no 
#      rooms are open and we need to evaluate all potential moves into the hallway.
#
#  Because of the variable energy cost of moves, the first solution we find, even with a priority queue, is not guaranteed to be the cheapest 
#  (there may be almost complete solutions later in the queue with a lower cost final move). Thus found solutions have to be added back to the 
#  queue, and only once the first complete solution pops off the queue can we be certain we have the correct answer.
#
#  Part of the rationale for converting the game state to a numeric representation (.ABCD => 01234) is that this allows use of string to int 
#  conversion to determine a clear path between points + calculation of amphipod energy costs trivially in a single one-liner (energy costs
#  are increasing powers of ten, so step cost = 10**(amphipod-1)). It also makes converting the string index of any location to an x,y vector simpler
#  and avoids the need for generating a seperate hashable state reference. The downside (which is VERY apparent below) is that the string manipulation
#  required on this to determine valid moves, is pretty impenetrable and definitely not intuitive!

from heapq import heapify, heappush, heappop
from time  import time

def dijkstra(amphipods):

    start_time    = time()
    initial_state = ('0'*11) + ''.join([str(ord(x)-64) for x in list(amphipods.upper())])
    target_state  = ('0'*11) + ''.join([str(ord(x)-64) for x in sorted(list(amphipods.upper()))])
    seen_states   = dict([(initial_state,(0,[]))])

    queue = [(0,0,initial_state)]; heapify(queue)

    while len(queue) > 0:
        total_energy, move_ct, state = heappop(queue)     
        if state == target_state:
            break
        else:
            moves = get_moves(state)
            trail = seen_states[state][1]
            for new_state, move, energy in moves:
                seen = seen_states.get(new_state,(99**99,[]))
                new_energy = total_energy + energy
                if new_energy < seen[0] or (new_energy == seen[0] and len(trail)+1 < len(seen[1])):
                    seen_states[new_state] = (new_energy, trail + [move])
                    heappush(queue,(new_energy, move_ct + 1, new_state))

    return render(start_time, initial_state, seen_states[target_state][1])


def get_moves(state):

    capacity = (len(state)-11)//4 ;  hall = state[:11] ;  rooms = [state[i:i+capacity] for i in range(11,len(state),capacity)]

    hall_dwellers = [(i,i,0,a) for i,a in enumerate(hall) if a != '0']

    room_dwellers = [((capacity*((x//2)-1))+y+10,x,y,a) for x,y,a in 
                      [((i+1)*2, rm.index(rm.lstrip('0')[0])+1, rm.lstrip('0')[0]) for i,rm in enumerate(rooms) if rm.replace(str((i+1)),'0') != '0'*capacity]]

    open_rooms = [((capacity*((x//2)-1))+y+10,x,y,a) for x,y,a in   
                   [((i+1)*2,len(rm)-rm[::-1].index('0'),str(i+1)) for i,rm in enumerate(rooms) if '0' in rm and rm.replace(str((i+1)),'0') == '0'*capacity]]

    for dest,xx,yy,valid_species in open_rooms:
        for category in [room_dwellers,hall_dwellers]:
            for origin,x,y,species in category:
                if species == valid_species:
                    energy = (abs(xx-x) + y + yy)*(10**(int(species)-1)) if int(state[min(x,xx)+1:max(x,xx)]+'0') == 0 else 0
                    if energy > 0:
                        new_state = ''.join(['0' if i == origin else species if i == dest else x for i,x in enumerate(state)])
                        return [(new_state,((x,y),(xx,yy)),energy)]

    valid_moves = []
    open_stops = [(i,i,0) for i,a in enumerate(hall) if a == '0' and i not in (2,4,6,8)]

    for dest,xx,yy in open_stops:
        for origin,x,y,species in room_dwellers:
            energy = (abs(xx-x) + y + yy)*(10**(int(species)-1)) if int(state[min(x,xx)+1:max(x,xx)]+'0') == 0 else 0
            if energy > 0:
                new_state = ''.join(['0' if i == origin else species if i == dest else x for i,x in enumerate(state)])
                valid_moves += [(new_state,((x,y),(xx,yy)),energy)]

    return valid_moves


def render(start_time,state,trail):

    duration = str(round(time()-start_time,2))

    reset, red, blue = ('\033[0m','\033[31m','\033[94m');  moves, energy, total_energy = (0,0,0);  line = ''

    capacity  = (len(state)-11)//4
    amphipods = dict([(((x*2)+2,y+1),chr(int(a)+64)) 
                         for x,rm in enumerate([state[i:i+capacity] for i in range(11,len(state),capacity)]) for y,a in enumerate(rm)])
    locations = [(x,0) for x in range(11)] + list(amphipods.keys())
    borders   = [(x+a,y+b) for a in (-1,0,1) for b in (-1,0,1) for x,y in locations if (x+a,y+b) not in locations]

    for frm,to in trail:

        amphipods[to] = amphipods.pop(frm);  moves += 1
        energy = (abs(to[0]-frm[0]) + frm[1] + to[1])*(10**(int(ord(amphipods[to])-65)));  total_energy += energy

        for y in range(-1,capacity+2):
            for x in range(-1,13):

                if x < 0: 
                    line = '' if y >= 0 else '\n'

                if   (x,y) in amphipods: line += red + amphipods[(x,y)] + reset
                elif (x,y) in locations: line += blue + '.' + reset 
                elif (x,y) in borders:   line += chr(0x2021)
                else:                    line += ' '
                          
            if y == 0: line += ('  Energy used: +' + str(energy) + ' = ' + str(total_energy))
            print(line)

    print(f'\nTotal moves: {moves}') 
    print(f'Search time: {duration} seconds\n')

    return total_energy

def main():

    pt1 = dijkstra('DDCABACB')             # ~1.8s
    pt2 = dijkstra('DDDDCCBABBAACACB')     # ~4.5s

    return pt1, pt2
    
print(main())