from itertools import permutations

def read_file(filepath,include_me):
    
    happiness = dict(((x[0][0:1],x[8][0:1]),int(x[1])) for x in [x.split(' ') for x in
                    [x for x in open(filepath,'r').read().replace('.','').replace('would gain ','+').replace('would lose ','-').split('\n')]])

    people = sorted(list(set([k[0] for k in happiness.keys()])))
    
    if include_me:
        happiness.update([(('!',x),0) for x in people] + [((x,'!'),0) for x in people])
        people += ['!']    
    
    arrangements = [x+x[0:1] for x in list(set([min(x,x[::-1]) for x in [''.join(x) for x in list(permutations(people,len(people)))]]))]
    
    return arrangements, happiness

def best_arrangement(arrangements, happiness):

    highest_ranking = 0
    
    for a in arrangements:
        ranking = 0
        for i,p in enumerate(a[1:]):       ranking += happiness[(a[i],p)]
        for i,p in enumerate(a[::-1][1:]): ranking += happiness[(a[::-1][i],p)]
        
        highest_ranking = max(ranking,highest_ranking)
  
    return highest_ranking

def main(filepath,include_me=False):

    arrangements, happiness = read_file(filepath,include_me)
    return best_arrangement(arrangements,happiness)

print(main('13.txt'))        # pt1
print(main('13.txt',True))   # pt2
