#  Enjoyed this one, but that's probably my soft spot for RPGs. Weird that the 3 attributes of the boss were supplied as input but
#  15 purchasable items weren't... hence I got lazy and just hardcoded them.

from itertools import combinations, product

class Player:

    def __init__(self,*args):        
        self.species, self.health, self.damage, self.armour = args

    def __str__(self):
        return f"species: {self.species}, health: {self.health}, damage: {self.damage}, armour: {self.armour}"

    def repel(self,hit):        
        self.health -= max((hit-self.armour),1)

def purchase_options(w_limits,a_limits,r_limits):
    
    weapons = {'dagger':(8,4),'shortsword':(10,5),'warhammer':(25,6),'longsword':(40,7),'greataxe':(74,8)}
    armour  = {'leather':(13,1),'chain':(31,2),'splint':(53,3),'banded':(75,4),'plate':(102,5)}
    rings   = {'damage1':(25,1),'damage2':(50,2),'damage3':(100,3),'defence1':(20,1),'defence2':(40,2),'defence3':(80,3)}
    
    inventories = product(combos(weapons,w_limits),combos(armour,a_limits),combos(rings,r_limits))
    quantified_inventories = []
    for inv in inventories:
        cost = 0;  damage_up = 0;  armour_up = 0
        for i in inv[0]:
            attr = weapons[i];  cost += attr[0];  damage_up += attr[1]
        for i in inv[1]:
            attr = armour[i];  cost += attr[0];  armour_up += attr[1]
        for i in inv[2]:
            attr = rings[i];
            cost += attr[0];
            if i.startswith('damage'): damage_up += attr[1]
            if i.startswith('defence'): armour_up += attr[1]
            
        quantified_inventories += [(cost,damage_up,armour_up,inv)]
    
    return sorted(quantified_inventories)
                              
def combos(item,limits):
                   
    c = []
    for i in range(limits[0],limits[1]+1):
        c += [x for x in combinations(item.keys(),i)]
    return c

def combat(player,opponent):
    
    while player.health > 0 and opponent.health > 0:
        opponent.repel(player.damage)
        if opponent.health > 0: player.repel(opponent.damage)
        
    return 1 if player.health > 0 else 2

def fight(opponent,mode):

    inventories = purchase_options((1,1),(0,1),(0,2))
    if mode == 2: inventories = inventories[::-1]

    for inv in inventories:
        cost, damage, armour, purchases = inv
        victor = combat(Player('you',100,damage,armour), Player(*opponent))
        if mode == victor: break

    return (cost,purchases)

def main(opponent):
    
    pt1 = fight(opponent,1)
    pt2 = fight(opponent,2)
    
    return pt1, pt2
        
print(main(('boss',104,8,1)))
