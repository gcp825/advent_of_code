from itertools import chain
from math import gcd

def determine_actions_exponentially(actions,deck_size,nbr_of_shuffles):

    nbr_of_shuffles_in_binary = list(bin(nbr_of_shuffles)[2:])                
    length = len(nbr_of_shuffles_in_binary);  shuffles = [];  i = 0                                                                                                        
                                                                        
    while i < length:                                                    
        i += 1                                                                                    
        actions = shrink_actions(actions,deck_size)                  
        shuffles += [actions]                                                                                              
        if i < length:                                                                                               
            actions = actions + actions

    shuffles = shuffles[::-1]                                                 
    actions = list(chain(*[shuffles[i] for i in range(length) if nbr_of_shuffles_in_binary[i] == '1']))  
    final_actions = shrink_actions(actions,deck_size)                                           
                                                                                                          
    return final_actions  
                                                                                                         

def shrink_actions(actions,size):

    while len(actions) > 3:                                                       #  continue shrinking until actions reduced as much as possible
        i = 0
        while i < len(actions)-1:
            new_actions = combine_actions(actions[i],actions[i+1],size)           #  work out what do do with each pair of actions
            if len(new_actions) == 0:
                actions.pop(i+1)                                                  #  -  if no actions returned, they cancel each other out, so remove both
                actions.pop(i)
            elif len(new_actions) == 1:                                           #  -  if one action returned, the pair have been combined into a single action - so
                actions.pop(i+1)                                                  #     remove the latter action and update the former with the combined action
                actions[i] = new_actions[0]
            else:                                                                 #  -  if two actions update both - they'll either be the original actions or a pair
                actions[i] = new_actions[0]                                       #     of alternate actions that enable combination in a subsequent iteration
                actions[i+1] = new_actions[1]                              
                i += 1                                                           

    return actions


def combine_actions(a,b,size):

    pair = (a[0],b[0])
    x, y = (a[1],b[1])

    actions = ( [('cut',(x+y)%size)]             if pair == ('cut','cut')    else   #  combine two in one
                [('deal',(x*y)%size)]            if pair == ('deal','deal')  else   #  combine two in one
                []                               if pair == ('rev','rev')    else   #  two cancel each other out so remove
                [('deal',y),('cut',(x*y)%size)]  if pair == ('cut','deal')   else   #  swap cut then deal for deal then cut
                [('deal',size-y),('cut',y)]      if pair == ('rev','deal')   else   #  swap rev then deal for deal then cut (no reversal to deal-then-rev exists)
                [a,b]                                                               #  else perform no action on the pair - the above swaps are enough to reorder                                                                 
              )                                                                     #  the actions to allow adjacent actions to be combined/cancelled in a later pass 

    return actions


def solve(mode,target,actions,deck_size):

    funcs = { 'cut':  lambda m,x,n,s: (x - n) % s if m == 1 else (x + n) % s
            , 'deal': lambda m,x,n,s: (x * n) % s if m == 1 else (x * invmod(n,s)) % s
            , 'rev':  lambda m,x,n,s: s - x - 1}

    actions = actions if mode == 1 else actions[::-1]
    for action, arg in actions:
        f = funcs[action]
        target = f(mode,target,arg,deck_size)
    return target


def invmod(n,modulus):

    if modulus == 1: return 0 

    if gcd(n,modulus) == 1:
        original_modulus = modulus
        x, y, prev_y = (1,0,0)

        while (n > 1):
            y = x - ((n // modulus)*y)            
            modulus, n, x = (n % modulus, modulus, prev_y)
            prev_y = y

        return x if x >= 0 else x + original_modulus

    else:  #  Naive calculation included for compatibility with the worked examples; won't be invoked for the actual puzzles as deck_size is prime

        for x in range(1, modulus):
            if (((n%modulus) * (x%modulus)) % modulus == 1):
                return x


def main(f,mode,target,deck_size,shuffles):

    actions = [(x,int(y)) if x == 'cut' else ('deal',int(y)) if x == 'increment' else ('rev',0) for x,y in [x.split(' ')[-2:] for x in open(f,'r').read().split('\n')]]

    actions = determine_actions_exponentially(actions,deck_size,shuffles)
 
    return solve(mode,target,actions,deck_size)

print(main('22.txt',1,2019,10007,1))
print(main('22.txt',2,2020,119315717514047,101741582076661))
