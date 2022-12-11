#  Breadth First Search to a limited depth, pre-calculating every possible permutation and discarding anything that can't possibly be the correct
#  answer, before actually testing the remaining possibilities

#  This took some time to write! No idea whether it would actually be quicker to build up the sequences incrementally rather than using itertools.product
#  though product IS much quicker than building the sequences with the combinations then permutations approach used on Day 15 (primarily because
#  very little pruning can be done at the combination level).

#  Overall it's not hideously slow for a spell sequence of 8, although is noticeably slower for 9... all the time being spent evaluating 1.9m sequences
#  1 character at a time... and discarding virtually all of those leaving only 63 fights to actually try for my input!

#  Adding the Spell subclass has helped tidy up some of the hideous variable naming, though the fiddly nature of this puzzle means it's still a bit ugly in places

from itertools import product
from copy import deepcopy

class Fight:
    
    class Wizard:
        def __init__(self,health,mana):
            self.health = health;  self.mana = mana;  self.spend = 0
            
        def __str__(self):
            return f"Wizard: (health: {self.health}, mana: {self.mana}, spend: {self.spend})"
                    
    class Boss:        
        def __init__(self,health,damage):
            self.health = health;  self.damage = damage
            
        def __str__(self):
            return f"Boss:   (health: {self.health}, damage: {self.damage})"
        
    class Spell:
        def __init__(self,cost,value,life):
            self.cost = cost;  self.value = value;  self.life = life;  self.timer = 0
            
        def __str__(self):
            return f"(cost: {self.cost}, value: {self.value}, life: {self.life}, timer: {self.timer})"        
    
    def __init__(self,mode,life,mana,health,damage):
        
        self.mode = mode
        self.wizard = self.Wizard(life,mana)
        self.boss   = self.Boss(health,damage)
        self.d = self.Spell(73,2,1);  self.m = self.Spell(53,4,1);  self.p = self.Spell(173,3,6);  self.r = self.Spell(229,101,5);  self.s = self.Spell(113,7,3)

    def __str__(self):
        
        print(self.wizard)
        print(self.boss)
        p1 = f"Spells: (drain: {self.d}, magic missile: {self.m}, poison: {self.p}, recharge: {self.r}, shield: {self.s}"
        p2 = f"Mode:   {self.mode}"
        return p1 + '\n' + p2
    
    def boss_attack(self):
        
        self.timers()
        if self.boss.health > 0:
            self.wizard.health -= (self.boss.damage if self.s.timer == 0 else max(self.boss.damage-self.s.value,1))
            self.s.timer = max(self.s.timer-1,0)
        
    def cast_spell(self,x):

        if self.mode == 'hard': self.wizard.health -= 1
        if self.wizard.health > 0:
            self.timers()
            if   x == 'D':  self.wizard.mana -= self.d.cost;  self.wizard.spend += self.d.cost;  self.boss.health -= self.d.value;  self.wizard.health += self.d.value
            elif x == 'M':  self.wizard.mana -= self.m.cost;  self.wizard.spend += self.m.cost;  self.boss.health -= self.m.value
            elif x == 'P':  self.wizard.mana -= self.p.cost;  self.wizard.spend += self.p.cost;  self.p.timer  = 0 + self.p.life
            elif x == 'R':  self.wizard.mana -= self.r.cost;  self.wizard.spend += self.r.cost;  self.r.timer  = 0 + self.r.life
            else:           self.wizard.mana -= self.s.cost;  self.wizard.spend += self.s.cost;  self.s.timer  = 0 + self.s.life
        
    def timers(self):
        
        if self.p.timer > 0:
            self.boss.health -= self.p.value;  self.p.timer -= 1            
        if self.r.timer > 0:
            self.wizard.mana += self.r.value;  self.r.timer -= 1
            

def search(f,best_score=(9999,'')):

    lo, hi, shields = search_params(f)
    spells = list('DMPRS')
    
    sequences = product(spells,repeat=(lo-1)) if lo >= 2 else product([''])
    
    for moves in range(lo,hi):
        best_score, sequences = find_score(f,sequences,shields,best_score)
        if len(sequences) == 0: break

    return best_score


