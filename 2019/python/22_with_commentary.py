#  This puzzle seems to have gotten a lot of flack for requiring too much complicated math knowledge to solve. I disagree with that. Applying advanced maths is certainly a
#  way to solve it, but AoC is a programming challenge, so there *should* be a way of solving it with a standard programming approach i.e logic, some brute force, a bit of
#  experimentation, basic maths and a dash of stackoverflow... and this solution is basically that.

#  Full disclosure: my original solution used a modular inverse calculation, but I can't claim any deep maths knowledge was required - it was clear that to invert existing 
#  functions we needed to reverse the modulo somehow, so I googled that, found code to do it and just used that (with a couple of stylistic changes). The most difficult bit 
#  was actually trying to work out how to use that function i.e. where to invoke it in the inverse formula, but a bit of trial and error sorted that out. However, I then
#  checked the reddit solutions thread, and it was mentioned that this wasn't necessary... the repeating nature of the deck means you can calculate the value of a card in a
#  specified position by using the formulae from part 1 with deck_size-y-1 shuffles, so as it fits with what I was attempting here I've since retrofitted that approach.

#  My basic summary here is: don't panic, don't get caught up with the mathy-ness of ot all, just focus on one problem at a time and you should get there.

from itertools import chain

#  Create a binary representation of the number of shuffles. For each binary digit, determine the actions needed to shuffle the deck the number of times represented by a 1
#  in that position i.e. the actions required to shuffle 1,2,4,8,16,32 times... (2**0 up to 2**46 for my part 2 value).

#  This can be simply done: any list of actions can be shrunk down to a maximum of 3 actions, once of each type (and often just 2: cut & deal). Thus...
#  To perform 1 shuffle we shrink the original instructions from 100 to 2 or 3 and store the result.
#  To perform 2 shuffles we take the shrunken output for 1 shuffle, repeat it (i.e. double to 4 or 6 actions), shrink and store that result.  
#  To perform 4 shuffles we take the shrunken 2 shuffle output, repeat, shrink and store... and so on (up to 70368744177664 for my input - taking just 47 iterations)

#  Next, reverse the list of stored actions to match the binary representation of number of shuffles i.e. the actions required for the largest num calculated will be first 
#  in the list & the actions for one shuffle last. For each bit with a value of '1' we take the actions in the corresponding position in our list of actions. Concatenating 
#  these gives the actions needed to perform the calculation for the supplied number of shuffles and as before we then shrink that down to just 2 or 3 final actions.

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

#  Adjacent actions of the same type can be combined together (deal, cut) or cancel each other out (reverse) enabling the list of instructions to be reduced in size,
#  ultimately to just one of each type. However, as the input actions contain no adjacent instructions of the same type we have to replace certain pairs of actions
#  with an alternate pair of actions that always return the same result to create the adjacent pairs that can then be combined.                                                                                                            

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

#  Two adjacent actions of the same type combine or cancel each other out in a pretty obvious way.
#  When swapping a pair of actions for an alternate pair, we only swap combinations of certain types - if we swapped every combination we'd be back where we started
#  with no adjacent combinable actions! Reversing the position of just one instruction type in a pair consistently seems sufficient... i.e. for any pair with 'deal'
#  as the second item in the pair, swap for an alternate pair that places 'deal' as the first item.
#  It's relatively straightforward to spot alternate pairs by just brute-forcing every possible permutation of action and parameter with a very small deck of cards,
#  grouping the permutations that produce the same output deck & checking to find consistent (math) relationships between parameters for suspected pairs + alternates.

def combine_actions(a,b,size):

    pair = (a[0],b[0])
    x, y = (a[1],b[1])

    actions = ( [('cut',(x+y)%size)]             if pair == ('cut','cut')    else
                [('deal',(x*y)%size)]            if pair == ('deal','deal')  else
                []                               if pair == ('rev','rev')    else 
                [('deal',y),('cut',(x*y)%size)]  if pair == ('cut','deal')   else   #  swap cut then deal for deal then cut
                [('deal',size-y),('cut',y)]      if pair == ('rev','deal')   else   #  swap rev then deal for deal then cut (no reversal to deal-then-rev exists)
                [a,b]                                                               #  else perform no action on the pair      
              ) 
    
    return actions

#  Each action (cut, deal, rev) can be expressed as a simple formula. We could compose 2 or 3 functions into one, but let's just keep it simple... 

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
    
    if mode == 2: shuffles = deck_size - shuffles - 1      #  Value of card in pos x (mode 2) after y iterations == pos of card x (mode 1) after deck_size-y-1 iterations
      
    actions = determine_actions_exponentially(orig_actions,deck_size,shuffles)
    
    return solve(x,actions,deck_size)


print(main('22.txt',1,2019,10007,1))
print(main('22.txt',2,2020,119315717514047,101741582076661))
