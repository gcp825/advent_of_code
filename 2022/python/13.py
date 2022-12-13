#  Ugh. Should have implemented the packets as a Class so I that could specify custom sort logic and just use the sorted function for Part 2.
#  But by the time I'd finished debugging Part 1, I was only in the mood for just getting part 2 done asap... so just went for a simple, clunky
#  compare every item in a list to every other item in the list comparison. 

def intify(x):  return x[0] if type(x) is list and len(x) == 1 and type(x[0]) is int else x

def listify(x): return [x] if type(x) is int else x


def compare(left,right):

    left, right = intify(left), intify(right)

    if type(left) is int and type(right) is int:

        return {-1:'<',0:'=',1:'>'}[(left-right)//(abs(left-right) or 1)]

    else:

        left, right = listify(left), listify(right)

        for a,b in tuple(zip(left,right)):

            a,b = listify(a), listify(b)

            if len(a) < len(b) and len(a) == 0:  return '<'

            if len(b) < len(a) and len(b) == 0:  return '>'

            if min(len(a),len(b)) > 0 :
                
                result = compare(a,b)

                if result in ('<','>'):  return result


    return '<' if len(left) <= len(right) else '>'


def main(filepath):

    div1, div2 = [[2]], [[6]]

    pairs    = [tuple(map(eval,x.split('\n'))) for x in open(filepath).read().split('\n\n')]
    unsorted = [eval(x) for x in open(filepath).read().replace('\n\n','\n').split('\n')]+[div1]+[div2]

    results, sorted = [], []

    for left, right in pairs: 
        results += [compare(left,right)]

    while unsorted:

        for i,x in enumerate(unsorted):

            remainder = unsorted[:i] + unsorted[i+1:]

            for y in remainder:

                if compare(x,y) == '>': break

            if compare(x,y) == '<': break

        sorted.append(unsorted.pop(i))

    return sum([i+1 for i,v in enumerate(results) if v == '<']), (sorted.index(div1)+1) * (sorted.index(div2)+1)

print(main('13.txt'))