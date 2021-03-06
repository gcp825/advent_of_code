from itertools import groupby

def look_and_say(nbr,yield_at):
    
    for i in range(1,max(yield_at)+1):
        nbr = ''.join([str(len(list(y)))+x for x,y in groupby(nbr)])
        if i in yield_at:
            yield len(nbr)

def main(nbr,yield_at=(1,)):

    return tuple([x for x in look_and_say(str(nbr),yield_at)])

print(main(3113322113,(40,50)))
