from collections import Counter

def parse_data(filepath):

    facts = [x.replace('[','').replace(']','').replace(':',' ').split(' ') for x in sorted(open(filepath,'r').read().split('\n'))]

    facts = [(this[3]+'/'+next[3],int(this[1]),int(this[2]),int(next[2]),this[4])
                 for i,this in enumerate([fact[:5] for fact in facts])
                 for j,next in enumerate([fact[:5] for fact in facts[1:]]+[['','00','60','end','']]) if i == j]

    facts = [(0 if state == 'up' else 1 if state == 'asleep' else int(state[1:])*-1,
              0 if hr == 23 else start,
              60 if actions == 'wakes/Guard' else end) for actions,hr,start,end,state in facts]

    return facts


def main(filepath):

    facts  = parse_data(filepath)
    asleep = dict()

    for state, start, end in facts:

        if state < 0:  guard = state*-1
        if state == 1: asleep[guard] = asleep.get(guard,[]) + [minute for minute in range(start,end)]

    most_common_minute_by_guard = list(sorted([(*Counter(asleep[guard]).most_common()[0][::-1],guard) for guard in asleep.keys()]))
    sleepiest_guard             = sorted([(len(v),k)for k,v in asleep.items()])[-1][1]

    pt1 = sleepiest_guard * [min for _, min, guard in most_common_minute_by_guard if guard == sleepiest_guard][0]
    pt2 = most_common_minute_by_guard[-1][1] * most_common_minute_by_guard[-1][2]

    return pt1, pt2
    
print(main('04.txt'))