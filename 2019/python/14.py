#  Forget days 18 & 22... for no good reason Part 1 of this was my AoC 2019 nemesis. My first attempt treated this as some sort of mathematical formula exercise
#  where I could just replace a compound with it's constituent elements until left with various quantities of just those that could be produced from ore. 
#  Somehow that worked for all the examples even though I wasn't accounting for excess... but not the actual puzzle. I then had two failed attempts at a recursive
#  solution, where I was accounting for excess, but somehow each time I was missing something (still don't know what) with the answers coming in high. Only when
#  I switched to a simple, non-recursive queue based approach did whatever I was doing wrong magically disappear. Part 2 is just a simple binary search.
#  The code is slightly more complex than needs be, because I used this as an opportunity to play with use itertools.groupby and force it to behave like a SQL
#  group by to aggregate two lists.

from itertools import groupby
from math import ceil

def read_file(f):

    formulae = []
    for x,y in [tuple(x.split(' => ')[::-1]) for x in open(f,'r').read().split('\n')]:
        item = (x.split(' ')[1],int(x.split(' ')[0]))
        elements = dict([(y[1],int(y[0])) for y in [y.split(' ') for y in [y for y in y.split(', ')]]])
        formulae += [(item[0],(item[1],elements))]
    return dict(formulae)


def calculate_ore(item,qty,formulae):

    queue = [(item,qty)];  stash = {};  ore = 0

    while len(queue) > 0:

        queue_update = get_new_items(*queue.pop(0), formulae, stash)
        queue = [(x,sum([x[1] for x in y])) for x,y in groupby(sorted(queue+queue_update), lambda x: x[0])]
        ore += queue.pop(min([i for i,x in enumerate(queue) if x[0] == 'ORE']))[1]

    return ore


def get_new_items(item, qty, formulae, stash):

    queue_update = [('ORE',0)]
    std_qty, new_items = formulae[item]
    factor = ceil(qty/std_qty)   

    new_items = [(x,y*factor) for x,y in new_items.items()]
    stash = add_to_stash(item,stash,std_qty * factor,qty)

    for item, qty in new_items:
        stash, required = get_from_stash(item,stash,qty)
        queue_update += [(item,required)]       

    return queue_update


def add_to_stash(item,stash,generated,required):

    stash[item] = stash.get(item,0) + generated - required
    return stash
    

def get_from_stash(item,stash,required):

    excess = stash.get(item,0)
    stashed_qty = min(required,excess)
    if excess > 0: 
         stash[item] = stash[item] - stashed_qty
    
    return stash, required - stashed_qty
    

def calculate_fuel(item,target,formulae):

    ore, last_ore = (0,-1);  lo, hi = (0, (target//calculate_ore(item,1,formulae))*2)

    while ore != last_ore:
        qty = (lo+hi)//2
        last_ore = ore
        ore = calculate_ore(item,qty,formulae)
        lo, hi = (qty, qty) if ore == target else (qty, hi) if ore < target else (lo, qty)
    return lo if ore <= target else hi


def main(f):

    formulae = read_file(f)
    ore = calculate_ore('FUEL',1,formulae)
    fuel = calculate_fuel('FUEL',10**12,formulae)
    
    return ore, fuel

print(main('14.txt'))
