#  I enjoyed this one, and am pretty happy with the outcome (though the nature of Part 2 means it is pretty slow for that).
#  It was pretty clear to me from the outset that there were probably two ways to approach this:
#
#    i) Traverse the nested lists, mutating the hell out of them
#    ii) Try and flatten the structure into some other easier to navigate format
#
#    (Now that I'm looking at other people's solutions, it appears there was an option iii: string manipulation... bleeeuurgh!)
#
#  I think many would have gone for option ii as the easier approach, but that required thought, whereas the challenges for option i were immediately clear:
#  - figure out nearest left and right indices based on a given index
#  - figure out how to get and update nested list values by supplying an index of arbitrary length
# 
#  If I could come up with an answer for those, the rest would be trivial... and I'd already had the idea of generating the full list of possible indices in
#  left to right order using binary numbers which would make the former straightforward. The get & update also proved simple in the end - with the update
#  being the first time I've ever appreciated the shallow copying of references - and now I've got these as reusable components.
#
#  Obviously, having to continually traverse each list for reads and updates makes Part 2 slow... but I think it is worth it for the ease of implementation.
#  For fast performance on that, I'm pretty sure you'd need the flattened structure.

from ast import literal_eval
from functools import reduce

def list_depth(iterable,ct=0): return ct if not isinstance(iterable,list) else max([list_depth(x,ct+1) for x in iterable])

def add(iterable,indices,depth=5):

    updated = True
    while updated:
        iterable, updated = explode(iterable,depth,indices)
        if not updated:
            iterable, updated = split(iterable,indices)

    return iterable


def split(iterable,indices):

    for i in indices:
        target = nested_get(iterable,i)
        if type(target) is int and target >= 10:
            iterable = nested_update(iterable,i,[target//2,target-(target//2)])
            return iterable, True

    return iterable, False


def explode(iterable,depth,indices):

    if list_depth(iterable) == depth:
        for i in [index for index in indices if len(index) == depth-1]:
            item = nested_get(iterable,i)
            if isinstance(item,list):
                left, left_val, right, right_val = find_nearest(iterable,i,indices)
                if len(left) > 0:  
                    iterable = nested_update(iterable,left,left_val+item[0])
                if len(right) > 0: 
                    iterable = nested_update(iterable,right,right_val+item[1])
                iterable = nested_update(iterable,i,0)
                return iterable, True

    return iterable, False


def find_nearest(iterable,i,indices):

    nearest = [(),0,(),0]                                  

    left  = indices[:indices.index(i)][::-1]    # indices stored left to right, so we reverse the slice to bring the nearest left indexes to the front
    right = indices[indices.index(i)+3:]        # as index i refers to a list, the next 2 indices will be the contents of that list - thus we skip those

    for index in left:
        potential_target = nested_get(iterable,index)
        if type(potential_target) is int:
            nearest[0],nearest[1] = index, potential_target
            break

    for index in right:
        potential_target = nested_get(iterable,index)
        if type(potential_target) is int:
            nearest[2],nearest[3] = index, potential_target
            break

    return tuple(nearest)


def magnitude(x): return magnitude(x[0])*3 + magnitude(x[1])*2 if isinstance(x,list) else x


def nested_get(iterable, index, default=None):

    def _handled_get(x,y,default):

        try:    return x[y]
        except: return default

    return reduce(lambda x,y: _handled_get(x,y,default), index, iterable)


def nested_update(iterable, index, value):

    original = iterable

    for i in index[:-1]: 
        iterable = iterable[i]

    iterable[index[-1]] = value

    return original


def main(filepath):

    input   = [x for x in open(filepath,'r').read().split('\n')]
    numbers = [literal_eval(x) for x in input]
    a,c,z   = ('[',',',']')
    pairs   = [literal_eval(a+x+c+y+z) for x in input for y in input if x != y] + [literal_eval(a+y+c+x+z) for x in input for y in input if x != y]

    indices = list(sorted([tuple(map(int,list(str(bin(n))[2:].zfill(depth)))) for depth in range(1,6) for n in range(2**depth)]))

    pt1, pt2 = (numbers[0],0)

    for nbr in numbers[1:]: 
        pt1 = add([pt1,nbr],indices)

    for pair in pairs:
        pt2 = max(pt2, magnitude(add(pair,indices)))

    return magnitude(pt1), pt2
    
print(main('18.txt'))
