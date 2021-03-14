def reverse_deck(d):     return d[::-1]

def cut_cards(d,n):      return d[n:]+d[:n]

def increment_deal(d,n): return [c for sorter,c in sorted([((i*n)%len(d),d[i]) for i in range(len(d))])]

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


def main(f,deck_size=11):

    actions = [(x,int(y)) if x == 'cut' else ('deal',int(y)) if x == 'increment' else ('rev',0) for x,y in [x.split(' ')[-2:] for x in open(f,'r').read().split('\n')]]
    act = shrink_actions(actions,deck_size)   
    deck = list(range(deck_size))

    print(actions)

    for i in range(deck_size):

        for action, n in act[:1]:
            if   action == 'rev':
                deck = reverse_deck(deck)
            elif action == 'cut':
                deck = cut_cards(deck,n)
            else:
                deck = increment_deal(deck,n)
        print(i+1,deck)

    return None

print(main('22a.txt'))
