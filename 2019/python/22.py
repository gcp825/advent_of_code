#  This puzzle seems to have gotten a lot of flack for requiring too much complicated math knowledge to solve. I disagree with that. Applying advanced maths is certainly a
#  way to solve it, but AoC is a programming challenge, so there *should* be a way of solving it with a standard programming approach i.e logic, some brute force, a bit of
#  experimentation, basic maths and a dash of stackoverflow... and this solution is basically that.

#  Full disclosure: my original solution used a modular inverse calculation, but I can't claim any deep maths knowledge was required - it was clear that to invert existing 
#  functions we needed to reverse the modulo somehow, so I googled that, found code to do it and just used that (with a couple of stylistic changes). The most difficult bit 
#  was actually trying to work out how to use that function i.e. where to invoke it in the inverse formula, but a bit of trial and error sorted that out. However, I then
#  checked the reddit solutions thread, and it was mentioned that this wasn't necessary... the repeating nature of the deck means you can calculate the value of a card in a
#  specified position by using the formulae from part 1 with deck_size-y-1 shuffles, so as it fits with what I was attempting here I've since retrofitted that approach.

#  My basic summary here is: don't panic, don't get caught up with the mathy-ness of ot all, just focus on one problem at a time and you should get there.
#  For detailed explanation of what the code is doing see 22_with_commentary.py in this repo (this is the 'clean' version!)

from itertools import chain

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

    actions = ( [('cut',(x+y)%size)]             if pair == ('cut','cut')    else   #  combine 2 cuts
                [('deal',(x*y)%size)]            if pair == ('deal','deal')  else   #  combine 2 deals
                []                               if pair == ('rev','rev')    else   #  cancel out 2 revs
                [('deal',y),('cut',(x*y)%size)]  if pair == ('cut','deal')   else   #  swap cut then deal for deal then cut
                [('deal',size-y),('cut',y)]      if pair == ('rev','deal')   else   #  swap rev then deal for deal then cut (no reversal to deal-then-rev exists)
                [a,b]                                                               #  else perform no action (to allow combination with swapped actions in a future pass)     
              )     

    return actions


def solve(x,actions,deck_size):

    funcs = { 'cut':  lambda x,n,s: (x - n) % s , 
              'deal': lambda x,n,s: (x * n) % s ,
              'rev':  lambda x,n,s: s - x - 1 }

    for action, arg in actions:
        f = funcs[action]
        x = f(x,arg,deck_size)
    return x


def main(f,mode,x,deck_size,shuffles):

    orig_actions = [(x,int(y)) if x == 'cut' else ('deal',int(y)) if x == 'increment' else ('rev',0) for x,y in [x.split(' ')[-2:] for x in open(f,'r').read().split('\n')]]
    
    if mode == 2:  shuffles = deck_size - shuffles - 1    #  Value of card in pos x (mode 2) after y iterations == pos of card x (mode 1) after deck_size-y-1 iterations
      
    actions = determine_actions_exponentially(orig_actions,deck_size,shuffles)

    return solve(x,actions,deck_size)


print(main('22.txt',1,2019,10007,1))
print(main('22.txt',2,2020,119315717514047,101741582076661))
