#  This seemed to be much trickier than it initially looked. As a result I'm not completely happy with the code... it's a bit too
#  organic and feels like a refactor could be in order when I have time.

def determine_sequence(dependencies):

    steps        = len(list(set([x[0] for x in dependencies]+[x[1] for x in dependencies])))
    possible     = list(sorted(set([p for p,_ in dependencies if p not in [c for _,c in dependencies]])))
    sequence     = possible.pop(0)

    for i in range(steps-1):

        plausible = list(set([c for p,c in dependencies if sequence[-1] == p and c not in sequence and c not in possible]))

        possible = possible + [step for step in plausible if step not in 
                                  [s for s in plausible for p,c in dependencies if s == c and p not in sequence]]

        sequence += possible.pop(possible.index(min(possible)))

    return sequence


def determine_time(dependencies,time_offset,workers):

    work_allocations  = [('',0)] * workers
    queue             = list(sorted(list(set([x[0] for x in dependencies]+[x[1] for x in dependencies]))))
    steps             = len(queue)
    elapsed_time      = 0
    completed         = []

    while len(completed) < steps:

        unmet_dependencies = [c for p,c in dependencies if p not in completed]
        work_allocations   = [('' if s in completed else s,t) for s,t in work_allocations]  #  reset any completed worker allocations
        allocations        = []

        for allocation in work_allocations:

            step, time_remaining = allocation

            if (len(step) == 0 or time_remaining == 0) and len(queue) > 0:                  #  allocate new step to available workers if possible

                for i,s in enumerate(queue):
                    if s not in unmet_dependencies:
                        step = queue.pop(i)
                        time_remaining = ord(step)-time_offset
                        break

            allocations += [(step,time_remaining)]

        work_allocations = [(s,max(0,t-1)) for s,t in allocations]                          #  subtract 1 second from all eligible times remaining
        completed += [s for s,t in work_allocations if len(s) > 0 and t == 0]               #  add any completed steps to the completed list
        elapsed_time += 1

    return elapsed_time


def main(filepath,time_offset=4,workers=5):

    dependencies = [(x[5],x[36]) for x in open(filepath,'r').read().split('\n')]

    pt1 = determine_sequence(dependencies)
    pt2 = determine_time(dependencies,time_offset,workers)

    return pt1, pt2

print(main('07.txt'))
