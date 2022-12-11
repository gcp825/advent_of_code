#  Mostly avoided using the terminology used by the puzzle, as I found using equivalent military terminology much more intuitive.
#
#  First attempt at this was a prime example of over-complicating things: I had an A* mega-queue search that worked
#  perfectly for the example but ground to a halt when the input was scaled up.
#
#  Rewrote this as a straightforward BFS, keeping only coordinates in the queue and though it's not millisecond speedy, it's 
#  good enough. I could definitely make part 2 quicker with a more intelligent search for the elf attack power value, but
#  once again, what I've got is good enough with the actual input...

from copy import deepcopy

class Platoon:

    def __init__(self,*args):

        self.id, self.army = args;  self.enemy = chr(140-ord(self.army));  self.soldiers = 200

    def __str__(self): return f"id: {self.id}, army: {self.army}, soldiers: {self.soldiers}"


def build_battlefield(filepath):

    input     = [((y,x),z) for y,row in enumerate(open(filepath,'r').read().split('\n')) for x,z in enumerate(row)]
    terrain   = [x for x in input if x[1] not in 'EG']
    platoons  = [(x[0],Platoon(i,x[1])) for i,x in enumerate([x for x in input if x[1] in 'EG'])]

    return dict(terrain+platoons)


def render_battlefield(battlefield,round):

    print('Round:',round,'\n---------')

    row, line, soldiers = (-1,'','')

    for coords,val in sorted(battlefield.items()):

        if coords[0] > row: 
            print(line + soldiers)
            row, line, soldiers = (coords[0],'','')

        line += val if type(val) is str else val.army
        soldiers += '' if type(val) is str else ' ' + str(val.soldiers)

    print(line + soldiers)
    print('\n')


def adjacent_coords(y,x,battlefield,visited=set()):

    return [(yy,xx) for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)] if battlefield[(yy,xx)] == '.' and (yy,xx) not in visited]


def adjacent_enemy(y,x,battlefield,enemy):

    platoons = [(yy,xx,battlefield[(yy,xx)]) for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)] 
                   if type(battlefield[(yy,xx)]) is not str and battlefield[(yy,xx)].army == enemy]

    return list(sorted([(p.soldiers,(y,x),p) for y,x,p in platoons]))[0][1:] if platoons else False


def determine_move(y,x,battlefield,enemy):

    valid_routes = [(1,ac,ac) for ac in adjacent_coords(y,x,battlefield) if adjacent_enemy(*ac,battlefield,enemy)]

    if not valid_routes:

        first_steps  = [ac for ac in adjacent_coords(y,x,battlefield) if not adjacent_enemy(*ac,battlefield,enemy)]

        for first_step in first_steps:

            visited, steps, route_found = (set([first_step]), 1, False)
            queue = adjacent_coords(*first_step,battlefield)

            while queue:
            
                new_queue = []; steps += 1

                for location in queue:

                    if location not in visited:
                        visited.add(location)

                        if adjacent_enemy(*location,battlefield,enemy):
                            valid_routes += [(steps,location,first_step)]
                            route_found = True
                        else:
                            new_queue += adjacent_coords(*location,battlefield,visited)

                queue = [] if route_found else list(set(new_queue))

    return list(sorted(valid_routes))[0][2] if valid_routes else False


def battle(battlefield,elf_attack_power,render):

    rounds, victory_on_last_turn = (0,False)

    while len(list(set([v.army for v in battlefield.values() if type(v) is not str]))) > 1:

        platoons = list(sorted([(k,v) for k,v in battlefield.items() if type(v) is not str]))
        rounds += 1

        for coords, platoon in platoons:

            if platoon.id in [v.id for v in battlefield.values() if type(v) is not str]:

                victory_on_last_turn = False

                if not adjacent_enemy(*coords,battlefield,platoon.enemy):

                    new_location = determine_move(*coords,battlefield,platoon.enemy)          
                            
                    if new_location:
                        battlefield[new_location] = battlefield[coords]; battlefield[coords] = '.' 
                        coords = new_location

                target_in_range = adjacent_enemy(*coords,battlefield,platoon.enemy)

                if target_in_range:

                    target_coords, target = target_in_range
                    target.soldiers -= 3 if platoon.army == 'G' else elf_attack_power
                    battlefield[target_coords], victory_on_last_turn = (target,False) if target.soldiers > 0 else ('.',True)

        if render: render_battlefield(battlefield,rounds)


    victors = [v for v in battlefield.values() if type(v) is not str]
    complete_rounds = rounds if victory_on_last_turn else rounds-1

    return victors[0].army, len(victors), sum([v.soldiers for v in victors]) * complete_rounds


def main(filepath,render=False,elf_attack_power=3):

    results      = []
    battlefield  = build_battlefield(filepath)
    elf_platoons = sum([1 for v in battlefield.values() if type(v) is not str and v.army == 'E'])

    while True:

        results += [battle(deepcopy(battlefield),elf_attack_power,render)]

        if results[-1][0] == 'E' and results[-1][1] == elf_platoons: break
        else:
            elf_attack_power += 1

    return results[0][2], results[-1][2]

print(main('15.txt',False))