class Group:

    def __init__(self,*args):

        self.type, self.units, self.hit_pts, self.initiative, self.weapon, self.weapon_damage, self.immunities, self.weaknesses = args
        self.power = self.units * self.weapon_damage
        self.target = None

    def __str__(self):

        p1 = f"Initiative: {self.initiative}, Type: {self.type}, Units: {self.units}, Power: {self.power}, Hit Points: {self.hit_pts}, "
        p2 = f"Weapon: ({self.weapon}, {self.weapon_damage}), " + f"{'Immunities: ' + str(self.immunities) + ', ' if self.immunities else ''}"
        p3 = f"{'Weaknesses: ' + str(self.weaknesses) + ', ' if self.weaknesses else ''}" + f"Target: {self.target}"
        
        return p1 + p2 + p3


    def damage(self,a,b):

         return 0 if a.weapon in b.immunities else a.power * (2 if a.weapon in b.weaknesses else 1)       


    def determine_target(self, groups):

        targets = [v for v in [(-self.damage(self,t),-t.power,-t.initiative) for t in [g for g in groups if g.type != self.type]] if v[0] != 0]

        self.target = abs(sorted(targets)[0][2]) if targets else None


    def receive_damage(self, attacker):

        self.units = max(self.units - (self.damage(attacker,self) // self.hit_pts),0)
        self.power = self.units * self.weapon_damage


def parse_input(filepath,boost):

    combatants = list(zip(['reindeer', 'infection'],[x.split('\n')[1:] for x in open(filepath).read().split('\n\n')]))

    parsed, characteristics = [], []

    for type, groups in combatants:
        for group in groups:

            b = boost if type == 'reindeer' else 0
            x = list(sorted(group[group.find('(')+1:group.find(')')].split('; '))) if '(' in group else []

            characteristics = [type] + list(map(int,[x for i,x in enumerate(group.split(' ')) if i in (0,4)]))
            characteristics += [x if i == 4 else int(x)+b if i == 5 else int(x) for i,x in 
                                   [(i,x[::-1]) for i,x in enumerate(group[::-1].split(' ')) if i in (0,4,5)]]
            characteristics += [x.pop(0)[10:].split(', ') if x and x[0][:6] == 'immune' else []]
            characteristics += [x[0][8:].split(', ') if x else []]

            parsed += [Group(*characteristics)]

    return parsed


def combat(filepath,boost):

    groups, deadlock = parse_input(filepath,boost), False

    while not deadlock and len(list(set([g.type for g in groups]))) == 2:
        groups, deadlock = fight(groups)

    return 'neither' if deadlock else groups[0].type, sum([g.units for g in groups])


def fight(groups):

    initial_units = sum([g.units for g in groups])
    available_targets = [] + groups

    groups = [x[1] for x in sorted([((-g.power,-g.initiative),g) for g in groups])]

    for selecter in groups:
        selecter.determine_target(available_targets)
        available_targets = [t for t in available_targets if t.initiative != selecter.target]

    groups = [x[1] for x in sorted([(-g.initiative,g) for g in groups])]

    for attacker in groups:
        if attacker.units and attacker.target:
            i = [i for i,g in enumerate(groups) if g.initiative == attacker.target][0]
            groups[i].receive_damage(attacker)

    deadlock = False if sum([g.units for g in groups]) < initial_units else True

    return [g for g in groups if g.units], deadlock


def binary_search_values(victor,lo,hi,boost):

    if hi-lo == 1:
        lo, hi = (lo,lo) if victor == 'reindeer' else (hi,hi)
    else:
        lo, hi = (lo,boost) if victor == 'reindeer' else (boost,hi)

    return lo, hi, (lo+hi)//2


def main(filepath):
    
    results, lo, hi, boost = [], 0, 0, 0

    while True:

        victor, remaining_units = combat(filepath,boost)
        results += [remaining_units]

        if hi == 0:
            hi, boost = (boost, boost) if victor == 'reindeer' else (hi, max(boost+100,boost*2))

        if hi > 0:
            if lo == hi: break
            lo, hi, boost = binary_search_values(victor,lo,hi,boost)

    return results[0], results[-1]


print(main('24.txt'))