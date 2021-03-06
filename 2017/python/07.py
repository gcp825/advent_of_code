#  This one made my head hurt. Just couldn't quite get my head around the problem enough for too long... and was not helped by the example that was far too easy to
#  get the right answer for with code that wouldn't work generally! Ultimately though, really happy with a short, quick, tidy piece of code that uses neither
#  regex nor recursion - it just relies on storing child-->parent relationships as a linked list and looping over levels of relationships. Like yesterday, seems
#  to be an approach where I haven't gone in the same direction as the reddit concensus.

from itertools import product, chain
from collections import Counter

def main(filepath):

    data = [x.replace('->',',').replace('(',',').replace(')','').replace(' ','').split(',') for x in open(filepath,'r').read().split('\n')]
    relationships = dict(list(chain(*[product(x[2:],x[:1]) for x in data if len(x) > 2])))

    weights = dict([(x[0],int(x[1])) for x in data]);  cumulative_weights = {};  unbalanced_trees = [];  level = 1

    parents = list(set([parent for child,parent in relationships.items() if child not in relationships.values()]))  #  Parents of children who aren't parents

#   Starting with the lowest level of parents, determine cumulative weights (weight of parent plus sum of cumulative weights of all children)
#   and then move up a generation by retrieving the parents of the current parents and so on back up to the origin.
#   If the weights for all children of a parent are not the same, add to the unbalanced tree list for investigation once we've navigated back to the origin

    while len(parents) > 0:

        for p in sorted(parents):
            children = list(sorted(child for child,parent in relationships.items() if parent == p))
            child_weights = [cumulative_weights.get(child,weights[child]) for child in children]
            cumulative_weights[p] = sum(child_weights) + weights[p]
            if len(list(set(child_weights))) > 1:
                unbalanced_trees += [(level,p,children,child_weights)]

        parents = list(set([parent for child,parent in relationships.items() if child in parents]))
        level += 1

#   Starting with the unbalanced sub-tree nearest the origin, find the child responsible for the weight imbalance. Move down to the next level and find the sub-tree 
#   where the problem child is a parent. Check if it is actually one of their children responsible and keep navigating down in a similar manner until you can go no further.
#   This gives you the problem program, whose individual (not cumulative) weight you then need to adjust to bring in line with it's siblings.

    depth, program = unbalanced_trees[-1][:2]
    for level, parent, children, child_weights in unbalanced_trees[::-1]:
        if level == depth and parent == program:
            counter = sorted([(v,k) for k,v in Counter(child_weights).items()])
            antimode, mode = counter[0][1], counter[-1][1]
            program = [children[i] for i in range(len(children)) if child_weights[i] == antimode][0]
            depth -= 1
 
    return min(parent for child,parent in relationships.items() if parent not in relationships.keys()),  weights[program]-(antimode-mode)

print(main('07.txt'))
