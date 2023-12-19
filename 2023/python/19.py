# This code feels like a disaster zone, though from all the different possibilities in the puzzle and even the horrendous input
# horrendous input format, it's difficult to see how it can ever be really clean. Some more granular functions would likely help,
# though they might feel a little bit artificial.

def parse_input(filepath):

    f = [lambda x: list(map(tuple,x)), lambda x: x.split('='), lambda x: int(x[1])]

    w,p = open(filepath).read().split('\n\n')

    workflows = [(i,f[0]([x.split(':') for x in r.split(',')])) for i,r in [y[:-1].split('{') for y in w.split('\n')]]
    parts = [tuple(map(f[2],tuple(map(f[1],x)))) for x in [tuple(y[1:-1].split(',')) for y in p.split('\n')]]

    return dict(workflows), parts


def process_parts(parts,workflows):

    index = dict(zip('xmas',(0,1,2,3)))
    total = 0

    for part in parts:

        workflow = workflows['in']

        while True:

            for rule in workflow:
                condition, outcome = rule if len(rule) == 2 else ('',rule[0])
                if condition:
                    category, op, value = part[index[condition[0]]], condition[1], int(condition[2:])
                    if ((op == '<' and category < value) 
                    or  (op == '>' and category > value)):
                        break
                else:
                    break

            if outcome not in ('A','R'):
                workflow = workflows[outcome]
            else:
                total += sum(part) if outcome == 'A' else 0
                break

    return total


def process_ranges(workflows):

    diff = lambda x: x[1]-x[0]+1
    index = dict(zip('xmas',(0,1,2,3)))

    accepted = 0
    stack = [('in',[(1,4000),(1,4000),(1,4000),(1,4000)])]

    while stack:

        w, parts = stack.pop(-1)
        workflow = workflows[w]

        for rule in workflow:
            condition, outcome = rule if len(rule) == 2 else ('',rule[0])
            if condition:
                i = index[condition[0]]
                cat, op, v = parts[i], condition[1], int(condition[2:])

                if op == '<':
                    ranges = [cat,()] if cat[1] < v else [(cat[0],v-1), (v,cat[1])] if cat[0] < v else [(),cat]
                else:
                    ranges = [cat,()] if cat[0] > v else [(v+1,cat[1]), (cat[0],v)] if cat[1] > v else [(),cat]

                if ranges[0]:
                    match = [] + parts[:i] + [ranges[0]] + parts[i+1:]
                    if outcome == 'A':
                        accepted += diff(match[0])*diff(match[1])*diff(match[2])*diff(match[3])
                    elif outcome != 'R':
                        stack += [(outcome,match)]

                if ranges[1]:
                    parts = [] + parts[:i] + [ranges[1]] + parts[i+1:]
                else:
                    break
            else:
                if outcome == 'A':
                    accepted += diff(parts[0])*diff(parts[1])*diff(parts[2])*diff(parts[3])
                elif outcome != 'R':
                    stack += [(outcome,parts)]

    return accepted


def main(filepath):

    workflows, parts = parse_input(filepath) 

    return process_parts(parts,workflows), process_ranges(workflows)


print(main('19.txt'))
