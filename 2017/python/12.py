def determine_group(programs,start):
    
    members = set();  queue = [start] 

    while len(queue) > 0:
        members.add(queue[0])
        queue = queue[1:] + [p for p in programs[queue[0]] if p not in members]
       
    return list(sorted(members))

def main(filepath):

    programs = dict([(x[0],x[1:]) for x in [list(map(int,x.replace(' <->',',').split(','))) for x in open(filepath,'r').read().split('\n')]])
    groups = {}

    for k in programs.keys():
        group = determine_group(programs,k)
        groups[group[0]] = len(group)

    return groups[0], len(groups)

print(main('12.txt'))
