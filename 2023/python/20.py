#  For Part 2 used an online Graphviz implementation to visualise the network and then manually solved using
#  a circuit mod counter approach. Part 2 here is an automated implementation of that manual solve.

def parse_input(filepath):

    input = [(x[1:] if x[0] in '&%' else x, x[0] if x[0] in '&%' else '?', y.split(',')) 
                for x,y in [z.split('->') for z in open(filepath).read().replace(' ','').split('\n')]]

    downstream = dict([(x,z) for x,_,z in input])

    upstream = {}
    for src, targets in downstream.items():
        for target in targets:
            upstream[target] = upstream.get(target,[]) + [src]

    modtype = dict([(x,y) for x,y,_ in input] + [(x,'?') for x in upstream.keys() if x not in downstream.keys()])
    state   = dict(list(set([(k,0) for k in modtype.keys()] + [(k,0) for k in upstream.keys()])))

    return downstream, upstream, modtype, state


def press_button(modules, presses, counts=[0,0]):

    downstream, upstream, modtype, state = (d.copy() for d in modules)

    for _ in range(presses):

        counts[0] += 1
        queue = [(mod,0) for mod in downstream["broadcaster"]]

        while queue:

            mod, pulse = queue.pop(0)

            if modtype[mod] == "%" and pulse == 1: pass
            else:
                if modtype[mod] == "%" and pulse == 0: 
                    state[mod] = (state[mod]+1)%2
 
                if modtype[mod] == "&":
                    state[mod] = 0 if min([state[src] for src in upstream[mod]]) == 1 else 1
            
                if mod in downstream:
                    queue += [(target,state[mod]) for target in downstream[mod]]

            counts[pulse] += 1

    return counts[0]*counts[1]


def lcm(numbers):

    gcd  = lambda a,b: a if b == 0 else gcd(b,a % b)
    nums = list(sorted(list(set(numbers))))[::-1]

    while len(nums) > 1:
        nums = [(nums[0]*nums[1]) // gcd(nums[0],nums[1])] + nums[2:] 

    return nums[0]


def analyse_circuit_diagram(downstream,upstream,modtype,_):

    queue = ['broadcaster'];  conjunctions = [];  cycles = [];  previous = ''

    while not conjunctions:
        queue = [m for mod in queue for m in downstream[mod]]
        conjunctions = [m for m in queue if modtype[m] == '&']

    for module in conjunctions:

        circuit  = list(set(downstream[module]).intersection(upstream[module]))[:1]

        while len(circuit) == 1 or circuit[-1] != previous:

            previous = circuit[-1]
            next_modules = downstream[circuit[-1]]

            if len(next_modules) > 1:
                circuit += [m for m in next_modules if m != module]
            elif next_modules[0] != module:
                circuit += next_modules
            else: break

        binary_cycle = ''.join([str(len([x for x in upstream[m] if len(x) == 2])%2) for m in circuit[::-1]])
        cycles += [int(binary_cycle,2)]

    return lcm(cycles)


def main(filepath):

    modules = parse_input(filepath)

    return press_button(modules,1000), analyse_circuit_diagram(*modules)


print(main('20.txt'))