def search_params(f):

    max_damage = (f.p.value*f.p.life)+(f.m.value*2) 
    h = 0 + f.boss.health
                                                                                     #  Establish the range of moves that the optimum solution is likely to fall within
    moves = 1 if h <= f.m.value else 2 if h <= (f.m.value + (f.p.value*3)) else 3    #  based upon the minimum moves to deplete the boss's health assuming infinite mana
    h -= min(h,max_damage-f.p.value)                                                 #  and health (and ignoring drain as an attacking move)
                                                                                     #  Also determine whether shields will be required based on wizard health
    while h >= max_damage:                                                           #  and boss's damage rating and adjust the minimum moves to account for this.  
        moves += (h//max_damage)*3;
        h -= (h//max_damage)*max_damage
        
    if h > 0:
        moves += 1 if h <= f.m.value else 2 if h <= (f.m.value + (f.p.value*3)) else 3
        
    shields =  moves // ((f.wizard.health // f.boss.damage) + 1)
    lo = moves + shields
    hi = lo+1 if shields > 0 else lo*2

    return lo, hi, shields


def find_score(f,sequences,shields,best_score):

    sequences = product([''.join(x) for x in sequences],list('DMPRS'))
    play = [];  stash = []

    for s in sequences:
        sequence = ''.join(s)
        damage, spend = evaluate_sequence(sequence,shields,best_score[0],f)
        
        if 0 <= damage < f.boss.health:
            stash += [sequence]                                            #  keep valid but insufficient sequences as a root to build the next sequences from
        if (damage >= f.boss.health and sequence[-1:] in 'MD'):            #  play valid & sufficient sequences if final spell is an attack of fully realised benefit
            play  += [(spend,sequence)]                                    #  else prune anything marked for discard (-ve damage) or with suboptimal final spell   
                                                                                             
    play = [x[1] for x in sorted(play)]

    for sequence in play:
        respawn = deepcopy(f)
        spend = fight(respawn,sequence)
        if 0 < spend < best_score[0]:                                      #  fight sequences are in ascending spend order
            best_score = (spend,sequence)                                  #  thus as soon as we find a more optimal sequence in this pass we can
            break                                                          #  simply discard the remainder as we already know they are more expensive
        
    return best_score, stash


def evaluate_sequence(sequence,shields,best,f):
    
    spend = 0;  shield_ct = 0;  damage = 0;  mana = 0 + f.wizard.mana
  
    for i,s in enumerate(sequence):
        
        if s in 'PRS' and s in sequence[i+1:i+3]: return (-1, None)              #  invalid spell sequence: discarded
        
        if 'R' in sequence[max(0,i-2):i]:   mana += f.r.value

        if   s == 'D':  spend += f.d.cost;  mana -= f.d.cost;  damage += f.d.value
        elif s == 'M':  spend += f.m.cost;  mana -= f.m.cost;  damage += f.m.value
        elif s == 'P':  spend += f.p.cost;  mana -= f.p.cost;  damage += min(((len(sequence[i+1:])*(2*f.p.value))+f.p.value),(f.p.life*f.p.value))
        elif s == 'R':  spend += f.r.cost;  mana -= f.r.cost;
        else:           spend += f.s.cost;  mana -= f.s.cost;  shield_ct += 1
        
        if mana < 0: return (-2, None)                                           #  invalid purchase - not enough mana: discarded
        
        if (s == 'R' or 'R' in sequence[max(0,i-2):i]):  mana += f.r.value

    if shield_ct < shields: return (-3, None)                                    #  sequence destined to lose as your health requires a shield purchase
    if spend >= best:       return (-4, None)                                    #  cannot be the optimum game as mana cost > an already known winning game

    return damage, spend


def fight(f,sequence):

    i = 0
    while (min(f.wizard.health,f.boss.health) > 0 and f.wizard.mana >= 0):

        f.cast_spell(sequence[i])
        if (min(f.wizard.health,f.boss.health) <= 0 or f.wizard.mana < 0): break
        f.boss_attack()
        i += 1
  
    return f.wizard.spend if f.wizard.health > 0 and f.wizard.mana >= 0 else -1


def main(fighters,mode='standard'):

    combatants = Fight(mode,*fighters)
    optimal_sequence = search(combatants)
    return optimal_sequence


print(main((50,500,58,9)))          # pt1
print(main((50,500,58,9),'hard'))   # pt2
